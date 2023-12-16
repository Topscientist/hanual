from __future__ import annotations

from typing import TYPE_CHECKING, Any

from hanual.compile.context import Context
from hanual.util import Reply, Request, Response

if TYPE_CHECKING:
    from hanual.compile.bytecode_instruction import ByteCodeInstruction
    from hanual.lang.nodes.base_node import BaseNode


class Compiler:
    def __init__(self):
        self._instructions: list[ByteCodeInstruction] = []
        self._constants: set[int | str] = set()
        self._names: set[str] = set()

        self._context: list = []

    def compile_code(self, node: BaseNode):
        self.prepare_nodes(node)
        self.compile_body(node)

    def prepare_nodes(self, node: BaseNode):
        reply: Reply | None = None
        pipe = node.prepare()

        while True:
            try:
                req: Request = pipe.send(reply)

            except StopIteration:
                break

            reply = Reply(self._satisfy_prepare_request(req))

    def _satisfy_prepare_request(self, request: Request) -> list:
        req = iter(request.params)
        reply = []

        while True:
            req_type = next(req, None)

            if req_type is None:
                break

            if req_type == Request.ADD_CONSTANT:
                const = next(req)
                self._constants.add(const)
                reply.append(Reply.SUCCESS)

            elif req_type == Request.ADD_NAME:
                name = next(req)
                self._names.add(name)
                reply.append(Reply.SUCCESS)

            else:
                raise NotImplementedError(f"{req_type}")

        return reply

    def compile_body(self, nodes: BaseNode):
        instructions = nodes.gen_code()
        reply: Reply | None = None

        while True:
            try:
                val = instructions.send(reply)

            except StopIteration:
                break

            if isinstance(val, Request):
                reply = self._satisfy_compile_request(val)

            elif isinstance(val, Response):
                self._instructions.append(val.response)
                reply = Reply(True)  # accepted

            else:
                raise NotImplementedError

    def _satisfy_compile_request(self, request: Request) -> Reply:
        requests = iter(request.params)
        reply: list[Any] = []

        while True:
            req: Any | None = next(requests, None)

            if req is None:
                break

            if req == Request.GET_MEM_LOCATION:
                raise NotImplementedError

            elif req == Request.GET_CONTEXT:
                if len(request.params) == 1:
                    return self._context[-1]

                else:
                    reply.append(self._context[-1])

            elif req == Request.CREATE_CONTEXT:
                # create a blank context
                ctx = Context(deleter=self._delete_context, adder=self._add_context)

                self._context.append(ctx)

                if len(request.params) == 1:  # this is the only element
                    return Reply(ctx)

                else:
                    reply.append(ctx)

            else:
                raise Exception

        return Reply(reply)

    def _delete_context(self, ctx):
        self._context.remove(ctx)

    def _add_context(self, ctx):
        self._context.append(ctx)