# -*- coding: utf-8 -*-

import csv
from ckanapi import RemoteCKAN

dadosgovbr = RemoteCKAN('http://dados.gov.br')

orgaos_quantidades = [(orgao['display_name'], orgao['package_count']) for orgao in dadosgovbr.action.organization_list(all_fields=True)]

with open('orgaos.csv', 'w') as f:
    planilha = csv.writer(f)
    planilha.writerow(('órgão', 'quantidade'))
    for linha in orgaos_quantidades:
        planilha.writerow(linha)

