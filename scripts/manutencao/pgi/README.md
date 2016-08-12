Conjunto de scripts para trabalhar com os conjuntos de dados do PGI no portal
dados.gov.br.

# O que é o PGI?

A [Plataforma de Gestão de Indicadores (PGI)](http://pgi.gov.br/pgi/) foi uma
ferramenta criada em 2010, no âmbito do
[projeto I3Gov](https://i3gov.planejamento.gov.br/), para agregar séries de
indicadores de gestão a partir de informações prestadas por diversos órgãos
federais.

Foi desativada no início de 2015 pela Casa Civil da Presidência da República,
entretanto, ficou estabelecido que o Ministério do Planejamento, Orçamento e
Gestão manteria disponíveis os dados históricos que haviam sido cadastrados
até dezembro de 2014.

Cada grupo de série histórica foi mapeada para um conjunto de dados e cada
série de indicadores foi mapeada para um recurso. Os dados são servidos nos
formatos XML e JSON pela API do PGI.

# Scripts

## retira-recursos-html.py

Retira os recursos em formato html dos conjuntos de dados do PGI.

Os recursos em html eram links para páginas no PGI que apresentavam
visualmente a série histórica. Com a desativação da plataforma, essas
visualizações não estão mais disponíveis. Todavia, permanecem os dados
disponíveis nos demais formatos (XML e JSON).

## ajuste-descricao.py

Ajusta a descrição dos conjuntos de dados do PGI.
