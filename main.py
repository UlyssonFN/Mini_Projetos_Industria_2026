#Menu dos sistemas
def menu():
    from funcoes import space, repeticao

    a = 1
    while a ==1:
        call = space()
        print("------------Menu de Solicitações-------------")
        print("1 - Regra de 3 Simples")
        print("2 - Geração de QrCode")
        print("3 - Equação 2° Grau")
        print("4 - Calculadora de Produtividade")
        call = space()
        try:
            respc = int(input("Insira a opção desejada: "))

            match respc:
                case 1:
                    import regra_3_simples
                    call = regra_3_simples
                case 2:
                    import gerar_qrcode
                    call = gerar_qrcode
                case 3:
                    import equacao_2_Grau
                    call = equacao_2_Grau
                case 4:
                    import calculadora_Produtividade
                    call = calculadora_Produtividade
        except Exception:
            print("Nenhum valor corresponde a lista")
            a =1
            call = space()
call = menu()