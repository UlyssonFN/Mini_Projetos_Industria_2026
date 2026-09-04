#Verificar bitcoin tempo real
import pandas as pd
import yfinance as yf
from notifypy import Notify
from funcoes import space, repeticao
import datetime as dt

a = 1
while a==1:
    hoje = dt.date.today()
    print(hoje)
    hora = dt.time()
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
            cotas = int(input("Digite a quantidade de cotas compradas: "))
            data_compra = input("Digite a data da compra: aaaa-mm-dd ")
            #converter para dataframer
            data_compra = pd.to_datetime(data_compra)
            periodomax = 'max'
            dfmax = acao.history(periodomax)
            #faz o filtro de acordo com o que o cliente digitar de data
            filtro = dfmax[dfmax.index.date == data_compra.date()]
            #["Close"] → quero a coluna Close
            #.iloc[0] → quero o primeiro valor dessa coluna
            precofechamento = filtro['Close'].iloc[0]
            investimento_inicial = cotas * precofechamento
            space()
            print('O seu investimento inicial foi de :',round(investimento_inicial,2))
            space()           
            
            if periodo == '1d' or periodo == '1mo' or periodo == '1y' or periodo == 'ytd' or periodo =='max':
                df = acao.history(periodo)
                df2 = df.filter(items=['Open','Close'])
                print("------Hoje (Ação BR)------",acao)
                print(round(df2,2))
                print("------Detalhado (Ação BR)------", acao)
                print(round(df2.describe(),2))
                
                #calculo de investimento atual
                precofechamento_hoje = acao.history('1d')
                filtro_hoje = precofechamento_hoje[precofechamento_hoje.index.date == hoje]
                precofechamento_hojef = filtro_hoje['Close'].iloc[0]
                investimento_atual = precofechamento_hojef * cotas
                space()
                print('O seu investimento Hoje é de :',round(investimento_atual,2))
                space()    
                
                lucro_prejuizo = investimento_atual - investimento_inicial
                
                if lucro_prejuizo < 0:
                    print("Seu prejuízo é de :", lucro_prejuizo)
                    a = repeticao()
                else:
                    print("Seu Lucro é de :", lucro_prejuizo)
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
                