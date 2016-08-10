Conjunto de scripts para trabalhar com os conjuntos de dados do PGI no portal
dados.gov.br.

# O que é o PGI?

A Plataforma de Gestão de Indicadores (PGI) foi uma ferramenta para agregar
indicadores de gestão do governo federal a partir de informações prestadas de
diversos ministérios. Foi desativada no início de 2015 pela Casa Civil, e
estão disponíveis apenas os dados históricos que haviam sido informados até
dezembro de 2014.

# Scripts

## retira-recursos-html.py

Retira os recursos em formato html dos conjuntos de dados do PGI.

Os recursos em html eram links para páginas no PGI que apresentavam
visualmente a série histórica. Com a desativação da plataforma, essas
visualizações não estão mais disponíveis. Todavia, permanecem os dados
disponíveis nos demais formatos (XML e JSON).

## ajuste-descricao.py

Ajusta a descrição dos conjuntos de dados do PGI.
