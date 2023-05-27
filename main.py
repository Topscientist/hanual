from __future__ import annotations


from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.util.dump_tree import dump_tree
from hanual.lang.nodes.block import CodeBlock
from hanual.compile.ir import IR
from pprint import PrettyPrinter


pp = PrettyPrinter()


class HanualMainClass:
    def __init__(self) -> None:
        self.preproc = PrePeoccesser()
        self.parser = get_parser()
        self.lexer = HanualLexer()

        # self.parser.toggle_debug_messages(True)

    def run(self, src: str) -> CodeBlock:
        whisper = self.preproc.process(src, starting_defs=["__testing_lang__"])
        whisper = self.lexer.tokenize(whisper)
        whisper = self.parser.parse(whisper)[0][1]
        return whisper


main = HanualMainClass()

res = main.run(
    r"""
let x = 0



"""
)

ir = IR()

# env = RuntimeEnvironment()
# print(res.run(env))

# pp.pprint(res.instructions)
# pp.pprint(res.deps)
# pp.pprint(res.compile(ir))
res.compile(ir)

print(dump_tree(ir, depth=12))


# print(dump_tree(res, depth=25))
# pp.pprint(res.as_dict())
