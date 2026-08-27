#Sistema de Resolução de equação do 2° grau
#ax²+bx+c
#Delta = b²-4*a*c
#x=-b+ or - √b²-4*a*c/2*a
def equacao2grau():
    from funcoes import space, repeticao
    import math
    a = 1
    while a == 1:
        try:
            print("Sistema de Resolução de Equação do 2° Grau")
            call = space()
            #Definição de variáveis de entrada ax²+bx+c
            ax = float(input("Digite o valor de ax²: "))
            if ax == 0:
                print("Não é uma equação do 2° Grau")
                a = repeticao()
            else:
                bx = float(input("Digite o valor de bx: "))
                c = float(input("Digite o valor de c: "))
                call = space()
                #comi bola aqui e acabei sujando o código, mas vou deixar assim.
                ax2 = ax
                #mostrando o formato da equação, porém sem os sinais de positivo e negativo
                print("Sua equação é: ",ax2,"²", bx, c,"=0")

                #Aqui a mágica acontece, tive que realizar cada cálculo separado (transformo b em nevativo -b igual inicio da formula)
                bx1 = -(bx)
                #b² para resolver o delta
                potenciacao = bx**2
                #Faço a multiplicação da parte do Delta
                mult = -4*ax2*c
                #Divisão da parte de x
                div = 2*ax2
                #Resultado do Delta
                delta = potenciacao + mult
                #Aqui confesso que tive que entender um pouco mais, se houver raiz nevativa o programa dava erro, ou seja, o resultado é a raiz negativa.
                if delta < 0:
                    call = space()
                    print("Não existem raízes reais.")
                    print("Resultado do Delta: ",delta)
                    call = space()
                    a = repeticao()
                #Caso a raiz não seja negativa ele continua resolvendo a equação.
                else:
                    raiz = math.sqrt(delta)        
                    print("------Cálculos da Equação------")
                    print("Seu bx é: ",bx1)
                    print("Sua potencia é:", potenciacao)
                    print("Resultado do Delta: ",delta)
                    print("Seu mult é: ",mult)
                    print("Sua raiz é: ", raiz)
                    print("Seu div é: ",div)

                    #Lembra da formula x=-b+ or - √b²-4*a*c
                    x01 = bx1+raiz
                    x02 = bx1-raiz
                    #Aqui é o final colocando a divisão x=-b+ or - √b²-4*a*c/2*a
                    x1 = x01/div
                    x2 = x02/div
                    print("------Resultado Final------")
                    print("Seu x1 é: ",round(x1,2))
                    print("Seu x2 é: ",round(x2,2))
                    call = space()
                    a = repeticao()
        #Tratativa de erro caso haja divisão por zero
        except ZeroDivisionError:
            print("A equação apresentou divisão por zero!")
            a = repeticao()
        #Tratativa de Erro para entrada de dados inválida
        except Exception:
            print("Entrada de Dados inválida")
            a = repeticao()