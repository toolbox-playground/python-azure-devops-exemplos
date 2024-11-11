import requests
from requests.auth import HTTPBasicAuth

# Configurações do Azure DevOps
organization = "<NOME_DA_SUA_ORGANIZACAO>"
project = "<NOME_DO_SEU_PROJETO>"
library_id = "<ID_ADO_LIBRARY>"  # ID da Biblioteca onde estão as variáveis
pat_token = "<SEU_PAT_TOKEN_AQUI>"

# URL da API para acessar as variáveis da biblioteca
url = f"https://dev.azure.com/{organization}/{project}/_apis/distributedtask/variablegroups/{library_id}?api-version=7.1-preview.2"

# Realiza a requisição GET para ler as variáveis
response = requests.get(url, auth=HTTPBasicAuth('', pat_token))

if response.status_code == 200:
    variables = response.json().get("variables", {})
    for var_name, var_info in variables.items():
        print(f"Variável: {var_name}, Valor: {var_info.get('value')}") # Se sucesso, printa todas as variáveis
else:
    print(f"Erro ao obter as variáveis: {response.status_code} - {response.text}")
