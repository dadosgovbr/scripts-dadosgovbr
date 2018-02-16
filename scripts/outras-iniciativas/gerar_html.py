#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from io import StringIO
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
        states[row['Sigla']] = {
            'nome': row['Nome'],
            'ativo': False
            }

# get list of data catalogs

csv_url = 'https://github.com/dadosgovbr/catalogos-dados-brasil/raw/master/dados/catalogos.csv'

catalogs = []

r = requests.get(csv_url)

if r.status_code != 200:
    raise IOError('Cannot download data catalogs table from Github repository.')

reader = csv.DictReader(StringIO(r.text))

for row in reader:
    catalogs.append(row)

# check which states have catalogs

for catalog in catalogs:
    if catalog['UF'] in list(states.keys()):
        states[catalog['UF']]['ativo'] = True

# generate area activation script

filein = 'activate_areas.js'

with open(filein) as f:
    activate_script_template = Template(f.read())

habilitados_dict = {}

for state in list(states.keys()):
    if states[state]['ativo']:
        habilitados_dict[states[state]['nome']] = '1'

activate_areas_script = activate_script_template.substitute({'habilitados_dict': json.dumps(habilitados_dict)})

# generate map colors

filein = 'mapa.svg'

ns = {'svg': 'http://www.w3.org/2000/svg'}
ElementTree.register_namespace('', 'http://www.w3.org/2000/svg')

tree = ElementTree.parse(filein)

for a in tree.findall('svg:g[@id="Estados"]/svg:a', ns):
    state = a.get('data-target')[-2:]
    path = a.find('svg:path', ns)
    if states[state]['ativo']:
        xml_class = path.get('class').replace(' inactive','')
        xml_class += ' active'
        path.set('class', xml_class)

map_svg = ElementTree.tostring(tree.getroot()).decode()

# generate modals

filein = 'modal_template.html'

with open(filein) as f:
    modal_template = Template(f.read())

filein = 'catalog_template.html'

with open(filein) as f:
    catalog_template = Template(f.read())

modal_section = ''

for state in sorted(states.keys()):
    if states[state]['ativo']:
        modal_html = ''
        catalog_list = ''
        municipal_catalogs = {}
        
        for catalog in catalogs:
            if catalog['UF'] == state:
                catalog_type = ''
                if catalog['Solução'] == 'CKAN':
                    catalog_type = '<img src="/wp/wp-content/uploads/2017/12/ckan-logo.png" />'
                # add state catalogs
                if not catalog['Município']:
                    catalog_list += catalog_template.substitute({
                        'catalog_title': catalog['Título'],
                        'catalog_url': catalog['URL'],
                        'catalog_type': catalog_type,
                        })
                else:
                    catalogs_in_this_municipality = municipal_catalogs.setdefault(catalog['Município'], [])
                    catalogs_in_this_municipality.append(catalog)
        
        # add municipal catalogs
        for municipality, municipal_catalogs in list(municipal_catalogs.items()):
            municipality_html = '<h4>{}</h4>'.format(municipality)
            municipality_html += "<dl>"
            for catalog in municipal_catalogs:
                catalog_type = ''
                if catalog['Solução'] == 'CKAN':
                    catalog_type = '<img src="/wp/wp-content/uploads/2017/12/ckan-logo.png" />'
                municipality_html += catalog_template.substitute({
                    'catalog_title': catalog['Título'],
                    'catalog_url': catalog['URL'],
                    'catalog_type': catalog_type,
                    })
            municipality_html += "</dl>"
            catalog_list += municipality_html
        
        modal_html = modal_template.substitute({
            'state_abbr': state,
            'state_name': states[state]['nome'],
            'catalog_list': catalog_list
            })
        modal_section += modal_html

# national catalogs

catalog_list = ''
for catalog in catalogs:
    if not catalog['UF']:
        catalog_type = ''
        if catalog['Solução'] == 'CKAN':
            catalog_type = '<img src="/wp/wp-content/uploads/2017/12/ckan-logo.png" />'
        catalog_list += catalog_template.substitute({
            'catalog_title': catalog['Título'],
            'catalog_url': catalog['URL'],
            'catalog_type': catalog_type,
            })
modal_section += modal_template.substitute({
            'state_abbr': 'BR',
            'state_name': 'Nacionais',
            'catalog_list': catalog_list
            })

# generate page

filein = 'template-pagina.html'

with open(filein) as f:
    page_template = Template(f.read())

page_html = page_template.substitute({
    'activate_areas_script': activate_areas_script,
    'map_svg': map_svg,
    'modal_section': modal_section
    })

fileout = 'outras-iniciativas.html'

with open(fileout, 'w') as f:
    f.write(page_html)

