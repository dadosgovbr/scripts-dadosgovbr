# -*- coding: utf-8 -*-

import ckanapi

import datasets_pgi

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

pgi_reader = datasets_pgi.DatasetsPGI()
datasets_pgi = pgi_reader.datasets

for dataset in datasets_pgi[u'results']:
    pass
