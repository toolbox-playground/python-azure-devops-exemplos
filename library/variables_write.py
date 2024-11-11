import requests
from requests.auth import HTTPBasicAuth

# Configurações do Azure DevOps
organization = "<NOME_DA_SUA_ORGANIZACAO>"
project_name = "<NOME_DO_SEU_PROJETO>"
library_id = "<ID_ADO_LIBRARY>"  # ID da Biblioteca onde estão as variáveis
pat_token = "<SEU_PAT_TOKEN_AQUI>"

# Variável que você deseja definir/atualizar
nome_variavel = "DEBUG"
valor_variavel = "DEPOIS DA MUDANÇA"

# Obter o ID do projeto a partir do nome do projeto
project_url = f"https://dev.azure.com/{organization}/_apis/projects/{project_name}?api-version=6.0"
project_response = requests.get(project_url, auth=HTTPBasicAuth('', pat_token))

print(f"Project Status Code: {project_response.status_code}")
print(f"Project Response Text: {project_response.text}")

if project_response.status_code == 200:
    project_data = project_response.json()
    project_id = project_data['id']
else:
    print(f"Erro ao obter o ID do projeto: {project_response.status_code} - {project_response.text}")
    exit()

# URL da API para atualizar o grupo de variáveis (inclui o nome do projeto)
url = f"https://dev.azure.com/{organization}/{project_name}/_apis/distributedtask/variablegroups/{library_id}?api-version=7.1-preview.2"

# Requisição atual para obter as variáveis existentes
response = requests.get(url, auth=HTTPBasicAuth('', pat_token))

print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

if response.status_code == 200:
    # Obter os dados atuais do grupo de variáveis
    library_data = response.json()
    print(f"Library Data: {library_data}")

    variables = library_data.get("variables", {})

    # Atualizar ou adicionar a nova variável
    variables[nome_variavel] = {"value": valor_variavel}

    # Atualizar os dados do grupo de variáveis
    library_data['variables'] = variables

    # Atualizar o campo variableGroupProjectReferences com o ID do projeto
    library_data['variableGroupProjectReferences'] = [
        {
            "projectReference": {
                "id": project_id
            },
            "name": library_data["name"]
        }
    ]

    # Enviar a atualização
    update_response = requests.put(
        url,
        auth=HTTPBasicAuth('', pat_token),
        json=library_data
    )

    print(f"Update Status Code: {update_response.status_code}")
    print(f"Update Response Text: {update_response.text}")

    if update_response.status_code == 200:
        print(f"Variável '{nome_variavel}' atualizada com sucesso.")
    else:
        print(f"Erro ao atualizar a variável: {update_response.status_code} - {update_response.text}")
else:
    print(f"Erro ao obter a biblioteca: {response.status_code} - {response.text}")
