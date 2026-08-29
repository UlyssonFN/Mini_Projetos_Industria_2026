#Logaritmo
#Volume de um Cubo V = a³
#Paralelepipedo Retângulo V = a*b*c
#Cilindro 'Sb = área da base do cilindro' então V = Sb*h, lembrando que para saber a área da base A = Pi*Raio²
#Cálculo de Log| Loga N = x <-> a^x = N
#Logaritmo decimnal: É o log de base 10, normalmente o logaritmo decimal não tem sua base especificada. Se escreve log =a já entende que a base é 10
#Logaritmo natural: Também chamado de logaritmo neperiano. Sua base é o número e=2,71828...(número de Euler) Loge a = Ln a
#1L é igual a 1dm³ e 1dm é igual a 10cm
#Logb (a*c) = logb a + logb c
#Logb (a:c) = logb a - logb c
#Logb a^n = n*logb a

def logaritmo():
    from funcoes import space, repeticao
    import math
    
    a = 1
    while a == 1:
        print("Aula de Logaritmos - Escolha uma opção abaixo")
        print("1 - Volume de um Cubo")
        print("2 - Volume de um Paralelepipedo Retângulo")
        print("3 - Volume de um Cilindro")
        resp = int(input("Responda: ")) 
        match(resp):
            case 1:
                print("Descubra o volume de um Cubo")
                area = float(input("Digite a área do cubo"))
                volumeC = area**3
                #cm para m
                cmpm = area / 10 / 10
                #m³
                m3 = cmpm**3
                print("O volume do seu Cubo é: ",volumeC,"cm3")
                print("Convertendo para m³: ",m3,"m³")
            case 2:
                print("Descubra o volume de um Paralelepipedo Retângulo")
                area = float(input("Digite a: "))
                base = float(input("Digite b: "))
                profundidade = float(input("Digite c: "))
                volumeP = area*base*profundidade
                litros = (area*10)*(base*10)*(profundidade*10)
                print("O volume do seu Paralelepipedo é: ",volumeP,"m³")
                print("Convertendo para litros: ",litros,"L")
            case 3:
                print("Descubra o volume de um Cilindro")
                pi = math.pi
                raioN = float(input("Digite o raio da área do cilindro: "))
                raio = raioN**2
                area_circulo = pi*raio
                #Sb=area_circulo
                altura = float(input("Digite a altura do cilindro(h): "))
                volumeC = area_circulo*altura
                print("A área do seu circulo é: ",area_circulo)
                print("O volume do seu Cilindro é: ",volumeC)
            case 4:
                a = float(input("Digite o valor de a que é a base: "))
                n = float(input("Digite o valor de N: "))
                x = float(input("Digite o valor de x: "))
                
                #log a^n = n*log a 
                resolucao = a**x
                print("O resultado da Base elevado a x é: ", resolucao)
                if resolucao == n:
                    print("É logaritmo")
                if n == 1:
                    print("O logaritmo de 1 em qualquer base é nulo = 0")
                elif log == a:
                    print("O logaritmo de log = a é a")
                #Rapaz entendi nada, me ajudem....
                
            case valor_invalido:
                print("O Valor, ",valor_invalido,"não corresponde a uma opção válida.")
                a = repeticao()
                
tipo = logaritmo()


#calcular o valor dos logaritmos dados
log2 8 =x
2^x = 8
2^x = 2³
x = 3