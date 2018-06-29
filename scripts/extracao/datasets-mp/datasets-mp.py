# -*- coding: utf-8 -*-

from ckanapi import RemoteCKAN

ua = 'scriptDatasetsMP/0.1'

portal = RemoteCKAN('http://dados.gov.br', user_agent=ua)

datasets = portal.action.package_search(fq='organization:ministerio-do-planejamento-desenvolvimento-e-gestao-mp', rows=1000)

# expressao regular para usar, e.g., no Google Analytics
regex = "(?:" + ("|".join([r['name'] + "/?" for r in datasets['results']])) + ")"

# escrever um por linha
print ("\n".join([r['name'] for r in datasets['results']]))

