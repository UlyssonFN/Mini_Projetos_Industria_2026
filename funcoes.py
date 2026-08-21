#funcoes
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