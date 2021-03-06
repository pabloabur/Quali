import sys
sys.path.append('/home/pablo/beampy-master')

from beampy import *
from beampy.utils import draw_axes

doc = document(theme="mytheme")

with slide():
    maketitle(r'\textsc{Modelagem de células de Renshaw e sua utilização em simulações do sistema neuromuscular}',
              author='Pablo Alejandro de Abreu Urbizagastegui')

# TODO I think this is not really necessary
#with slide('Table of content'):
#    tableofcontents()

section('Introdução')
with slide():
    tableofcontents(currentsection=True)
with slide('A circuitaria da medula espinhal'):
    with group(x='auto', y='center') as g1:
        figure('figures/coluna.png', width=250)
    with group(x='auto', y='center') as g2:
        figure('figures/slice.png', width=200)
    text('Fonte: Bear, Connors e Paradiso (2016)', y=500, size=15)

with slide('A circuitaria da medula espinhal'):
    with group(x='auto', y='center') as g1:
        figure('figures/um.png', width=280)
    with group(x='auto', y='center') as g2:
        itemize(['Fibras do tipo S, FR e FF',
                 'Tipos de unidades motoras',
                 r'Tamanho $\times$ tipo'],
                 width=300)
    text('Fonte: Bear, Connors e Paradiso (2016)', x=80, y=450, width=250, size=15)

with slide('A circuitaria da medula espinhal'):
    figure('figures/circuit.png', width=400)

with slide('Teorias sobre possíveis funções da célula de Renshaw'):
    itemize(['Ordem de recrutamento',
             'Regulador de ganho variável',
             'Redução de correlações positivas e negativas',
             'Outras hipóteses'])

with slide('Objetivos'):
    itemize(['Melhora no desempenho computacional do simulador'],
            y=100)
    itemize(['Avaliar estratégias'], x=100, y=150)
    itemize(['Parametrização e avaliação'], y=200)
    itemize(['Célula de Renshaw e motoneurônio',
             'Dados experimentais da literatura de gatos'],
             x=100, y=250)
    itemize(['Estudos exploratórios'],
             y=350)
    itemize(['Recrutamento e taxa de disparos de motoneurônios',
             'Força muscular',
             'Análises espectrais'], x=100, y=400)

section('Metodologia')
subsection('Desempenho computacional')
with slide():
    tableofcontents(currentsubsection=True)

with slide('Modelos computacionais'):
    with group(x='auto', y='center') as g1:
        itemize(['ReMoto',
                 'Modelos dos neurônios',
                 'Versões: Java, Python e Fortran'])
    with group(x='auto', y='center') as g2:
        figure('figures/neuron.png', width=250)
    text('Fonte: Bear, Connors e Paradiso (2016)', x=500, y=500, size=15, width=250)

with slide('Modelos computacionais'):
    with group(x='auto', y='center') as g1:
        itemize(['ReMoto',
                 'Modelos dos neurônios',
                 'Versões: Java, Python e Fortran'])
    with group(x='auto', y='center') as g2:
        figure('figures/cisimodel.png', width=250)
    text('Fonte: Cisi e Kohn (2008)', x=500, y=500, size=15)

with slide('Desempenho computacional'):
    itemize(['Duas abordagens: Cluster e vetorização',
             'Cluster Águia'], y=110)
    itemize(['64 servidores físicos com 20 cores e 512 GB de RAM',
             'Processador Intel(R) Xeon(R) CPU E7-2870 com 2.4 GHz',
             'Python 2.7.13, distribuição Anaconda2 4.4.0',
             'MPI4Py',
             'Simulação simples'], x=100, y=210)

with slide('Desempenho computacional'):
    itemize(['Vetorização'], y=210)
    itemize(['Matriz com condutâncias de um grupo de neurônios',
             'Oito processadores i7-2600 a 3.40 GHz e 7.8 GB de RAM',
             'Python 2.7.14, distribuição Anaconda2 5.0.1-1'],
             x=100, y=260)
    itemize([r'$S=\frac{t_s}{t_p}$ e $E=\frac{t_s}{N_{proc}t_p}$'], y=410)

subsection('Parametrizações e validações')
with slide():
    tableofcontents(currentsubsection=True)
