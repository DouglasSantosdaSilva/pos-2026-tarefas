import users_wrapper as users

executando = True
while executando:
    menu = "1 - Listar usuários\n2 - Ler usuário\n3 - Criar usuário\n4 - Atualizar usuário\n5 - Excluir usuário\n6 - Sair\nEscolha uma opção: "
    opcao = input(menu)
    
    if opcao == "1":
        print("--- Usuários Cadastrados ---")
        lista_usuarios = users.list()
        if lista_usuarios:
            for usuario in lista_usuarios:
                print(f"ID: {usuario['id']} | Nome: {usuario['name']}")
        else:
            print("Não foi possível carregar a lista.")
        print("-" * 30)

    if opcao == "2":
        id_busca = input("Digite o ID do usuário que deseja consultar: ")
        usuario = users.read(id_busca)
        if usuario:
            print(f"[Dados do Usuário {id_busca}]")
            print(f"Nome: {usuario['name']}")
            print(f"Email: {usuario['email']}")
        else:
            print("Usuário não encontrado.")
        print("-" * 30)

    if opcao == "3":
        print("--- Cadastrar Novo Usuário ---")
        nome_novo = input("Nome: ")
        email_novo = input("Email: ")
        
        dados_novos = {"name": nome_novo, "email": email_novo}
        retorno_criacao = users.create(dados_novos)
        
        if retorno_criacao:
            print(f"Sucesso! Novo usuário criado com o ID: {retorno_criacao['id']}")
        else:
            print("Falha ao criar o usuário.")
        print("-" * 30)

    if opcao == "4":
        print("--- Atualizar Dados do Usuário ---")
        id_atualizar = input("Digite o ID do usuário: ")
        nome_alt = input("Novo Nome: ")
        email_alt = input("Novo Email: ")
        
        dados_atualizados = {"name": nome_alt, "email": email_alt}
        retorno = users.update(id_atualizar, dados_atualizados)
        
        if retorno:
            print("Os dados foram atualizados com sucesso!")
        else:
            print("Erro ao atualizar os dados na API.")
        print("-" * 30)

    if opcao == "5":
        id_excluir = input("Digite o ID do usuário para exclusão: ")
        removido = users.delete(id_excluir)
        if removido:
            print(f"Usuário {id_excluir} removido com sucesso!")
        else:
            print("Erro ao tentar remover o usuário.")
        print("-" * 30)

    if opcao == "6":
        print("Encerrando a aplicação CLI. Até mais!")
        executando = False