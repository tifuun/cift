import cift as cf

mycif="""
L L000;
DS 1;
P 10 10 20 30 40 50;
DF;
C 1;
E
"""

parser = cf.Parser(cf.grammars.strict.grammar, mycif)
cst = parser.parse()
cst.compute_string()
cf.astextra.reduce(cst)
cf.astextra.print_dot(cst)

