"""Opt-in live model verification using the existing actual source HTTP servers."""

import argparse
import asyncio
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.request import urlopen

from jsonschema import Draft202012Validator
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from a2api.api import input_schema
from a2api.mcp_schemas import output_schemas
from client import ALIASES, run_question

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0,str(REPO/'examples/source-http'))
import verify as servers

def assess(run, kind, ids, language):
    failures, known, discovered, invoked = [], {}, {}, []
    schemas = output_schemas()
    reverse = {value: key for key, value in ids.items()}
    for call in run['calls']:
        method = call['tool'].split('.')[-1]
        args, payload = call['input'], call['output']
        if not Draft202012Validator(input_schema(method)).is_valid(args):
            failures.append('wire_input_mismatch')
        if not Draft202012Validator(schemas[method]).is_valid(payload):
            failures.append('wire_output_mismatch')
        if 'internalNote' in json.dumps(payload):
            failures.append('private_field_exposed')
        if method == 'discover' and 'capabilities' in payload:
            discovered.setdefault(payload['catalogVersion'], set()).update((x['id'], x['version']) for x in payload['capabilities'])
        elif method == 'describe' and 'capability' in payload:
            descriptor = payload['capability']
            key = (descriptor['id'], descriptor['version'])
            if key not in discovered.get(payload['catalogVersion'], set()):
                failures.append('describe_without_discovery')
            known[key] = descriptor
        elif method == 'invoke':
            descriptor = known.get((args.get('id'), args.get('version')))
            if descriptor is None or (args.get('id'), args.get('version')) not in discovered.get(args.get('catalogVersion'), set()):
                failures.append('invoke_without_discovery_and_description')
            elif not Draft202012Validator(descriptor['inputSchema']).is_valid(args.get('input')):
                failures.append('business_input_mismatch')
            if descriptor and payload.get('status') == 'succeeded' and not Draft202012Validator(descriptor['outputSchema']).is_valid(payload.get('data')):
                failures.append('business_output_mismatch')
            route = reverse.get(args.get('id'))
            invoked.append((route, args.get('input', {}), payload))
    if run.get('hostError') or not run.get('answer'):
        failures.append('host_or_answer_incomplete')
    if kind == 'read':
        if Counter(x[0] for x in invoked) != Counter([('GET', '/items/{id}'), ('HEAD', '/items/{id}')]):
            failures.append('expected_read_and_head_missing_or_extra_invokes')
        for route, args, result in invoked:
            if args != {'path': {'id': 'I-1'}} or result.get('status') != 'succeeded' or result.get('httpStatus') != 200:
                failures.append('read_input_or_status_mismatch')
            if route and route[0] == 'GET' and result.get('data') != {'id': 'I-1', 'name': 'original'}:
                failures.append('original_data_mismatch')
    elif kind == 'crud':
        expected = [('POST', '/items'), ('PUT', '/items/{id}'), ('PATCH', '/items/{id}'),
                    ('POST', '/items/search'), ('DELETE', '/items/{id}'), ('GET', '/items/{id}')]
        if [x[0] for x in invoked] != expected:
            failures.append('crud_sequence_missing_or_extra_invokes')
        if len(invoked) == 6:
            created_id = (invoked[0][2].get('data') or {}).get('id')
            run['createdId'] = created_id
            if not isinstance(created_id, str) or created_id == 'I-1':
                failures.append('created_id_missing_or_protected')
            for index, (route, args, result) in enumerate(invoked):
                if index in (0, 1, 2):
                    suffix = ('create', 'replace', 'patch')[index]
                    expected_name = f'local-{language}-{suffix}'
                    if args.get('body') != {'name': expected_name} or result.get('data') != {'id': created_id, 'name': expected_name}:
                        failures.append('mutation_input_or_output_mismatch')
                if index in (1, 2, 4, 5) and args.get('path') != {'id': created_id}:
                    failures.append('created_id_not_reused')
                if index < 5 and result.get('status') != 'succeeded':
                    failures.append('mutation_or_search_failed')
                if index == 0 and result.get('httpStatus') != 201:
                    failures.append('created_status_mismatch')
                if index == 3 and (args.get('body') != {'q': f'local-{language}-patch'} or result.get('data') != [{'id': created_id, 'name': f'local-{language}-patch'}]):
                    failures.append('search_mismatch')
                if index == 4 and (result.get('httpStatus') != 204 or result.get('data') is not None):
                    failures.append('delete_status_mismatch')
                if index == 5 and (result.get('status') != 'failed' or result.get('error', {}).get('code') != 'RESOURCE_NOT_FOUND'):
                    failures.append('deleted_resource_not_found_missing')
    elif invoked:
        failures.append('missing_id_invoked_instead_of_clarifying')
    return {'passed': not failures, 'failures': sorted(set(failures)), 'invokeCount': len(invoked),
            'answerReview': 'required', 'clarificationReview': 'required' if kind == 'clarify' else 'not_applicable'}


