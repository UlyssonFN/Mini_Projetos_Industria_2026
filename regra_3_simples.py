#Cálculo de Proporção para demandas
# Aplicação: estimativas de demanda e apoio à análise de negócio

#Varíaveis para medição de proporção
#Principío da Regra de 3 Simples
# x1 = 2------------x1resultado = 400
# x2 = 4------------x2resultado = X
# Lógica de cálculo
# x=4*400
# x=1600
# x=1600/2
# x=800

def space():
    print("--------------------------------") 

def repeticao():
    resp = input("Deseja realizar uma nova consulta? s/n ")
    call = space()
    #condição    
    if resp == 's' or resp == 'S':
        return 1 
    else:
        print("Finalização do Programa")
        return 0

#Variável do loop
a = 1

while a ==1:
    #Tratativa de erro
    try:
        print("Sistema de cálculo de proporção (Regra de 3 diretamente Proporcional)")
        call = space()

        #Adicionando váriaveis de input para usuário
        x1 = float(input("Digite o valor grandeza x1: "))
        x1resultado = float(input("Digite o valor grandeza x1resultado: "))
        x2 = float(input("Digite o valor grandeza x2: "))

        #Cálculos de proporção
        x2resultado = x2*x1resultado
        predicao = round(x2resultado/x1,2)

        call = space()

        print("Lógica de Leitura")
        print("Se x1 = ", x1, "e resultado de x1resultado = :",x1resultado)
        print("E o valor de x2 é :", x2)
        print("Então x = ",x2,"*",x1resultado)
        print("Sendo o resultado de x = ",x2resultado)
        print("Onde x = ",x2resultado,"/",x1)
        print("Finalizando x = ",predicao)

        call = space()
        print("Lógica da Equação")
        print("x1 = ", x1," <------------> ",x1resultado)
        print("x2 = ", x2," <------------> x")

        call = space()
        print("Resolução")
        print("x = ",x2,"*",x1resultado)
        print("x = ",x2resultado)
        print("x = ",x2resultado,"/",x1)
        print("x = ",predicao)
        call = space()
        a = repeticao()

    #Tratativa de erro por divisão por zero
    except ZeroDivisionError:
        call = space()
        print("Não existe divisão por 0 !")
        call = space()
        a = repeticao()

    #Tratativa de erro por entrada de dados inválidos tipo string
    except Exception:
        call = space()
        print("Erro na inserção de dados")
        call = space()
        a = repeticao()
