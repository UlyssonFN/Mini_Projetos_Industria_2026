#Lógica de cálculo de capacidade
 
def capacidade_volumetrica():
    print("Cálculo de capacidade")
    print("1 - Abrir Sistema")
    print("2 - Ajuda")
    reposta = int(input("Digite a opção desejada: "))
    #cubagem de endereço
    match(reposta):
        case 1:
            print("---------------Digite as dimensões do endereço(cm)---------------")
            qtd_endereco = int(input("Digite a quantidade de endereço: "))
            altura_end = float(input("Digite a altura endereço: "))
            largura_end = float(input("Digite a largura endereço: "))
            comprimento_end = float(input("Digite a comprimento endereço: "))
            empolamento = 0.06
            litrage_End = (altura_end*largura_end*comprimento_end)/1000
            cubagem_End = (litrage_End * qtd_endereco) - empolamento
            print("Litragem por endereço bin é: ",litrage_End,"L")
            print("Litragem geral do endereço é: ", cubagem_End,"L") 

            print("---------------Digite as dimensões do item(cm))- --------------")
            altura_sku = float(input("Digite a altura: "))
            largura_sku = float(input("Digite a largura: "))
            comprimento_sku = float(input("Digite a comprimento: "))
            empolamento = 0.06
            litrage_sku = ((altura_sku*largura_sku*comprimento_sku)/1000) - empolamento
            print("Litragem do item é: ",litrage_sku,"L")
            
            print("---------------Quantidade de Unidades p/Endereço)---------------")
            unidpend = cubagem_End/litrage_sku  
            print("No seu endereço atual, é possivel armazenar até: ",round(unidpend,0))
            print("---------------Fim de Operação---------------")  
    
        case 2:
            print("Cálculo de Capacidade - O cálculo consiste em comparar a cubagem do endereço fisico (recipiente) vs o endereço do produto, o intuito é encontrar a quantidade minima de unidades que irá alocar dentro do endereço, mediante a sua litragem.")
            print("Regra - Tamanho do endereço (Altura*Largura*Comprimento)/1000, Tamanho do item (Altura*Largura*Comprimento)/1000")
            print("Cálculo - Tamanho do endereço/Tamanho do item")
            print("Empolamento - É o aumento de um material quando ele é retirado do seu estado original e fica solto, como padrão desconsideramos 6%, não é regra, pode haver variações.")
            print("Resulta = (Tamnho do endereço/Tamanho do item)-6% do empolamento")
            
            
