import sys
sys.path.append('/home/pablo/beampy-master')

from beampy import *

# We first create a new document for our presentation
# Remove quiet=True to see Beampy compiler output
doc = document(theme="mytheme", quiet=True)

with slide():
    maketitle(r'\textsc{Modelagem de células de Renshaw e sua utilização em simulações do sistema neuromuscular}',
              author='Pablo Alejandro de Abreu Urbizagastegui')

# I think this is not really necessary
#with slide('Table of content'):
#    tableofcontents()

section('Introdução')
with slide('A circuitaria da medula espinhal'):
    with group(x='auto', y='center') as g1:
        figure('figures/coluna.png', width=250)
    with group(x='auto', y='center') as g2:
        figure('figures/slice.png', width=200)
    text('Fonte: Bear, Connors e Paradiso (2016)', y=500)

with slide('A circuitaria da medula espinhal'):
    with group(x='auto', y='center') as g1:
        figure('figures/um.png', width=280)
    with group(x='auto', y='center') as g2:
        itemize(['Fibras do tipo S, FR e FF',
                 'Tipos de unidades motoras',
                 r'Tamanho $\times$ tipo'],
                 width=300)
    text('Fonte: Bear, Connors e Paradiso (2016)', x=60, y=450, width=250)

section('Metodologia')
section('Resultados e discussões')
subsection('Desempenho computacional')
subsection('Validações')
subsection('Estudos exploratórios')
section('Conclusão')

save('pres.html')