with slide('Parametrização de motoneurônios'):
    itemize(['Composição do núcleo motor',
             'Ativação do núcleo motor',
             'Dados da literatura utilizados'])
    figure('figures/mupres.png', x=550, y=40, width='28%')
    figure('figures/mntab.png', width='90%')
    text('Referências: (a) Mrówczyński, Celichowski e Krutki (2006), (b) Burke et al. (1971) e (c) Zengel et al. (1985)', y=500, size=15, width='90%')

with slide('Parametrização de célula de Renshaw'):
    itemize(['100 células de Renshaw/mm',
             'PEPS'], y=150)
    itemize(['Capacitância específica', 'Resistência específica'],
            x=100, y=250)
    figure('figures/metpeps.png', y=350, width='60%')
    text('Fonte: Adaptado de Walmsley e Tracey (1981)', y=520, size=15, width='60%')

with slide('Parametrização de célula de Renshaw'):
    itemize(['Características de disparos'], y=120)
    itemize(['Disparos espontâneos, limiar, comprimento e diâmetro'], y=170, x=100)
    itemize([r'Curva $F\times I$ e AHP'], y=220, x=100)
    itemize(['Variáveis de transição', 'densidade de condutâncias iônicas'],
             y=270, x=200)
    figure('figures/metfiring.png', y=350, width='60%')
    text('Fonte: Adaptado de Hultborn e Pierrot-Deseilligny (1979)', y=530, size=15, width='60%')

with slide('Parametrização de célula de Renshaw'):
    itemize(['PIPS'], y=100)
    itemize(['Condutâncias sinápticas'], y=150, x=100)
    itemize(['Sinapses no compartimento dendrítico'], y=200)
    figure('figures/metpips.png', width='50%', y=230)
    text('Fonte: Adaptado de Uchiyama, Johansson e Windhorst (2003)', y=530, size=15, width='70%')

with slide('Parametrização de célula de Renshaw'):
    itemize(['Distribuição do PIPS recorrentes'], y=100)
    itemize(['Conectividade', 'Condutâncias sinápticas (1:0.55:0.45)'],
             x=100, y=150)
    figure('figures/metpipsrecur.png', y=250, width='50%')
    text('Fonte: Adaptado de McCurdy e Hamm (1994)', y=470, size=15, width='50%')

with slide('Parametrização de célula de Renshaw'):
    itemize(['Resposta dinâmica e depressão sináptica'], y=100)
    itemize(['Constante de tempo', 'Intensidade da depressão'], y=150, x=100)
    figure('figures/metdin.png', y=230, width='40%')
    text('Fonte: Adaptado de Uchiyama, Johansson e Windhorst (2003)', y=520, size=15)

with slide('Resultados experimentais usados para validações'):
    figure('figures/methists.png', width='50%')
    text('Fonte: Adaptado de Hamm et al. (1987)', y=460, size=15, width='50%')

with slide('Resultados experimentais usados para validações'):
    figure('figures/metstatic.png', width='50%')
    text('Fonte: Cleveland, Kuschmierz e Ross (1981)', y=510, size=15, width='50%')

with slide('Resultados experimentais usados para validações'):
    figure('figures/meteccles.png', width='50%')
    text('Fonte: Eccles et al. (1961)', size=15, y=450, width='50%')

subsection('Estudos exploratórios')
with slide():
    tableofcontents(currentsubsection=True)
with slide('Efeitos da célula de Renshaw em simulações'):
    itemize(['Disparos de motoneurônios'], y=150)
    itemize([r'$i(t)=40t/1000$', r'$FD(t)=1500t/1000$'], x=100, y=200)
    itemize([''], x=100, y=400)
    figure('figures/fdeq.png', y=320, x=120, width='60%')

with slide('Efeitos da célula de Renshaw em simulações'):
    itemize(['Diminuição da força'], y=150)
    figure('figures/forcedecr.png', y=200, width='70%')
    text('Fonte: Adaptado de Granit e Renkin (1961)', y=450, size=15)

with slide('Efeitos da célula de Renshaw em simulações'):
    itemize(['Análise espectral'], y=130)
    figure('figures/mettabdci.png', y=180, width='50%')
    figure('figures/metspectral.png', y=330, width='70%')
    text('Fonte: Adaptado de Williams e Baker (2009)', y=550, size=15)

with slide('Efeitos da célula de Renshaw em simulações'):
    itemize(['Contrações isométricas'], y=250)
    itemize(['Diferentes porcentagens da contração voluntária máxima',
             'Coeficiente de variação',
             'Coeficiente de sincronia'], x=100, y=300)

