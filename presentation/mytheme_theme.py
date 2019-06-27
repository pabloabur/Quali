# Defining colors
navyBlue = '#000080'
papayaWhip = '#FFEFD5'
khaki = '#C3B091'
rawUmber = '#826644'

THEME = {}

THEME['tableofcontents'] = {
    'section_decoration_color': navyBlue,
    'section_text_color': navyBlue,
    }

THEME['itemize'] = {
    'x':50,
    'item_color':navyBlue,
    }

THEME['title'] = {
    'y': 75,
    'color': navyBlue,
    }

######################## Define the layout of each slide ###################
from beampy.commands import *
def createMakeTitle(titlein, author = []):
    from beampy.modules.svg import rectangle
    from beampy.modules.core import group
    from beampy.modules.text import text
    from beampy.modules.figure import figure
    from beampy.document import document

    # Main maketitle text elements
    args = THEME['maketitle']

    rectangle(x=0, y=0, width=document._width,
              height=document._height, color=args['background-color'],
              edgecolor=None)

    with group(x=10, y='center', width='70%') as g6:
        text(titlein, y=0, color=args['title_color'],
             size=args['title_size'])
        text(author, x=g6.left+10, y="+1.5cm",
             color=args['author_color'], size=args['author_size'])
        text('Orientador: André Fabio Kohn', x=g6.left+10, y="+0.5cm",
             color=args['author_color'], size=args['author_size'])

    # Upper part
    with group(y=0, background=khaki, height=100, width='100%') as g1:
        text(r'\textsc{LABORATÓRIO DE ENGENHARIA BIOMÉDICA}', x=390,
             y='center', color='#ffffff', size=12)

    # Lower part
    with group(x=0, y=550, height=50, width=800) as g2:
        with group(x=g2.left+10, y=g2.top-8) as g3:
            figure('./figures/usp-logo-eps.jpg', width=50)
        with group(x=g2.left+70, y=g2.top+8) as g6:
            text('Escola Politécnica da Universidade de São Paulo - 2 de julho de 2019',
                 size=10, color='#888888')
        with group(x=0, y=20, height=10, width=800) as g5:
            rectangle(y=0, color=rawUmber, height=5,
                      edgecolor=rawUmber)
            rectangle(y=5, color=khaki, height=5,
                      edgecolor=khaki)
        with group(x=g3.right+690, y=g2.top+2) as g4:
            figure('./figures/EP.jpg', width=40)

THEME['maketitle'] = {
    'title_color': navyBlue,
    'background-color': papayaWhip,
    'template': createMakeTitle
    }

######################## Define the layout of each slide ###################
def createSlideLayout():
    from beampy.modules.svg import rectangle
    from beampy.modules.core import group
    from beampy.modules.text import text
    from beampy.modules.figure import figure
    from beampy.document import document

    # Upper part
    with group(y=0, background=khaki, height=30, width='100%') as g1:
        text(r'\textsc{LABORATÓRIO DE ENGENHARIA BIOMÉDICA}', x=390,
             y='center', color='#ffffff', size=12)

    # Lower part
    with group(x=0, y=550, height=50, width=800) as g2:
        with group(x=g2.left+10, y=g2.top-8) as g3:
            figure('./figures/usp-logo-eps.jpg', width=50)
        with group(x=0, y=20, height=10, width=800) as g5:
            rectangle(y=0, color=rawUmber, height=5,
                      edgecolor=rawUmber)
            rectangle(y=5, color=khaki, height=5,
                      edgecolor=khaki)
        with group(x=g3.right+690, y=g2.top+2) as g4:
            figure('./figures/EP.jpg', width=40)

        # Counting slides and displaying them
        numSlides = len(document._slides)
        curSlide = int(document._curentslide.split('_')[1]) + 1
        text('%i/%i'%(curSlide, numSlides), x=12, y=32, size=10)

THEME['slide'] = {
    'background': "white",
    'layout': createSlideLayout, 
}
