#Verificar bitcoin tempo real
import pandas as pd
import yfinance as yf
from notifypy import Notify
from funcoes import space, repeticao

a = 1
while a==1:
    print("Escolha a ação:")
    print("1 - Ação BR (interna)")
    print("2 - Ação Externa")
    resposta = int(input("Digite uma opção: "))
    match(resposta):
        case 1:
            space()
            acao_entrada = input("Digite a ação que procura: ")
            sufixobr = '.SA'

            acao = yf.Ticker(acao_entrada+sufixobr)

            print("---Informe o período--- ")
            print("1d = 1 dia, 1mo = 1 mês, 1y = 1 ano, ytd = inicio do ano até hoje, max = todo histórico")
            periodo = input("Digite o período: ")

            if periodo == '1d' or periodo == '1mo' or periodo == '1y' or periodo == 'ytd' or periodo =='max':
                df = acao.history(periodo)
                print("------Hoje (Ação BR)------",acao)
                print(round(df,2))
                print("------Detalhado (Ação BR)------", acao)
                print(round(df.describe(),2))
                a = repeticao()
            else:
                print("valor inválido")
                a = repeticao()
        case 2:
            space()
            acao_entrada = input("Digite a ação que procura: ")
            
            acao = yf.Ticker(acao_entrada)

            print("---Informe o período--- ")
            print("1d = 1 dia, 1mo = 1 mês, 1y = 1 ano, ytd = inicio do ano até hoje, max = todo histórico")
            periodo = input("Digite o período: ")

            if periodo == '1d' or periodo == '1mo' or periodo == '1y' or periodo == 'ytd' or periodo =='max':
                df = acao.history(periodo)
                print("------Hoje (Ação Ex)------",acao)
                print(round(df,2))
                print("------Detalhado (Ação Ex)------", acao)
                print(round(df.describe(),2))
                a = repeticao()
            else:
                print("valor inválido")
                a = repeticao()