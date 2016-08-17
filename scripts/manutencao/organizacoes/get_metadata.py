# -*- coding: utf-8 -*-

import sys
import csv
import urlparse

import dataset_operation

# maximum number of results to read
MAX_ROWS = 100

dataset_reader = dataset_operation.DatasetReader()

# count results
dataset_reader.read(0,10)
dataset_count = dataset_reader.datasets[u'count']

# read dataset metadata from api
datasets = []
for offset in xrange(0, dataset_count, MAX_ROWS):
    print u'\rLendo datasets {}-{} de {}...'.format(offset+1,
        offset+MAX_ROWS if offset+MAX_ROWS < dataset_count else dataset_count,
        dataset_count),
    sys.stdout.flush()
    dataset_reader.read(offset,MAX_ROWS)
    datasets.extend(dataset_reader.datasets[u'results'])
print u'\n{} datasets lidos.'.format(len(datasets))

metadata = set()

for dataset in datasets:
    author = dataset.get(u'author', u'')
    maintainer = dataset.get(u'maintainer', u'')
    domain = u''
    if dataset.get(u'url', None):
        url = urlparse.urlparse(dataset[u'url'])
        domain = url.hostname
    organization_url = u''
    if dataset.get(u'organization', None):
        organization_url = u'http://dados.gov.br/organization/{}'.format(
            dataset[u'organization'][u'name'])
    metadata.add((
        author.encode('utf-8') if author else u'',
        maintainer.encode('utf-8') if maintainer else u'',
        domain,
        organization_url if organization_url else u''
        ))
print u'{} combinações encontradas.'.format(len(metadata))


with open ('dados/organization-map.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('author', 'maintainer', 'source hostname', 'organization url'))
    for fieldset in metadata:
        writer.writerow(fieldset)

