class Jogo:
    def __init__(self, idJogo, titulo, console, genero, publisher, developer, criticScore, totalVendas, vendasAn, vendasJp, vendasEu, outrasVendas, dataLanc):
        self.idJogo = idJogo
        self.titulo = titulo
        self.console = console
        self.genero = genero
        self.publisher = publisher
        self.developer = developer
        self.criticScore = criticScore
        self.totalVendas = totalVendas
        self.vendasAn = vendasAn
        self.vendasJp = vendasJp
        self.vendasEu = vendasEu
        self.outrasVendas = outrasVendas
        self.dataLanc = dataLanc

    def exibir(self):
        print(f'ID: {self.idJogo} | {self.titulo} | Console: {self.console} | Gênero: {self.genero} | Score: {self.criticScore}')

    def linhaBacklog(self):
        return f'{self.idJogo}, {self.titulo}, {self.console}'

    def linhaRecentes(self):
        return f'{self.idJogo}, {self.titulo}, {self.console}'