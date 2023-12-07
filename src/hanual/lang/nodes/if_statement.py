from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from .base_node import BaseNode

from hanual.util import Reply, Response, Request


if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

    from .block import CodeBlock
    from .conditions import Condition


class IfStatement(BaseNode):
    __slots__ = "_condition", "_block", "_lines", "_line_range"

    def __init__(
            self,
            condition: Condition,
            block: CodeBlock,
            lines: str,
            line_range: LineRange,
    ) -> None:
        self._condition: Condition = condition
        self._block: CodeBlock = block

        self._lines = lines
        self._line_range = line_range

    @property
    def condition(self) -> Condition:
        return self._condition

    @property
    def block(self) -> CodeBlock:
        return self._block

    def compile(self) -> Generator[Reply | Request, Response, None]:
        raise NotImplementedError
