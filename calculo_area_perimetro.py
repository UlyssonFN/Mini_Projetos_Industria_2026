#Cálculo de Perímetros e Área de Figuras
#from funcoes import pringeometria, space, repeticao


print("Escolha a figura: ")
print("1 - Retângulo")
print("2 - Quadrado")  
print("3 - Paralelogramo")
print("4 - Triangulo")
print("5 - Losango ou rombo")
print("6 - Trapézio")
print("7 - Circulo")
try:
    interacao = int(input("Responda: "))
    if interacao > 7:
                print("Opção inválida")
    else:
        match(interacao):
            case 1: #Retângulo
                base = float(input("Digite e base: "))
                altura = float(input("Digite a altura: "))
                area = base * altura
                perimetro = (2*base)+(2*altura)
                print("Sua área é: ",area)
                print("Seu perímetro é: ",perimetro)
            case 2: #Quadrado
                lado = float(input("Digite o valor do lado: "))
                area = lado**2
                perimetro = 4*lado
                print("Sua área é: ",area)
                print("Seu perímetro é: ",perimetro) 
            case 3: #Paralelogramo
                base = float(input("Digite e base: "))
                altura = float(input("Digite a altura: "))
                ladoobliquo = float(input("Digite a lados obliquo: "))
                area = base * altura
                perimetro = 2*(ladoobliquo+base)
                print("Sua área é: ",area)
                print("Seu perímetro é: ",perimetro)
            case 4: #Triangulo
                base = float(input("Digite e base: "))
                altura = float(input("Digite a altura: "))
                area = base*altura/2
                print("Selecione o triangulo para calcular o perímetro")
                print("1- Escaleno - três lados diferentes")
                print("2- Isósceles - dois lados iguais e uma base")
                print("3- Equilatero - três lados iguas")
                interacao2 = int(input("Responda: "))
                match(interacao2):
                    case 1: #Escaleno
                        a = float(input("Digite a medida do lado 1: "))
                        b = float(input("Digite a medida do lado 2: "))
                        c = float(input("Digite a medida do lado 3: "))
                        perimetro = a+b+c
                        print("Sua área é: ",area)
                        print("Seu perímetro é: ",perimetro)
                    case 2: #Isósceles
                        lado = float(input("Digite o valor do lado: "))
                        perimetro = base+(2*lado)
                        print("Sua área é: ",area)
                        print("Seu perímetro é: ",perimetro)
                    case 3: #Equilatero
                        lado = float(input("Digite o valor do lado: "))
                        perimetro = 3*lado
                        print("Sua área é: ",area)
                        print("Seu perímetro é: ",perimetro)
            case 5: #Losango ou rombo
                diagonalmaior = float(input("Digite a Diagonal Maior: "))
                diagonalmenor = float(input("Digite a Diagonal Menor: ")) 
                lado = float(input("Digite o valor do lado: "))
                area = diagonalmaior*diagonalmenor/2
                perimetro = 4*lado
                print("Sua área é: ",area)
                print("Seu perímetro é: ",perimetro)
            case 6: #Trapézio
                basemenor = float(input("Digite e base menor: "))
                basemaior = float(input("Digite e base maior: "))
                altura = float(input("Digite a altura: "))
                lado = float(input("Digite o valor do lado: "))
                area = (basemaior+basemenor)*altura/2
                perimetro = (2*lado)+basemaior+basemenor
                print("Sua área é: ",area)
                print("Seu perímetro é: ",perimetro)
            case 7: #Circulo
                pi = 3.14159
                raio = float(input("Digite o raio: "))
                area = pi*raio**2
                perimetro = 2*pi*raio
                print("Sua área é: ",area)
                print("Seu perímetro é: ",perimetro)            
except Exception:
    print("Opção inválida")