def independent(origin, created_id):
    result = {}
    with urlopen(origin+'/items/I-1',timeout=10) as response:
        data = json.loads(response.read(8192));result['originalUnchanged'] = data['id']=='I-1' and data['name']=='original'
    if created_id:
        try:
            with urlopen(origin+'/items/'+created_id,timeout=10) as response:result['deletedHTTPStatus'] = response.status
        except HTTPError as error:result['deletedHTTPStatus'] = error.code
    result['passed'] = result['originalUnchanged'] and result.get('deletedHTTPStatus')==404
    return result


async def language_checks(language, origin, args):
    _, ids = servers.application(language,origin,search_metadata=not args.plain_descriptions)
    command = [str(servers.ROOT/'mcp_server.py'),'--language',language,'--origin',origin]
    if args.plain_descriptions:command.append('--plain-descriptions')
    parameters = StdioServerParameters(command=sys.executable,args=command)
    scenarios = json.loads((HERE/'scenarios.json').read_text())
    runs = []
    async with Client(parameters,read_timeout_seconds=30) as client:
        listing = await client.list_tools()
        serialized = json.dumps(listing.model_dump(mode='json'))
        assert all(identifier not in serialized for identifier in ids.values())
        for case in scenarios:
            if case['language'] != language:continue
            run = await run_question(client,case['question'],base_url=args.base_url,model=args.model,
                                     api_key=os.environ.get(args.api_key_env))
            run.update(language=language,scenario=case['id'])
            run['checks'] = assess(run,case['id'],ids,language)
            runs.append(run)
            print(language+'/'+case['id']+': '+json.dumps(run['checks']),flush=True)
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.with_name(language+'-partial.json').write_text(json.dumps(runs,ensure_ascii=False,indent=2)+'\n')
    created = next((run.get('createdId') for run in runs if run['scenario']=='crud'),None)
    return {'language':language,'capabilities':len(ids),'businessSchemasInToolsList':False,
            'toolsListBytes':len(serialized.encode()),'runs':runs,'independentHTTP':independent(origin,created)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',default=os.environ.get('A2API_MODEL_BASE_URL'))
    parser.add_argument('--model',default=os.environ.get('A2API_MODEL'))
    parser.add_argument('--api-key-env',default='A2API_MODEL_API_KEY')
    parser.add_argument('--language',choices=['all','spring','go','rust'],default='all')
    parser.add_argument('--plain-descriptions',action='store_true')
    parser.add_argument('--output',type=Path,default=REPO/'artifacts/model-client/report.json')
    args = parser.parse_args()
    if not args.base_url or not args.model:parser.error('Configure --base-url and --model or the model environment variables.')
    paths,env = servers.tools()
    servers.ARTIFACTS.mkdir(parents=True,exist_ok=True)
    report = {'checkedAt':datetime.now(timezone.utc).isoformat(),'model':args.model,
              'searchMetadata':not args.plain_descriptions,'argumentsRepaired':False,
              'automaticRetries':False,'reasoningStored':False,'results':[]}
    for language in (['spring','go','rust'] if args.language=='all' else [args.language]):
        print('Building '+language,flush=True)
        command = servers.build(language,paths,env)
        with servers.running(language,command,env) as origin:
            report['results'].append(asyncio.run(language_checks(language,origin,args)))
        runs=[run for result in report['results'] for run in result['runs']]
        calls=[call for run in runs for call in run['calls']]
        report['summary']={'scenarios':len(runs),'passed':sum(run['checks']['passed'] for run in runs),
            'modelDrivenAPIInvocations':sum(run['checks']['invokeCount'] for run in runs),
            'mcpCalls':dict(Counter(call['tool'] for call in calls)),
            'emptyDiscoveryResults':sum(call['tool']=='a2api.discover' and not call['output'].get('capabilities') for call in calls),
            'chatCompletionRequests':sum(len(run['steps']) for run in runs)}
        report['passed']=all(result['independentHTTP']['passed'] and all(run['checks']['passed'] for run in result['runs']) for result in report['results'])
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('AUTOMATIC CHECKS: '+str(report['passed']),flush=True)
    return 0 if report['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
