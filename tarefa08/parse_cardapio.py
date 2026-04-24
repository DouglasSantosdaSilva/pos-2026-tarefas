from xml.dom.minidom import parse

dom = parse("cardapio.xml")   

cardapio = dom.documentElement

pratos = cardapio.getElementsByTagName("prato")

for prato in pratos:
    nome = prato.getAttribute('nome')
    

