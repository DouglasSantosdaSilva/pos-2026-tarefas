import requests
from getpass import getpass
from tabulate import tabulate

# URL base da API do SUAP
api_url = "https://suap.ifrn.edu.br/api/"

# 1. Coleta de dados do usuário
user = input("Digite a matrícula do aluno: ")
password = getpass("Digite a senha: ")

aluno = {"username": user, "password": password}

print("\nTentando autenticar no SUAP...")
# 2. Faz a requisição de login
response = requests.post(api_url + "v2/autenticacao/token/", json=aluno)

# Verifica se o login deu certo antes de tentar pegar o token
if response.status_code != 200:
    print("\n Erro na autenticação!")
    print("Verifique se sua matrícula e senha estão corretas e tente novamente.")
    exit()

# Se o login deu certo, pega o token com segurança
token = response.json()["access"]

headers = {
    "Authorization": f'Bearer {token}'
}

# 3. Busca do Boletim
ano = input("\nDigite o ano do boletim que deseja visualizar (ex: 2025): ")
periodo = input("Digite o período (1 ou 2): ")

print("Buscando notas...")
url_boletim = f"{api_url}ensino/meu-boletim/{ano}/{periodo}/"
response = requests.get(url_boletim, headers=headers)

if response.status_code != 200:
    print("\n 2022Erro ao buscar o boletim.")
    print("Verifique se o ano e o período digitados existem.")
    exit()

boletim = response.json()

# 4. Montagem da Tabela
tabela = []

for disciplina in boletim:
    # Remove o código da disciplina do nome para a tabela ficar mais limpa
    nome_completo = disciplina.get("disciplina", "—")
    nome = nome_completo.split(" - ")[-1] if " - " in nome_completo else nome_completo
    
    # Coleta as notas de forma segura
    nota_1 = disciplina.get("nota_etapa_1", {}).get("nota", "—")
    nota_2 = disciplina.get("nota_etapa_2", {}).get("nota", "—")
    nota_3 = disciplina.get("nota_etapa_3", {}).get("nota", "—")
    nota_4 = disciplina.get("nota_etapa_4", {}).get("nota", "—")
    media = disciplina.get("media_final_disciplina", "—")
    
    tabela.append([nome, nota_1, nota_2, nota_3, nota_4, media])

# Cabeçalho da tabela
cabecalho = ["Disciplina", "Nota 1", "Nota 2", "Nota 3", "Nota 4", "Média"]

# Exibe o resultado formatado
print("\n" + tabulate(tabela, headers=cabecalho, tablefmt="grid"))