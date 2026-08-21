#Geração de Imagens QRcode
#Código usado para gerar imagens QRcode a partir de links

#biblioteca de QRcode para instalar pip install qrcode
import qrcode as qr

#Digitar o link online, utilizo bastante para criar inscrições em forms e divulgo as vagas com o qrcode
link = "https://www.linkedin.com/in/ulysson-fontenele-nobre-287a26125/"

#criar a imagem do QrCode
imagem = qr.make(link)

#Gera a imagem do qrcode
imagem.save("C:\\FFOutput\\qrcode_linkedin.png")

