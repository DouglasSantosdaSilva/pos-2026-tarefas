import json

with open("imobiliaria.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

imoveis = dados["imobiliaria"]["imoveis"]

print("=== SISTEMA DA IMOBILIÁRIA - IMÓVEIS DISPONÍVEIS ===")
for imovel in imoveis:
    print(f"ID: {imovel['id']} - {imovel['descricao']}")

try:
    escolha = int(input("\nDigite o ID do imóvel para ver detalhes: "))

    encontrado = False
    for imovel in imoveis:
        if imovel["id"] == escolha:
            encontrado = True
            print("\n" + "="*40)
            print(f"DETALHES DO IMÓVEL #{imovel['id']}")
            print(f"Descrição: {imovel['descricao']}")
            print(f"Valor: R$ {imovel['valor']:,.2f}")
            
            print("\nPROPRIETÁRIO:")
            print(f"  Nome: {imovel['proprietario']['nome']}")
            if "telefones" in imovel["proprietario"]:
                print(f"  Telefones: {', '.join(imovel['proprietario']['telefones'])}")
            if "email" in imovel["proprietario"]:
                print(f"  E-mail: {imovel['proprietario']['email']}")

            print("\nENDEREÇO:")
            end = imovel["endereco"]
            num = end["numero"] if "numero" in end else "S/N"
            print(f"  {end['rua']}, {num}")
            print(f"  Bairro: {end['bairro']} - {end['cidade']}")

            print("\nCARACTERÍSTICAS:")
            carac = imovel["caracteristicas"]
            print(f"  Tamanho: {carac['tamanho']}m²")
            print(f"  Quartos: {carac['numQuartos']} | Banheiros: {carac['numBanheiros']}")
            print("="*40)
            break

    if not encontrado:
        print("\n[!] Imóvel com ID informado não foi encontrado.")

except ValueError:
    print("\n[!] Por favor, digite um número válido para o ID.")