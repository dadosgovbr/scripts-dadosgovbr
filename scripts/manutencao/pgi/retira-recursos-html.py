# -*- coding: utf-8 -*-

import ckanapi

import datasets_pgi

# ask for confirmation
answer = raw_input(u'Este script apaga todos os recursos com o formato HTML em todos os datasets que tenham a tag "PGI". Tem certeza? (s/n) ')
if not answer.strip().lower() == u's':
    print u'Operação cancelada.'
    import sys
    sys.exit(2)

# read datasets
pgi_reader = datasets_pgi.DatasetsPGI()
datasets_pgi = pgi_reader.datasets

for dataset in datasets_pgi[u'results']:
    for resource in dataset[u'resources']:
        if resource[u'format']==u'HTML':
            print u'Excluindo o recurso "{}" do conjunto de dados "{}"...'.format(resource[u'name'], dataset[u'title'])
            pgi_reader.ckansite.action.resource_delete(id=resource[u'id'])

