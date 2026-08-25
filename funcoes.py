#funcoes
import calculo_area_perimetro

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

def pringeometria():
    print("Sua área é: ",area)
    print("Seu perímetro é: ",perimetro)