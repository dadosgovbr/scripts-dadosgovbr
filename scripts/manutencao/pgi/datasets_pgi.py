# -*- coding: utf-8 -*-

import ckanapi

# maximum number of results to read
MAX_ROWS = 200

class DatasetsPGI(object):
    
    ckan_url = u"http://dados.gov.br"
    api_key = u""
    
    def __init__(self):
        self.read_api_key()
        self.ckansite = ckanapi.RemoteCKAN(self.ckan_url, apikey=self.api_key)
        self.datasets = self.ckansite.action.dataset_search(q=u"tags:PGI state:active",rows=MAX_ROWS)
        
    def read_api_key(self):
        try:
            with open("../../../api.key","r") as f:
                self.api_key=f.readline().strip()
        except IOError:
            raise Exception(u"Uma chave de API no arquivo api.key é necessária para a operação.")
    
