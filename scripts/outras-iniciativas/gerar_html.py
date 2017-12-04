#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from StringIO import StringIO
from string import Template
import requests
import json
from xml.etree import ElementTree

# get Brazilian states

filein = 'unidades-federativas.csv'

states = {}

with open(filein) as f:
    reader = csv.DictReader(f)
    for row in reader:
        states[row[u'Sigla']] = {
            u'nome': row[u'Nome'].decode('utf-8'),
            u'ativo': False
            }

# get list of data catalogs

csv_url = 'https://github.com/dadosgovbr/catalogos-dados-brasil/raw/master/dados/catalogos.csv'

catalogs = []

r = requests.get(csv_url)

if r.status_code != 200:
    raise IOError(u'Cannot download data catalogs table from Github repository.')

reader = csv.DictReader(StringIO(r.text.encode('utf-8')))

for row in reader:
    catalogs.append(row)

# check which states have catalogs

for catalog in catalogs:
    if catalog[u'UF'] in states.keys():
        states[catalog[u'UF']][u'ativo'] = True

# generate area activation script

filein = 'activate_areas.js'

with open(filein) as f:
    activate_script_template = Template(f.read())

habilitados_dict = {}

for state in states.keys():
    if states[state][u'ativo']:
        habilitados_dict[states[state][u'nome']] = '1'

activate_areas_script = activate_script_template.substitute({u'habilitados_dict': json.dumps(habilitados_dict)})

# generate map colors

filein = 'mapa.svg'

ns = {'svg': 'http://www.w3.org/2000/svg'}
ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')

tree = ElementTree.parse(filein)

for a in tree.findall('svg:g[@id="Estados"]/svg:a', ns):
    state = a.get('data-target')[-2:]
    path = a.find('svg:path', ns)
    if states[state][u'ativo']:
        xml_class = path.get('class').replace(' inactive','')
        xml_class += ' active'
        path.set('class', xml_class)

map_svg = ElementTree.tostring(tree.getroot()).decode('utf-8')

# generate modals

filein = 'modal_template.html'

with open(filein) as f:
    modal_template = Template(f.read())

filein = 'catalog_template.html'

with open(filein) as f:
    catalog_template = Template(f.read())

modal_section = u''

for state in sorted(states.keys()):
    if states[state][u'ativo']:
        modal_html = u''
        catalog_list = u''
        municipal_catalogs = {}
        
        for catalog in catalogs:
            if catalog[u'UF'] == state:
                catalog_type = u''
                if catalog[u'Solução'.encode('utf-8')] == u'CKAN':
                    catalog_type = u'<img src="/wp/wp-content/uploads/2017/12/ckan-logo.png" />'
                # add state catalogs
                if not catalog[u'Município'.encode('utf-8')]:
                    catalog_list += catalog_template.substitute({
                        u'catalog_title': catalog[u'Título'.encode('utf-8')].decode('utf-8'),
                        u'catalog_url': catalog[u'URL'],
                        u'catalog_type': catalog_type,
                        })
                else:
                    catalogs_in_this_municipality = municipal_catalogs.setdefault(catalog[u'Município'.encode('utf-8')], [])
                    catalogs_in_this_municipality.append(catalog)
        
        # add municipal catalogs
        for municipality, municipal_catalogs in municipal_catalogs.items():
            municipality_html = u'<h4>{}</h4>'.format(municipality.decode('utf-8'))
            municipality_html += "<dl>"
            for catalog in municipal_catalogs:
                catalog_type = u''
                if catalog[u'Solução'.encode('utf-8')] == u'CKAN':
                    catalog_type = u'<img src="/wp/wp-content/uploads/2017/12/ckan-logo.png" />'
                municipality_html += catalog_template.substitute({
                    u'catalog_title': catalog[u'Título'.encode('utf-8')].decode('utf-8'),
                    u'catalog_url': catalog[u'URL'],
                    u'catalog_type': catalog_type,
                    })
            municipality_html += "</dl>"
            catalog_list += municipality_html
        
        modal_html = modal_template.substitute({
            u'state_abbr': state,
            u'state_name': states[state][u'nome'],
            u'catalog_list': catalog_list
            })
        modal_section += modal_html

# generate page

filein = 'template-pagina.html'

with open(filein) as f:
    page_template = Template(f.read())

page_html = page_template.substitute({
    u'activate_areas_script': activate_areas_script,
    u'map_svg': map_svg,
    u'modal_section': modal_section
    })

fileout = 'outras-iniciativas.html'

with open(fileout, 'w') as f:
    f.write(page_html.encode('utf-8'))

