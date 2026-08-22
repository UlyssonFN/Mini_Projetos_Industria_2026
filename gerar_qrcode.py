#Geração de Imagens QRcode
#Código usado para gerar imagens QRcode a partir de links

#biblioteca de QRcode para instalar pip install qrcode
import qrcode as qr

#Digitar o link online, utilizo bastante para criar inscrições em forms e divulgo as vagas com o qrcode
print("Bem vindo ao Sistema de Qrcode")
print("Seu Qrcode vai ser salvo na pasta C:\\Users\\Public\\Documents\\qrcode.png")

link = input("Digite o seu URL: ")

#criar a imagem do QrCode
imagem = qr.make(link)

#Gera a imagem do qrcode
imagem.save("C:\\Users\\Public\\Documents\\SeuQrCode.png")
print("Segue o Ulysson Fontenele Nobre no Linkedin e mande um salve")

