# -*- coding: utf-8 -*-

import csv
from ckanapi import RemoteCKAN

dadosgovbr = RemoteCKAN('http://dados.gov.br')

orgaos_quantidades = [
    (
        orgao['display_name'],
        ([extra['value'] for extra in orgao['extras'] if extra['key'] == 'siorg'][:1] or [''])[0],
        orgao['package_count']
    ) for orgao in dadosgovbr.action.organization_list(all_fields=True, include_extras=True) \
        if orgao['state'] == 'active']

with open('orgaos.csv', 'w') as f:
    planilha = csv.writer(f)
    planilha.writerow(('órgão', 'siorg', 'quantidade'))
    for linha in orgaos_quantidades:
        planilha.writerow(linha)

