from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, List, TypeVar, Union
from abc import ABC

if TYPE_CHECKING:
    from typing_extensions import Self

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class _ProductionInterface(ABC):
    def get(self, *args, **kwargs) -> T:
        pass

    def __format__(self, format_spec: Any) -> None:
        pass


P = TypeVar("P", bound=_ProductionInterface)


class DefaultProduction(_ProductionInterface, ABC, Generic[A, B, C]):
    __slots__ = ("ts",)

    def __init__(self: Self, ts: List[T]) -> None:
        self.ts: List[T] = ts

    @property
    def raw(self: Self) -> List[T]:
        return self.ts

    def __repr__(self: Self) -> str:
        return str(self.ts)

    def __getitem__(self: Self, item: int) -> Union[A, B, C]:
        return self.ts[item]

    def get(self, *args, **kwargs) -> T:
        return super().get(*args, **kwargs)
