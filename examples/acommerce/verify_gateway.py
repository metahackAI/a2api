"""Check the a2api gateway against the raw facade, screen by screen, on a running a-commerce stack.

python examples/acommerce/verify_gateway.py --gateway http://127.0.0.1:7011 --out report.json

Each case sends the same request twice: in the screen's own fields and codes to the facade
(`?set=facade` on commerce), and in the converted names and words to the gateway. The check: same
HTTP outcome, and the gateway's result equals the facade's after the vocabulary is applied (names
renamed, codes as words). Writes run for real, so the demo store is reset before every write case.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from legacy_facade import CODES, RENAME  # noqa: E402
from stack import COMMERCE, call, token  # noqa: E402

WINDOW = {'starts_at': '2026-11-07T00:00', 'ends_at': '2026-11-08T23:59'}
# (converted tool, screen, converted input, screen input); `{claim}` / `{promotion}` are filled from reads.
CASES = [
    ('get_claim_grid_list', 'getClmGridList', {'claim_status': 'requested', 'min_claim_amount': 200, 'page_size': 5},
     {'clmStatCd': 'R10', 'clmAmtFrom': 200, 'pageSize': 5}),
    ('get_claim_grid_list_count', 'getClmGridListCnt', {'claim_status': 'requested', 'min_claim_amount': 200},
     {'clmStatCd': 'R10', 'clmAmtFrom': 200}),
    ('get_display_corner_list', 'getDispCornerList', {'page_type': 'main', **WINDOW},
     {'dispPageCd': '01', 'strtDtm': WINDOW['starts_at'], 'endDtm': WINDOW['ends_at']}),
    ('get_member_grade_list', 'getMbrGrdList', {}, {}),
    ('get_order_grid_list', 'getOrdGridList', {'order_status': 'processing', 'page_size': 5}, {'ordStatCd': '20', 'pageSize': 5}),
    ('get_order_grid_list', 'getOrdGridList', {'keyword': '27184'}, {'srchKwd': '27184'}),
    ('get_order_grid_list_count', 'getOrdGridListCnt', {'order_status': 'processing'}, {'ordStatCd': '20'}),
    ('get_order_grid_list_count', 'getOrdGridListCnt', {'order_status': 'processing', 'ordered_to': '2026-11-02'},
     {'ordStatCd': '20', 'ordDtmTo': '2026-11-02'}),
    ('get_order_detail_popup_init_data', 'getOrdDtlPopInitData', {'order_id': 'ord_27184'}, {'ordNo': 'ord_27184'}),
    ('get_order_detail_popup_init_data', 'getOrdDtlPopInitData', {'order_id': 'ord_20402'}, {'ordNo': 'ord_20402'}),
    # The order number people see: the gateway finds the key with the order grid (HANDLES); the screen
    # itself answers 404 for a bare number.
    ('get_order_detail_popup_init_data', 'getOrdDtlPopInitData', {'order_id': '#20402'}, {'ordNo': 'ord_20402'}),
    ('get_order_detail_popup_init_data', 'getOrdDtlPopInitData', {'order_id': '999999'}, {'ordNo': '999999'}),
    ('get_product_detail_info', 'getPrdDtlInfo', {'product_id': 'prd_wool_overcoat'}, {'prdNo': 'prd_wool_overcoat'}),
    ('get_product_detail_info_v2', 'getPrdDtlInfoV2', {'product_id': 'prd_wool_overcoat'}, {'prdNo': 'prd_wool_overcoat'}),
    ('get_product_grid_list', 'getPrdGridList', {'keyword': 'coat', 'availability': 'in_stock', 'page_size': 3},
     {'srchKwd': 'coat', 'sellStatCd': '10', 'pageSize': 3}),
    ('get_product_grid_list_count', 'getPrdGridListCnt', {'max_stock': 10}, {'stkQtyTo': 10}),
    ('get_promotion_grid_list', 'getPrmtGridList', {'promotion_status': 'running'}, {'prmtStatCd': '20'}),
    ('get_promotion_grid_list_count', 'getPrmtGridListCnt', {'promotion_status': 'running'}, {'prmtStatCd': '20'}),
    ('get_promotion_target_member_list', 'getPrmtTgtMbrList', {'member_status': 'active', 'page_size': 3},
     {'mbrStatCd': '10', 'pageSize': 3}),
    ('get_promotion_target_member_list_count', 'getPrmtTgtMbrListCnt', {'member_status': 'active'}, {'mbrStatCd': '10'}),
    ('get_refund_popup_init_data', 'getRfndPopInitData', {'claim_id': '{claim}'}, {'clmNo': '{claim}'}),
    ('get_sale_analysis_grid_list', 'getSaleAnlsGridList',
     {'from_date': '2026-11-05', 'to_date': '2026-11-05', 'compare_to': 'same_weekday_last_4_weeks'},
     {'srchStrtDt': '2026-11-05', 'srchEndDt': '2026-11-05', 'cmprBaseCd': '1'}),
    ('save_promotion_list', 'savePrmtList', {'rows': [{'row_action': 'update', 'promotion_id': '{promotion}', 'promotion_status': 'paused'}]},
     {'rows': [{'rowStat': 'U', 'prmtNo': '{promotion}', 'prmtStatCd': '30'}]}),
    ('save_coupon_list', 'saveCpnList', {'rows': [{'row_action': 'insert', 'coupon_code': 'CHECK10', 'promotion_id': '{promotion}',
                                                   'coupon_application': 'code_entry', 'stacking': 'no_other_coupons'}]},
     {'rows': [{'rowStat': 'I', 'cpnCd': 'CHECK10', 'prmtNo': '{promotion}', 'cpnAplyTpCd': '02', 'dupAplyCd': 'X'}]}),
    ('save_coupon_list', 'saveCpnList', {'rows': [{'row_action': 'insert', 'coupon_code': 'CHECK10', 'promotion_id': '{promotion}',
                                                   'target_member_grade': 'G00', 'coupon_application': 'code_entry',
                                                   'stacking': 'no_other_coupons'}]},
     {'rows': [{'rowStat': 'I', 'cpnCd': 'CHECK10', 'prmtNo': '{promotion}', 'tgtMbrGrdCd': 'G00', 'cpnAplyTpCd': '02',
                'dupAplyCd': 'X'}]}),
    ('save_display_banner_list', 'saveDispBnrList',
     {'rows': [{'row_action': 'insert', 'corner_id': 'slot_home_hero', 'starts_at': '2026-11-14T00:00', 'ends_at': '2026-11-15T23:59',
                'headline': 'Check', 'eyebrow': 'CHECK', 'button_label': 'Shop', 'link_url': '/c/check',
                'image_product_id': 'prd_wool_overcoat'}]},
     {'rows': [{'rowStat': 'I', 'cornerNo': 'slot_home_hero', 'strtDtm': '2026-11-14T00:00', 'endDtm': '2026-11-15T23:59',
                'bnrTitl': 'Check', 'bnrSubTitl': 'CHECK', 'btnNm': 'Shop', 'lnkUrl': '/c/check', 'imgPrdNo': 'prd_wool_overcoat'}]}),
    ('save_display_banner_list', 'saveDispBnrList',
     {'rows': [{'row_action': 'insert', 'corner_id': 'slot_home_hero', 'target_member_grade': 'G03', 'starts_at': '2026-11-14T00:00',
                'ends_at': '2026-11-15T23:59', 'headline': 'Check', 'eyebrow': 'CHECK', 'button_label': 'Shop',
                'link_url': '/c/check', 'image_product_id': 'prd_wool_overcoat'}]},
     {'rows': [{'rowStat': 'I', 'cornerNo': 'slot_home_hero', 'tgtMbrGrdCd': 'G03', 'strtDtm': '2026-11-14T00:00',
                'endDtm': '2026-11-15T23:59', 'bnrTitl': 'Check', 'bnrSubTitl': 'CHECK', 'btnNm': 'Shop', 'lnkUrl': '/c/check',
                'imgPrdNo': 'prd_wool_overcoat'}]}),
    ('save_customer_message_send', 'saveCustMsgSend', {'member_id': 'cus_alex', 'message_type': 'custom', 'channel': 'email',
                                                       'subject': 'Check', 'text': 'A check message.'},
     {'mbrNo': 'cus_alex', 'msgTpCd': 'M99', 'sndChnlCd': '1', 'msgTitl': 'Check', 'msgCntt': 'A check message.'}),
    ('save_refund_process', 'saveRfndProc', {'claim_id': '{claim}', 'refund_method': 'original_payment'},
     {'clmNo': '{claim}', 'rfndMthdCd': '01'}),
]


def readable(value, field=None):
    """The facade result as the vocabulary shows it: legacy names renamed, codes as words."""
    if isinstance(value, dict):
        return {RENAME.get(key, key): readable(item, key) for key, item in value.items()}
    if isinstance(value, list):
        return [readable(item, field) for item in value]
    if field in CODES and isinstance(value, str):
        return CODES[field].get(value, value)
    return value


# IDs a write creates differ between the two runs.
CREATED = {'msgNo', 'rfndNo', 'cpnNo', 'dispNo', 'prmtNo', 'preview_id'}


def created_blank(value):
    if isinstance(value, dict):
        return {key: '*' if key in CREATED or RENAME.get(key) in {RENAME.get(c) for c in CREATED} else created_blank(item)
                for key, item in value.items()}
    if isinstance(value, list):
        return [created_blank(item) for item in value]
    return value


def fill(value, known):
    text = json.dumps(value)
    for key, item in known.items():
        text = text.replace('{' + key + '}', item)
    return json.loads(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gateway', default='http://127.0.0.1:7011')
    parser.add_argument('--out', type=Path)
    options = parser.parse_args()
    agent, admin = token('admin', agent=True), token('admin')

    def reset():
        status, body = call(COMMERCE, 'POST', '/v1/platform/demo/reset', bearer=admin, timeout=120)
        assert status == 200, body
        call(COMMERCE, 'PUT', '/v1/platform/demo-clock', {'now': '2026-11-06T11:00', 'is_running': False}, bearer=admin)

    reset()
    _, claims = call(COMMERCE, 'POST', '/v1/tools/getClmGridList?set=facade', {'input': {'clmStatCd': 'R10', 'clmAmtFrom': 200}}, bearer=agent)
    _, promotions = call(COMMERCE, 'POST', '/v1/tools/getPrmtGridList?set=facade', {'input': {'prmtStatCd': '20'}}, bearer=agent)
    rows = lambda body: next((v for v in body.values() if isinstance(v, list)), []) if isinstance(body, dict) else []
    known = {'claim': rows(claims)[0]['clmNo'], 'promotion': rows(promotions)[0]['prmtNo']}
    report, failures = [], 0
    for tool, screen, converted, legacy in CASES:
        converted, legacy = fill(converted, known), fill(legacy, known)
        write = tool.startswith('save_')
        if write:
            reset()
        raw_status, raw = call(COMMERCE, 'POST', f'/v1/tools/{screen}?set=facade', {'input': legacy}, bearer=agent)
        if write:
            reset()
        status, out = call(options.gateway, 'POST', f'/v1/tools/{tool}?set=facade', {'input': converted}, bearer=agent)
        same_outcome = (raw_status == 200) == (status == 200)
        same_result = (created_blank(readable(raw)) == created_blank(out) if write else readable(raw) == out) \
            if raw_status == 200 and status == 200 else None
        ok = same_outcome and same_result is not False
        failures += not ok
        report.append({'tool': tool, 'screen': screen, 'input': converted, 'facadeStatus': raw_status, 'gatewayStatus': status,
                       'sameResult': same_result, 'ok': ok,
                       'gateway': out if status != 200 else None, 'facade': raw if raw_status != 200 else None})
        print(f"{'ok ' if ok else 'BAD'} {tool:42} facade {raw_status} gateway {status} same={same_result}"
              + ('' if status == 200 else f" | {json.dumps(out, ensure_ascii=False)[:160]}"))
    reset()
    if options.out:
        options.out.write_text(json.dumps({'cases': report, 'failures': failures}, ensure_ascii=False, indent=1))
    raise SystemExit(1 if failures else 0)


if __name__ == '__main__':
    main()