with slide('Efeitos da célula de Renshaw em simulações'):
    itemize(['Modulação das taxas de disparos das fibras descendentes'], y=150)
    itemize([r'$10sen(2\pi0.5t)+5sen(2\pi1.0t)+2.5sen(2\pi2.5t)$'],
             x=100, y=200)
    itemize([r'$Q_1=\frac{B_1}{B_2}$',
             r'$Q_2=\frac{B_1}{B_3}$',
             r'$Q_3=\frac{\sqrt{B_1^2+B_2^2+B_3^2}}{\sqrt{B_j^2}}$',
             'CST'],
             y=250)
    figure('figures/auxq.png', x=350, y=250, width='50%')
    text(r'$B_1$', x=430, y=300, size=15)
    text(r'$B_2$', x=450, y=390, size=15)
    text(r'$B_3$', x=515, y=440, size=15)

with slide('Efeitos da célula de Renshaw em simulações'):
    itemize(['Modulação das taxas de disparos das fibras descendentes'], y=150)
    itemize([r'$10sen(2\pi0.5t)+5sen(2\pi1.0t)+2.5sen(2\pi2.5t)$'],
             x=100, y=200)
    itemize([r'$Q_1=\frac{B_1}{B_2}$',
             r'$Q_2=\frac{B_1}{B_3}$',
             r'$Q_3=\frac{\sqrt{B_1^2+B_2^2+B_3^2}}{\sqrt{B_j^2}}$',
             'CST'],
             y=250)
    figure('figures/metcst.png', x=350, y=250, width='50%')
    text('Fonte: Adaptado de Farina et al. (2014)',
         x=400, y=510, size=15, width='50%')

section('Resultados e discussões')
with slide():
    tableofcontents(currentsection=True)

with slide('Desempenho computacional'):
    figure('figures/resaguia.png', width='70%')
    figure('figures/resG.png', width='70%')

with slide('PEPS nas células de Renshaw'):
    figure('figures/metpeps.png', x='auto', y='center', width='50%')
    figure('figures/respeps.png', x='auto', y='center', width='50%')
    text('Fonte: Adaptado de Walmsley e Tracey (1981)',
         x=10, y=460, size=15, width='50%')

with slide('Disparos de células de Renshaw'):
    figure('figures/metfiring.png', width='60%')
    text('Fonte: Adaptado de Hultborn e Pierrot-Deseilligny (1979)', y=280, size=15)
    figure('figures/resfiring.png', width='70%')

with slide('Disparos de células de Renshaw'):
    figure('figures/resspont.png', y=120, width='30%')
    figure('figures/resfiringobs.png', y=300, width='70%')
    text('Fonte: Adaptado de Hultborn e Pierrot-Deseilligny (1979)', 
         x=140, y=500, size=15, width=240)

with slide('PIPS nos motoneurônios'):
    figure('figures/metpips.png', x='auto', y='center', width='50%')
    figure('figures/respips.png', x='auto', y='center', width='50%')
    text('Fonte: Adaptado de Uchiyama, Johansson e Windhorst (2003)',
         x=50, y=480, size=15, width='50%')

with slide('Distribuição topográfica dos PIPS'):
    figure('figures/metpipsrecur.png', x='auto', y='center', width='50%')
    figure('figures/respipsrecur.png', x='auto', y='center', width='50%')
    text('Fonte: Adaptado de McCurdy e Hamm (1994)',
         x=50, y=480, size=15, width='50%')

with slide('Característica dinâmica e depressão pós-sináptica'):
    figure('figures/metdin.png', x='auto', y='center', width='50%')
    figure('figures/resdin.png', x='auto', y='center', width='50%')
    text('Fonte: Adaptado de Uchiyama, Johansson e Windhorst (2003)',
         x=50, y=500, size=15, width='50%')

with slide('Características de PIPS recorrentes'):
    figure('figures/methists.png', width='40%')
    figure('figures/reshists1.png', width='80%')
    figure('figures/auxpips.png', y=100, x=550, width='35%')
    text('Fonte: Adaptado de Hamm et al. (1987)', y=300, size=15)
    arrow(x=632, y=197, dx=35, dy=0, style='<->')

with slide('Características de PIPS recorrentes'):
    figure('figures/reshists2.png', width='70%')

