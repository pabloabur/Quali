# PoliLatex

Este repositório contém uma classe para produzir Teses e Dissertações no formato da Escola Politécnica da Universidade de São Paulo.

Para utilizá-lo, faça o download do conteúdo do repositório e o armazene em um único diretório. Para executar um exemplo, compile o arquivo tese.tex.

Para mudar os dados da capa e folha de rosto, edite o arquivo capa.tex.

O conteúdo deste repositório foi fortemente baseado na classe abnTex. 

# Troubleshooting
* Se ocorrer um erro no arquivo .bbl, tente deletá-lo
* Acentos no nome dos autores pode ocasionar em erros, símbolos estranhos ou,
  caso se use artifícios como \"{u}, por exemplo, letras minúsculas na 
  bibliografia. A solução é usar, a partir do exemplo anterior, \"u.
* Sometimes, error might appear because of encoding. In Vim, this can be solved with the command _set fileencoding=latin1_
