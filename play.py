import cift as cf
from pathlib import Path
from os import system

mycif="""
L L000;
DS 1;
L L001;
P 10 10 20 -30 -40 50;
DF;
C 1;
P -10 10 20 -30 -40 50;
E
"""

parser = cf.Parser(cf.grammars.strict.grammar, mycif)
cst = parser.parse()
cst.compute_string()
#cf.astextra.reduce(cst)
Path('cst.gv').write_text(cf.astextra.get_dot(cst))
system("sh -c 'dot -T png < cst.gv > cst.png'")
#cf.astextra.print_dot(cst)
monad = cf.semir.CSTMonad(cst)
semir = cf.semir.SemIR(monad)
semir.eval()
print(semir.build())
##semir.print()

#mycif="""C 1;"""
#
#parser = cf.Parser(cf.grammars.strict.grammar, mycif)
#cst = parser.parse(cf.grammars.strict.command)
#cst.compute_string()
##cf.astextra.reduce(cst)
#cf.astextra.print_dot(cst)
#
#gr = cf.grammars.strict
#monad = cf.semir.CSTMonad(cst)
#print(
#    cf.semir.RoutCall(
#        monad
#        .sole_child(gr.prim_command)
#        .sole_child(gr.call_command)
#        )
#    )


