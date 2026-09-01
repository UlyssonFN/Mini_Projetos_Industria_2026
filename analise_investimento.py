#Verificar bitcoin tempo real
import pandas as pd
import yfinance as yf

acao_entrada = input("Digite a ação que procura: ")

acao = yf.Ticker(acao_entrada)

print("---Informe o período--- ")
print("1d = 1 dia, 1mo = 1 mês, 1y = 1 ano, ytd = inicio do ano até hoje, max = todo histórico")
periodo = input("Digite o período: ")

if periodo == '1d' or periodo == '1mo' or periodo == '1y' or periodo == 'ytd' or periodo =='max':
    df = ticker.history()
else:
    print("valor inválido")

