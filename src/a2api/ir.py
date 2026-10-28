"""Immutable, language-independent capability intermediate representation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


def freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({k: freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(freeze(v) for v in value)
    return value


def thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: thaw(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [thaw(v) for v in value]
    return value


@dataclass(frozen=True)
class ValueRef:
    source: str
    pointer: str = ""
    step: str | None = None
    value: Any = None

    @classmethod
    def from_dict(cls, value: dict) -> ValueRef:
        return cls(value["from"], value.get("pointer", ""), value.get("step"),
                   freeze(value.get("value")))


@dataclass(frozen=True)
class Check:
    result_pointer: str
    equals: ValueRef
    code: str


@dataclass(frozen=True)
class Operation:
    id: str
    service_ref: str
    operation_ref: str
    input_schema: Mapping
    output_schema: Mapping


@dataclass(frozen=True)
class Step:
    id: str
    operation_id: str
    inputs: Mapping[str, ValueRef]
    depends_on: tuple[str, ...]
    checks: tuple[Check, ...]
    foreach: ValueRef | None = None
    max_items: int = 1
    parallelism: int = 1
    select: tuple[str, ...] | None = None


@dataclass(frozen=True)
class Capability:
    id: str
    version: str
    title: str
    enabled: bool
    sample_only: bool
    required_scopes: frozenset[str]
    input_schema: Mapping
    output_schema: Mapping
    operations: Mapping[str, Operation]
    steps: tuple[Step, ...]
    outputs: Mapping[str, ValueRef]
    execution: Mapping
    manifest_json: str

    def describe(self) -> dict:
        # A fresh copy prevents callers from changing a catalog snapshot.
        return json.loads(self.manifest_json)


@dataclass(frozen=True)
class ExecutionContext:
    actor: str
    tenant: str
    scopes: frozenset[str]

    def __post_init__(self) -> None:
        for identifier in (self.actor, self.tenant):
            if not isinstance(identifier, str) or not identifier or len(identifier) > 256 or not identifier.isascii() or any(ord(c) < 33 or ord(c) > 126 for c in identifier):
                raise ValueError("actor and tenant must be nonempty printable ASCII identifiers")
        if isinstance(self.scopes, str) or any(not isinstance(s, str) or not s for s in self.scopes):
            raise ValueError("scopes must be a collection of nonempty strings")
        object.__setattr__(self, "scopes", frozenset(self.scopes))

    def values(self) -> dict:
        return {"actor": self.actor, "tenant": self.tenant}
