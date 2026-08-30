
def medicao_porta_palete_ocupacao():
    from funcoes import space, repeticao

    #dado essas variáveis faça um programa para verificar a estimativa de ocupação do porta palete
    #m_faturamento =55253 
    #m_recebimento =72525 
    #qtd_pp =3057
    #qtd_livre =343
    #qtd_ocupada =2714
    #unid_total = 3372384
    #m_unid_por_pp =1243
    a = 1
    while a == 1:
        try:
            total_enderecos = int(input("Ditite o total de endereços Porta Palete: "))
            endereco_livres = int(input("Ditite o total de endereços livres: "))
            ocupados = total_enderecos-endereco_livres
            percentil = (endereco_livres/total_enderecos)*100
            print("Total de endereços ocupados é ", ocupados)
            print("O percentil livre é ",round(percentil,2),"%")
            space()
            m_faturamento1 = int(input("Digite a média de faturamento: "))
            m_recebimento1 = int(input("Digite a média de recebimento: "))
            unid_totalcd = int(input("Digite as unidades totais contidas no PP: "))
            space()
            m_unid_por_pp1 = unid_totalcd/ocupados
            print("A média de unidades armazenadas por endereço é ", round(m_unid_por_pp1,0))
            # então se 1PP = m_unid_por_PP1 = unid_totalcd/ocupados
            consumo_posicao_recebimento = (m_recebimento1*1)/m_unid_por_pp1
            print("O consumo de paletes médio/dia no recebimento é: ",round(consumo_posicao_recebimento,0))
            vazao_posicao_faturamento = (m_faturamento1*1)/m_unid_por_pp1
            print("A vazão média de paletes por dia é: ",round(vazao_posicao_faturamento,0))
            space()
            sobra = consumo_posicao_recebimento - vazao_posicao_faturamento
            print("Todos os dias é armazenado uma diferença de ",round(sobra,0)," em relação ao que libera no faturamento")
            dias_para_lotacao = endereco_livres/sobra
            print("Seu Porta Palete irá ser preenchido em sua totalidade em ",round(dias_para_lotacao,0)," dias")
            space()
            a = repeticao()
        except ValueError():
            print("Digite um número inteiro")
            space()
            a = repeticao()
        except Exception():
            print("Valor inválido")
            space()
            a = repeticao()
        except ZeroDivisionError():
            print("Valor inválido")
            space()
            a = repeticao()