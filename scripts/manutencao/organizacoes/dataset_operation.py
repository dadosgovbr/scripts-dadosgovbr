# -*- coding: utf-8 -*-

import ckanapi

class DatasetReader(object):
    
    ckan_url = u"http://dados.gov.br"
    api_key = u""
    datasets = None
    
    def __init__(self):
        self.read_api_key()
        self.ckansite = ckanapi.RemoteCKAN(self.ckan_url, apikey=self.api_key)
    
    def read_api_key(self):
        try:
            with open("../../../api.key","r") as f:
                self.api_key=f.readline().strip()
        except IOError:
            raise Exception(u"Uma chave de API no arquivo api.key é necessária para a operação.")
    
    def read(self, start=0, rows=10):
        self.datasets = self.ckansite.action.dataset_search(q=u"state:active",rows=rows,start=start)

