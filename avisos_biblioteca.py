def notify():
    from notifypy import Notify

    notificacao = Notify()

    notificacao.title = "Sistema Online - Siga Ulysson Fontenele Linkedin"
    notificacao.message = "Bem vindo ao Repositório mais atualizado em regras!"

    notificacao.send()