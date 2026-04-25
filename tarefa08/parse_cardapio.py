from xml.dom.minidom import parse

dom = parse("cardapio.xml")
cardapio = dom.documentElement
pratos = cardapio.getElementsByTagName("prato")

print("=== MENU DE PRATOS ===")
for prato in pratos:
    id_prato = prato.getAttribute("id")
    nome = prato.getElementsByTagName("nome")[0].firstChild.nodeValue
    print(f"{id_prato} - {nome}")

escolha = input("Digite o ID do prato para saber mais detalhes: ")

encontrou = False
for prato in pratos:
    if prato.getAttribute("id") == escolha:
        encontrou = True
        nome = prato.getElementsByTagName("nome")[0].firstChild.nodeValue
        desc = prato.getElementsByTagName("descricao")[0].firstChild.nodeValue
        preco = prato.getElementsByTagName("preco")[0].firstChild.nodeValue
        calorias = prato.getElementsByTagName("calorias")[0].firstChild.nodeValue
        tempo = prato.getElementsByTagName("tempoPreparo")[0].firstChild.nodeValue

        print(f"--- Detalhes do prato {escolha} ---")
        print(f"Nome: {nome}")
        print(f"Descrição: {desc}")
        print(f"Preço: R$ {preco}")
        print(f"Calorias: {calorias}")
        print(f"Tempo de Preparo: {tempo}")
        
        print("Ingredientes:")
        ingredientes = prato.getElementsByTagName("ingrediente")
        for ing in ingredientes:
            print(f"  - {ing.firstChild.nodeValue}")

if not encontrou:
    print("[!] Prato não encontrado.")