import sys
sys.path.append('/home/pablo/beampy-master')

from beampy import *

# We first create a new document for our presentation
# Remove quiet=True to see Beampy compiler output
doc = document(theme="mytheme", quiet=True)

with slide():
    maketitle(r'\textsc{Modelagem de células de Renshaw e sua utilização em simulações do sistema neuromuscular}',
              author='Pablo Alejandro de Abreu Urbizagastegui')

with slide('Table of content'):
    tableofcontents()

section('Introdução')
section('Metodologia')
with slide('My first slide title'):
    itemize(['un','dos','tres', '14'])
    # Maybe subitem works with groups

section('Resultados e discussões')
subsection('Desempenho computacional')
subsection('Validações')
subsection('Estudos exploratórios')
section('Conclusão')
with slide('My second slide title'):
    text('Hello Beampy!')

save('pres.html')
