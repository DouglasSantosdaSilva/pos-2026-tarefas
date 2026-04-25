import json
from xml.dom.minidom import parse

dom = parse("imobiliaria.xml")
imoveis_xml = dom.getElementsByTagName("imovel")

lista_imoveis = []

for i, node in enumerate(imoveis_xml, start=1):
    descricao = node.getElementsByTagName("descricao")[0].firstChild.nodeValue
    valor = int(node.getElementsByTagName("valor")[0].firstChild.nodeValue)

    prop_node = node.getElementsByTagName("proprietario")[0]
    nome_prop = prop_node.getElementsByTagName("nome")[0].firstChild.nodeValue
    
    telefones = []
    for tel in prop_node.getElementsByTagName("telefone"):
        telefones.append(tel.firstChild.nodeValue)

    end_node = node.getElementsByTagName("endereco")[0]
    rua = end_node.getElementsByTagName("rua")[0].firstChild.nodeValue
    bairro = end_node.getElementsByTagName("bairro")[0].firstChild.nodeValue
    cidade = end_node.getElementsByTagName("cidade")[0].firstChild.nodeValue

    carac_node = node.getElementsByTagName("caracteristicas")[0]
    tamanho_texto = carac_node.getElementsByTagName("tamanho")[0].firstChild.nodeValue
    tamanho = int(tamanho_texto.replace('m', ''))
    quartos = int(carac_node.getElementsByTagName("numQuartos")[0].firstChild.nodeValue)
    banheiros = int(carac_node.getElementsByTagName("numBanheiros")[0].firstChild.nodeValue)

    imovel_dict = {
        "id": i,
        "descricao": descricao,
        "proprietario": {
            "nome": nome_prop,
            "telefones": telefones
        },
        "endereco": {
            "rua": rua,
            "bairro": bairro,
            "cidade": cidade
        },
        "caracteristicas": {
            "tamanho": tamanho,
            "numQuartos": quartos,
            "numBanheiros": banheiros
        },
        "valor": valor
    }
    
    lista_imoveis.append(imovel_dict)

resultado = {
    "imobiliaria": {
        "imoveis": lista_imoveis
    }
}

with open("imobiliaria.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Arquivo imobiliaria.json criado com sucesso!")