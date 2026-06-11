import zeep

# define a URL do WSDL
wsdl_url = "http://www.dataaccess.com/webservicesserver/NumberConversion.wso?WSDL"

# inicializa o cliente zeep
client = zeep.Client(wsdl=wsdl_url)

numero = int(input("digite um numero inteiro: "))
# faz a chamada do serviço
result = client.service.NumberToWords(
    ubiNum = numero

)

print(result)