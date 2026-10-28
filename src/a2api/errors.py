"""Public errors contain codes and schema paths, never backend payloads."""

from __future__ import annotations


class A2APIError(Exception):
    def __init__(self, code: str, detail: str, *, status: int = 400,
                 issues: list[dict] | None = None):
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.status = status
        self.issues = issues or []

    def problem(self) -> dict:
        result = {
            "type": f"urn:a2api:problem:{self.code.lower().replace('_', '-')}",
            "title": self.code,
            "status": self.status,
            "detail": self.detail,
            "code": self.code,
        }
        if self.issues:
            result["issues"] = self.issues
        return result


def contract_error(detail: str) -> A2APIError:
    return A2APIError("INVALID_CONTRACT", detail)
