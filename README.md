Scripts para fazer operações úteis no portal dados.gov.br.

# Instalação e uso

1. Clonar o repositório

`git clone https://github.com/dadosgovbr/scripts-dadosgovbr.git`

2. Para usar os scripts em Python, criar e ativar um [ambiente virtual](https://virtualenv.readthedocs.org/en/latest/)

```
cd scripts-dadosgovbr
virtualenv --no-site-packages pyenv
source pyenv/bin/activate
```

3. Instalar as dependências do script que deseja usar. Entre no diretório do script e use o comando

`pip install -r requirements.txt`

4. Consulte as instruções específicas no README.txt do script

# Estrutura

**scripts/importacao**: importam conjuntos de dados de outras fontes para o dados.gov.br (futuramente podem ser migrados para a interface de harvesting)

**scripts/extracao**: extraem dados do portal. Sugere-se colocar os dados extraídos na pasta 'dados', dentro da pasta do script.

**scripts/manutencao**: modificam dados do portal.

**api.key** coloque aqui a sua chave de acesso à API do CKAN. A chave está ná página do seu perfil de usuário no CKAN e é visível apenas quando logado.

