# -*- coding: utf-8 -*-

import re

import ckanapi

import datasets_pgi

# regular expression to catch group descriptions
description_re = re.compile(u'Descri\xe7\xe3o Grupo PGI: (.*)\(http://pgi.gov.br/pgi/\)')

# template text to transform into
target_template = \
u'''{}

**Atenção:** os dados das séries de indicadores são fornecidos por seu valor
histórico e não serão mais atualizados após dezembro/2014.

Fonte: [Plataforma de Gestão de Indicadores (PGI)](http://pgi.gov.br/pgi/)

## Sobre o PGI

A Plataforma de Gestão de Indicadores (PGI) foi uma ferramenta criada em 2010,
no âmbito do [projeto I3Gov](https://i3gov.planejamento.gov.br/), para agregar
séries de indicadores de gestão a partir de informações prestadas por diversos
órgãos federais.

Foi desativada no início de 2015 pela Casa Civil da Presidência da República,
entretanto, ficou estabelecido que o Ministério do Planejamento, Orçamento e
Gestão manteria disponíveis os dados históricos que haviam sido cadastrados
até dezembro de 2014.

Cada grupo de série histórica foi mapeada para um conjunto de dados e cada
série de indicadores foi mapeada para um recurso. Os dados são servidos nos
formatos XML e JSON pela API do PGI.
'''

# read datasets
pgi_reader = datasets_pgi.DatasetsPGI()
datasets_pgi = pgi_reader.datasets

for dataset in datasets_pgi[u'results']:
    found = description_re.match(dataset[u'notes'])
    if found and found.groups():
        print u'Ajustando descrição do conjunto de dados "{}"...'.format(dataset[u'title'])
        description = found.groups()[0]
        dataset[u'notes'] = target_template.format(description)
        pgi_reader.ckansite.action.package_update(**dataset)

