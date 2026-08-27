#Menu dos sistemas

from funcoes import space, repeticao
from calculadora_Produtividade import calculadora_produtividade
from calculo_area_perimetro import area_perimentro
from calculo_capacidade_endereco import capacidade_volumetrica
from equacao_2_Grau import equacao2grau
from gerar_qrcode import qrcode
from regra_3_simples import regrade3
from avisos_biblioteca import notify

notify()

a = 1
while a ==1:
    call = space()
    print("------------Menu de Solicitações-------------")
    print("1 - Regra de 3 Simples")
    print("2 - Geração de QrCode")
    print("3 - Equação 2° Grau")
    print("4 - Calculadora de Produtividade")
    print("5 - Calculo de Área e Perímetro de Figuras Geométricas")
    print("6 - Cálculo de Capacidade de Endereço Volumetrico")
    call = space()
    try:
        respc = int(input("Insira a opção desejada: "))

        match respc:
            case 1:
                regrade3()
            case 2:
                qrcode()
            case 3:
                equacao2grau()
            case 4:
                calculadora_produtividade()
            case 5:
                area_perimentro()
            case 6:
                capacidade_volumetrica()
            case valor_desconhecido:
                print(f"Erro: O comando '{valor_desconhecido}'é inválido.")
                a = repeticao()
    except Exception:
        print("Nenhum valor corresponde a lista")
        a = repeticao()
        call = space()
    