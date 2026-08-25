from notifypy import Notify

notificacao = Notify()

notificacao.title = "Sistema de Produtividade"
notificacao.message = "O cálculo foi concluído!"

notificacao.send()