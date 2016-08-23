# -*- coding: utf-8 -*-

import sys
import csv
import urlparse

import ckanapi

import dataset_operation

# maximum number of results to read
MAX_ROWS = 100

dataset_reader = dataset_operation.DatasetReader()

organization_map = {}

# read csv
with open ('dados/organization-map.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        organization_map[(
            row[u'author'].decode('utf-8'),
            row[u'maintainer'].decode('utf-8'),
            row[u'source hostname'].decode('utf-8')
            )] = row[u'organization url'].decode('utf-8')

# count results
dataset_reader.read(0,10)
dataset_count = dataset_reader.datasets[u'count']

# read dataset metadata from api
for offset in xrange(0, dataset_count, MAX_ROWS):
    print u'\rLendo datasets {}-{} de {}...'.format(offset+1,
        offset+MAX_ROWS if offset+MAX_ROWS < dataset_count else dataset_count,
        dataset_count),
    sys.stdout.flush()
    dataset_reader.read(offset,MAX_ROWS)
    for dataset in dataset_reader.datasets[u'results']:
        if not dataset.get(u'organization', None):
            domain = u''
            if dataset.get(u'url', None):
                url = urlparse.urlparse(dataset[u'url'])
                domain = url.hostname
            set_org = organization_map.get((
                dataset.get(u'author', u''),
                dataset.get(u'maintainer', u''),
                domain
                ), None)
            if set_org:
                org_name = urlparse.urlparse(set_org).path.split(u'/')[-1]
                print u'\nAssociando o dataset "{}" ({}) à organização "{}"...'.format(
                    dataset.get(u'name', u''),
                    dataset.get(u'title', u''),
                    org_name
                    )
                # get the organization id
                organization = dataset_reader.ckansite.action.organization_show(id=org_name)
                # set the owner organization on the package
                dataset_to_update = dataset_reader.ckansite.action.package_show(id=dataset[u'id'])
                dataset_to_update[u'owner_org'] = organization[u'id']
                dataset_reader.ckansite.action.package_update(**dataset_to_update)
                    
print u'\n{} datasets processados.'.format(dataset_count)

