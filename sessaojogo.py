from datetime import datetime

class SessaoJogo:
    def __init__(self, jogo, tempo, percentual, status, data=None):
        self.jogo = jogo
        self.tempo = tempo
        self.percentual = percentual
        self.status = status
        self.data = data if data else datetime.now().strftime('%d/%m/%Y %H:%M')

    def exibir(self):
        print(f'{self.jogo.titulo} | Tempo: {self.tempo}h | Data: {self.data} | Percentual: {self.percentual}% | Status: {self.status}')

