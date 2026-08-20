#Sistema de Resolução de equação do 2° grau
#ax²+bx+c
#x=-b+ ou - √b²-4*a*c/2*a
import math

ax = float(input("Digite o valor de ax²: "))
bx = float(input("Digite o valor de bx: "))
c = float(input("Digite o valor de c: "))

ax2 = ax

print("Sua equação é: ",ax2,"²", bx, c,"=0")

bx1 = -(bx)
potenciacao = bx**2
mult = -4*ax2*c
div = 2*ax2
potsubmul = potenciacao + mult
raiz = math.sqrt(potsubmul)

print("Seu bx é: ",bx1)
print("Sua potencia é:", potenciacao)
print("Resultado do potsubmul: ",potsubmul)
print("Seu mult é: ",mult)
print("Sua raiz é: ", raiz)
print("Seu div é: ",div)

x01 = bx1+raiz
x02 = bx1-raiz

x1 = x01/div
x2 = x02/div

print("Seu x1 é: ",round(x1,2))
print("Seu x2 é: ",round(x2,2))
