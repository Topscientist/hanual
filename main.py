from __future__ import annotations

from hanual.lang.nodes import (
    FunctionDefinition,
    NamespaceAcessor,
    AssighnmentNode,
    ReturnStatement,
    FunctionCall,
    IfStatement,
    FreezeNode,
    BinOpNode,
    Condition,
    CodeBlock,
    Arguments,
)

from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin import HanualLexer, Token
from hanual.lang.pparser import PParser
from typing import Any

pre = PrePeoccesser()
lex = HanualLexer()
par = PParser()


@par.rule("NUM OP NUM")
def expr(ts: DefaultProduction):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("expr OP NUM")
def expr(ts: DefaultProduction):
    return BinOpNode(op=ts[1], left=ts[0], right=ts[2])


@par.rule("COM NUM", "COM expr", "COM f_call", "COM ID")
def arg(ts: DefaultProduction):
    return Arguments(ts[1])


@par.rule("ID arg", "expr arg", "f_call arg", "ID arg")
def arg(ts: DefaultProduction[Any, Arguments]):
    return ts[1].add_child(ts[0])


@par.rule("NSA ID")
def namespace_acesssor(ts: DefaultProduction[Token]):
    return NamespaceAcessor(ts[1])


@par.rule("ID namespace_acesssor")
def namespace_acesssor(ts: DefaultProduction[NamespaceAcessor, Token]):
    return ts[1].add_child(ts[0])


@par.rule(
    "ID LPAR RPAR",  # NO ARGS
    "ID LPAR expr RPAR",
    "ID LPAR ID RPAR",
    "ID LPAR STR RPAR",
    "ID LPAR arg RPAR",
    types={"ID LPAR args RPAR": 1, "ID LPAR RPAR": 2},
)
def f_call(ts: DefaultProduction, case):
    if case is None:  # single arg
        return FunctionCall(ts[0], Arguments(ts[2]))

    elif case == 1:  # multiple args
        return FunctionCall(ts[0], ts[2])

    elif case == 2:  # no args
        return FunctionCall(ts[0], None)


@par.rule("LET ID EQ NUM")
def assighnment(ts: DefaultProduction):
    return AssighnmentNode(target=ts[1], value=ts[3])


@par.rule("FREEZE ID")
def freeze(ts: DefaultProduction):
    return FreezeNode(ts[1])


@par.rule("RET")
def ret(ts):
    return ReturnStatement(None)


@par.rule("ID EL NUM", "ID EL f_call", "ID EL expr", "ID EL ID")
def condition(ts: DefaultProduction):
    return Condition(op=ts[1], left=ts[0], right=ts[2])


@par.rule(
    "IF LPAR condition RPAR line END",
    "IF LPAR condition RPAR lines END",
    "IF LPAR condition RPAR lines END",
    "IF LPAR condition RPAR END",
    "IF cond_f_call line END",
    "IF cond_f_call lines END",
    "IF cond_f_call lines END",
    "IF cond_f_call END",
    types={
        "IF LPAR condition RPAR line END": 1,
        "IF LPAR condition RPAR lines END": 1,
        "IF LPAR condition RPAR lines END": 1,
        "IF LPAR condition RPAR END": 2,
        "IF cond_f_call line END": 3,
        "IF cond_f_call lines END": 3,
        "IF cond_f_call lines END": 3,
        "IF cond_f_call END": 4,
    },
)
def if_statement(ts: DefaultProduction, type: int):
    if type == 1:
        return IfStatement(condition=ts[2], if_true=ts[4])

    elif type == 2:
        return IfStatement(condition=ts[2], if_true=None)

    elif type == 3:
        return IfStatement(condition=ts[1], if_true=ts[2])

    elif type == 4:
        return IfStatement(condition=ts[1], if_true=None)


@par.rule("FN f_call")
def function_marker(ts: DefaultProduction):
    return ts[1]


@par.rule("LPAR f_call")
def par_f_mark(ts):
    return ts[1]


@par.rule("par_f_mark RPAR")
def cond_f_call(ts):
    return ts[0]


@par.rule(
    "function_marker END",
    "function_marker line END",
    "function_marker lines END",
    types={
        "function_marker END": False,
    },
)
def function_definition(ts: DefaultProduction[FunctionCall], hasend: bool):
    if hasend is False:
        return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=None)

    return FunctionDefinition(name=ts[0].name, args=ts[0].args, inner=ts[1])


@par.rule("USE namespace_acesssor")
def using(ts: DefaultProduction[Token, NamespaceAcessor]):
    return ts[1]


@par.rule(
    "f_call",
    "assighnment",
    "if_statement",
    "freeze",
    "function_definition",
    "using",
    "ret",
)
def line(ts):
    return CodeBlock(ts[0])


@par.rule("line line", "line lines", "lines line")
def lines(ts: DefaultProduction[CodeBlock, Any]):
    return ts[0].add_child(ts[1])


print(
    par.parse(
        lex.tokenize(
            pre.process(
                open(r"D:\programing\hanual\hanual\src\hanual\bootstrap\IO.hint").read()
            )
        )
    )
)