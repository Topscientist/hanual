from __future__ import annotations

from abc import ABC
from typing import Generator, Union, Literal, NoReturn

from .base_instr import BaseInstruction, no_param
from ..instructions import Instruction


@no_param
class NOP(BaseInstruction):
    def compile(self) -> Generator[bytes, None, None]:
        yield Instruction.NOP.value.to_bytes()

    def validate(self) -> Union[Literal[None], NoReturn]:
        return 