with slide('Características estáticas'):
    figure('figures/metstatic.png', width='30%')
    text('Fonte: Cleveland, Kuschmierz e Ross (1981)', y=320, size=15)
    figure('figures/resstatic.png', width='70%')

with slide('Resposta ao estímulo antidrômico'):
    figure('figures/meteccles.png', width='30%')
    figure('figures/resantidro.png', width='50%')
    text('Fonte: Eccles et al. (1961)', size=15, y=250, width='50%')

with slide('Diminuição da força'):
    figure('figures/forcedecr.png', y=100, width='50%')
    text('Fonte: Adaptado de Granit e Renkin (1961)', y=300, size=15)
    figure('figures/resforce.png', y=350, width='70%')

with slide('Recrutamento dos motoneurônios'):
    itemize([r'$i(t)=40t/1000$'], y=100)
    figure('figures/resrecruit1.png', y=150, width='60%')

with slide('Recrutamento dos motoneurônios'):
    itemize([r'$FD(t)=1500t/1000$'], y=100)
    figure('figures/resrecruit3.png', y=150, width='30%')
    figure('figures/resrecruit4.png', y=350, width='70%')
    text('Sem célula de Renshaw', x=430, y=550, size=15)
    text('Com célula de Renshaw', x=170, y=550, size=15)

with slide('Taxas de disparos de motoneurônios recrutados'):
    itemize([''])
    figure('figures/fdeq.png', y=115, x=70, width='30%')
    figure('figures/resonion.png', width='75%')
    text('Sem célula de Renshaw', x=160, y=500, size=15)
    text('Com célula de Renshaw', x=440, y=500, size=15)

with slide('Análise espectral'):
    figure('figures/resspect1.png', width='70%')
    text(r'5\% CMV', x=273, y=286, size=12)
    text(r'5\% CMV', x=553, y=286, size=12)
    text(r'70\% CMV', x=553, y=527, size=12)
    text(r'70\% CMV', x=273, y=527, size=12)

with slide('Análise espectral'):
    figure('figures/resspect3.png', width='70%')

with slide('Análise espectral'):
    figure('figures/resspect4.png', width='80%')

with slide('Contrações isométricas'):
    figure('figures/resiso.png', y=120, width='70%')
    figure('figures/resiso2.png', y=350, width='70%')
    text(r'5\% CMV', x=250, y=547, size=12)
    text(r'70\% CMV', x=533, y=547, size=12)
    itemize(['Desenvolvimento da força'], y=90)
    itemize(['Coeficientes'], y=320)

with slide('Distorções e controle da força'):
    itemize([r'$Q_1=\frac{B_1}{B_2}$',
             r'$Q_2=\frac{B_1}{B_3}$',
             r'$Q_3=\frac{\sqrt{B_1^2+B_2^2+B_3^2}}{\sqrt{B_j^2}}$'
             ])
    figure('figures/resqs.png', width='50%')
    figure('figures/resfft.png', y=100, x=300, width='55%')

with slide('Distorções e controle da força'):
    #draw_axes(show_ticks=True)
    itemize(['CSTs de motoneurônios'], y=100)
    figure('figures/rescst1.png', y=130, width='70%')
    text('Sem CR', x=273, y=311, size=12)
    text('Com CR', x=543, y=311, size=12)
    text('Com CR', x=543, y=547, size=12)
    text('Sem CR', x=273, y=547, size=12)

with slide('Distorções e controle da força'):
    itemize(['CSTs de células de Renshaw'])
    figure('figures/rescst2.png', width='90%')

with slide('Distorções e controle da força'):
    itemize(['Aumento do recrutamento de motoneurônios'])
    figure('figures/reslast.png', width='90%')

section('Conclusão')
with slide('Conclusões'):
    itemize(['Desempenho computacional'], y=100)
    itemize(['Possíveis melhorias'], x=100, y=150)
    itemize(['Modelo da célula de Renshaw'], y=200)
    itemize(['Recurso open source',
             'Apropriado para vários estudos',
             'Possíveis melhorias'], x=100, y=250)
    itemize(['Influência da inibição recorrente nas simulações'], y=400)
    itemize(['Estudos exploratórios',
             r'velocidade da força $\times$ qualidade do sinal transmitido'
             ], x=100, y=450)

with slide():
    itemize(['Obrigado!'])

save('pres.html')
