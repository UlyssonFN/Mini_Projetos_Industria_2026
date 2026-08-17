#Cálculo de HC(Pessoas) Separação e Conferência
#Esse código consiste em realizar a medição de pessoas com base no faturamento em unidades, meta produtiva e horas trabalhas, o mesmo retorna o quantitativo de pessoas mediante a conta exata.

#Função do espaço
def space():
    print("--------------------------------") 

def repeticao():
    resp = input("Deseja realizar uma nova consulta? s/n ")
    call = space()
    #condição    
    if resp == 's' or resp == 'S':
        return 1 
    else:
        return 0     
    
#Variável do loop
a = 1
while a == 1:
    print("Sistema de Verificação de Produtividade Necessária")
    #chamada do espaço
    call = space()
    #Variáveis Operacionais
    try:
        unid_faturamento = int(input("Digite a Unid/Faturamento: "))
        hora_trabalhada = float(input("Digite a hora trabalhada: "))
        meta_conf = int(input("Digite a meta de conferência por hora: "))
        meta_sep = int(input("Digite a meta de separação por hora: "))  
        #chamada do espaço
        call = space()
        #Calculo das variáveis
        qtd_hcC = unid_faturamento/hora_trabalhada/meta_conf
        qtd_hcS = unid_faturamento/hora_trabalhada/meta_sep
        #Mostra os resultados
        print("Quantidade de Pessoas Necessárias para Conferência é: ", round(qtd_hcC,1))
        print("Quantidade de Pessoas Necessárias para Separação é: ", round(qtd_hcS,1))
        #chamada do espaço
        call = space
        a = repeticao()
    except Exception:
        call = space()
        print("Erro ao digitar valores")
        print("Observações: ")
        print("1 - Não digitar textos nas variáveis: ")
        print("2 - Ao tentar usar ','(virgula) utilizar '.'(ponto)")
        call = space()    
        #Variável que dará inicio ao loop
        a = repeticao()