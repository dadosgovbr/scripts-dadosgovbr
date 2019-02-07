**[DEPRECIADO]** Cadastra no portal dados.gov.br como recursos os arquivos de servidores
do poder executivo federal localizados no Portal da Transparência.

Este script não funciona mais como previsto porque após a reformulação do Portal
da Transparência em 2018, as URLs mudaram.

# Fonte dos dados

Portal da Transparência: http://www.transparencia.gov.br/downloads/servidores.asp

# Instruções de utilização

1. Colocar no diretorio a três níveis acima o arquivo
   `../../../api.key` contendo a sua chave da api do CKAN.
2. Executar o script

  `python cadastra_recurso_servidores.py ano mes civis_ou_militares`
  
  sendo:
  
  ano
    o ano desejado (ex. 2016)
  
  mes
    o mês desejado (ex. 1)
  
  civis_ou_militares
    C para o arquivo contendo os dados de servidores civis
    M para o arquivo contento os dados de servidores militares

## Dependências

  * [ckanapi](https://github.com/ckan/ckanapi)
  * [requests](http://docs.python-requests.org/en/master/)

