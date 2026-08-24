#Cálculo de Perímetros e Área de Figuras

print("Escolha a figura: ")
print("1 - Retângulo")
print("2 - Quadrado")
print("3 - Paralelogramo")
print("4 - Triangulo")
print("5 - Losango ou rombo")
print("6 - Trapézio")
print("7 - Ciruclo")

interacao = int(input("Responda: "))

match(interacao):
    case 1:
        base = float(input("Digite e base: "))
        altura = float(input("Digite a altura: "))
        area = base * altura
        perimetro = (2*base)+(2*altura)
        print("Sua área é: ",area)
        print("Seu perímetro é: ",perimetro)