"""a2api capability contracts and explicitly bound HTTP applications."""

from .catalog import Catalog
from .contracts import compile_contract, load_contract
from .errors import A2APIError
from .http_adapter import HTTPAdapter, HTTPHeaderParameter, HTTPQueryParameter, HTTPResponse, HTTPRoute
from .ir import Capability, ExecutionContext
from .runtime import Runtime
from .builder import BuildResult, build_contracts, load_build, load_review, source_digest, write_build
from .reviewed_adapter import HTTPDeployment, ReviewedHTTPAdapter
from .openapi_dependencies import dependency_index, diff_openapi
from .regeneration import IncrementalBuild, regenerate
from .reapproval import prepare_review, approve_review, write_review
from .conversion import ConvertedAPI, convert
from .native import Application, capability

__all__ = ["A2APIError", "Capability", "Catalog", "ExecutionContext", "HTTPAdapter", "HTTPHeaderParameter", "HTTPQueryParameter", "HTTPResponse", "HTTPRoute",
           "Runtime", "compile_contract", "load_contract", "BuildResult", "build_contracts", "load_build", "load_review",
           "source_digest", "write_build", "HTTPDeployment", "ReviewedHTTPAdapter", "dependency_index", "diff_openapi",
           "IncrementalBuild", "regenerate", "prepare_review", "approve_review", "write_review", "ConvertedAPI", "convert",
           "Application", "capability"]
