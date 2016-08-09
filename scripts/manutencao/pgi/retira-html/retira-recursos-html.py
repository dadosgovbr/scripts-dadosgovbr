# -*- coding: utf-8 -*-

import ckanapi

ckan_url = u"http://dados.gov.br"
api_key = u""

# ask for confirmation

answer = raw_input(u'Este script apaga todos os recursos com o formato HTML em todos os datasets que tenham a tag "PGI". Tem certeza? (s/n) ')
if not answer.strip().lower() == u's':
    print u'Operação cancelada.'
    import sys
    sys.exit(2)

# read api key
try:
    with open("../../../../api.key","r") as f:
        api_key=f.readline().strip()
except IOError:
    raise Exception(u"Uma chave de API no arquivo api.key é necessária para a operação.")

ckansite = ckanapi.RemoteCKAN(ckan_url, apikey=api_key)

datasets_pgi = ckansite.action.dataset_search(q=u"tags:PGI state:active",rows=180)

for dataset in datasets_pgi[u'results']:
    for resource in dataset[u'resources']:
        if resource[u'format']==u'HTML':
            print u'Excluindo o recurso "{}" do conjunto de dados "{}"...'.format(resource[u'name'], dataset[u'title'])
            ckansite.action.resource_delete(id=resource[u'id'])

