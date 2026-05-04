"""
Menu Interativo para SteamPy
Sistema de Gerenciamento de Biblioteca de Jogos
"""

from steamPy import SteamPy
from pathlib import Path
import os


class MenuSteamPy:
    """
    Gerenciador de menu interativo para o SteamPy.
    """
    
    def __init__(self):
        self.steampy = SteamPy()
        self.jogos_carregados = False
        self.rodando = True
    
    def limpar_tela(self):
        """Limpa a tela do console."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausa(self):
        """Pausa a execução até o usuário pressionar Enter."""
        input("\n➡️  Pressione ENTER para continuar...")
    
    def exibir_menu_principal(self):
        """Exibe o menu principal com todas as opções."""
        self.limpar_tela()
        
        print(f"\n{'='*80}")
        print(f"{'STEAMPY - GERENCIADOR DE BIBLIOTECA DE JOGOS':^80}")
        print(f"{'='*80}")
        
        # Indicar status
        status = "✅ CARREGADO" if self.jogos_carregados else "⚠️  NÃO CARREGADO"
        print(f"\n📊 Status dos Jogos: {status}")
        if self.jogos_carregados:
            print(f"   Total: {len(self.steampy.jogos)} jogos")
            print(f"   Backlog: {self.steampy.backlog.tamanho()} jogos")
            print(f"   Sessões: {len(self.steampy.sessoes)} registradas")
            print(f"   Recentes: {self.steampy.recentes.tamanho()} jogos")
        
        print(f"\n{'='*80}")
        print(f"\n🎮 MENU PRINCIPAL:\n")
        print(f"  1. 📂  Carregar Catálogo")
        print(f"  2. 📋  Listar Jogos")
        print(f"  3. 🔍  Buscar Jogo por Nome")
        print(f"  4. 📚  Filtrar por Gênero")
        print(f"  5. 💾  Filtrar por Console")
        print(f"  6. ⭐  Filtrar por Nota")
        print(f"  7. 📊  Ordenar Catálogo")
        print(f"  8. ➕  Adicionar Jogo ao Backlog")
        print(f"  9. 📝  Ver Backlog")
        print(f" 10. ▶️   Jogar Próximo do Backlog")
        print(f" 11. 🎮  Ver Jogos Recentes")
        print(f" 12. 🔄  Retomar Último Jogo")
        print(f" 13. ⏱️   Registrar Tempo de Jogo")
        print(f" 14. 📖  Ver Histórico Completo")
        print(f" 15. 💡  Ver Recomendações")
        print(f" 16. 🏆  Ver Ranking Pessoal")
        print(f" 17. 💾  Salvar Backlog e Dados")
        print(f" 18. 🚪  Sair")
        print(f"\n{'='*80}\n")
    
    def opcao_1_carregar_catalogo(self):
        """Carrega o catálogo de jogos do arquivo CSV."""
        self.limpar_tela()
        
        print(f"\n{'='*80}")
        print(f"{'CARREGAR CATÁLOGO':^80}")
        print(f"{'='*80}\n")
        
        # Procura por arquivo CSV na pasta
        caminho_csv = Path("games.csv")
        caminho_dataset = Path("dataset.csv")
        
        # Tenta encontrar o arquivo
        arquivo = None
        if caminho_csv.exists():
            arquivo = "games.csv"
        elif caminho_dataset.exists():
            arquivo = "dataset.csv"
        else:
            # Pede ao usuário para informar o caminho
            arquivo = input("📄 Digite o caminho do arquivo CSV (ex: games.csv): ").strip()
            
            if not arquivo:
                print("❌ Nenhum arquivo informado!")
                self.pausa()
                return
        
        if self.steampy.carregarJogos(arquivo):
            self.jogos_carregados = True
        
        self.pausa()
    
    def opcao_2_listar_jogos(self):
        """Lista todos os jogos carregados."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado! Por favor, carregue o catálogo primeiro.")
            self.pausa()
            return
        
        print(f"\n")
        self.steampy.listarJogos()
        self.pausa()
    
    def opcao_3_buscar_jogo(self):
        """Busca um jogo por nome."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado!")
            self.pausa()
            return
        
        print(f"\n{'='*80}")
        print(f"{'BUSCAR JOGO POR NOME':^80}")
        print(f"{'='*80}\n")
        
        termo = input("🔍 Digite o nome do jogo para buscar: ").strip()
        
        if termo:
            self.steampy.buscarJogoPorNome(termo)
        
        self.pausa()
    
    def opcao_4_filtrar_genero(self):
        """Filtra jogos por gênero."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado!")
            self.pausa()
            return
        
        print(f"\n{'='*80}")
        print(f"{'FILTRAR POR GÊNERO':^80}")
        print(f"{'='*80}\n")
        
        # Listar gêneros únicos
        generos = sorted(set(j.genero for j in self.steampy.jogos))
        print(f"📚 Gêneros disponíveis:\n")
        for idx, genero in enumerate(generos, 1):
            print(f"  {idx}. {genero}")
        
        print()
        genero = input("Escolha um gênero (nome completo): ").strip()
        
        if genero:
            self.steampy.filtrarPorGenero(genero)
        
        self.pausa()
    
    def opcao_5_filtrar_console(self):
        """Filtra jogos por console."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado!")
            self.pausa()
            return
        
        print(f"\n{'='*80}")
        print(f"{'FILTRAR POR CONSOLE':^80}")
        print(f"{'='*80}\n")
        
        # Listar consoles únicos
        consoles = sorted(set(j.console for j in self.steampy.jogos))
        print(f"💾 Consoles disponíveis:\n")
        for idx, console in enumerate(consoles, 1):
            print(f"  {idx}. {console}")
        
        print()
        console = input("Escolha um console (nome completo): ").strip()
        
        if console:
            self.steampy.filtrarPorConsole(console)
        
        self.pausa()
    
    def opcao_6_filtrar_nota(self):
        """Filtra jogos por nota mínima."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado!")
            self.pausa()
            return
        
        print(f"\n{'='*80}")
        print(f"{'FILTRAR POR NOTA':^80}")
        print(f"{'='*80}\n")
        
        try:
            nota = input("⭐ Digite a nota mínima (0-100): ").strip()
            if nota:
                self.steampy.filtrarPorNota(float(nota))
        except ValueError:
            print("\n❌ Nota inválida!")
        
        self.pausa()
    
    def opcao_7_ordenar_catalogo(self):
        """Ordena o catálogo por diferentes critérios."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado!")
            self.pausa()
            return
        
        print(f"\n{'='*80}")
        print(f"{'ORDENAR CATÁLOGO':^80}")
        print(f"{'='*80}\n")
        print("📋 Critérios disponíveis:\n")
        print("  1. Título")
        print("  2. Nota")
        print("  3. Vendas")
        print("  4. Console")
        print("  5. Gênero")
        print()
        
        criterios = {
            '1': 'titulo',
            '2': 'nota',
            '3': 'vendas',
            '4': 'console',
            '5': 'genero'
        }
        
        opcao = input("Escolha o critério (1-5): ").strip()
        
        if opcao in criterios:
            self.steampy.ordenarJogos(criterios[opcao])
        else:
            print("\n❌ Opção inválida!")
        
        self.pausa()
    
    def opcao_8_adicionar_backlog(self):
        """Adiciona um jogo ao backlog."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado!")
            self.pausa()
            return
        
        print(f"\n{'='*80}")
        print(f"{'ADICIONAR JOGO AO BACKLOG':^80}")
        print(f"{'='*80}\n")
        
        termo = input("🔍 Digite o nome do jogo para adicionar: ").strip()
        
        if termo:
            resultados = [j for j in self.steampy.jogos if termo.lower() in j.titulo.lower()]
            
            if not resultados:
                print(f"\n❌ Nenhum jogo encontrado com '{termo}'!")
            elif len(resultados) == 1:
                self.steampy.adicionarAoBacklog(resultados[0])
            else:
                print(f"\n🎮 {len(resultados)} jogo(s) encontrado(s):\n")
                for idx, jogo in enumerate(resultados, 1):
                    print(f"  {idx}. {jogo.titulo} ({jogo.console})")
                
                try:
                    escolha = int(input("\nEscolha o número do jogo: ")) - 1
                    if 0 <= escolha < len(resultados):
                        self.steampy.adicionarAoBacklog(resultados[escolha])
                    else:
                        print("❌ Opção inválida!")
                except ValueError:
                    print("❌ Entrada inválida!")
        
        self.pausa()
    
    def opcao_9_ver_backlog(self):
        """Exibe o backlog."""
        self.limpar_tela()
        
        print(f"\n")
        self.steampy.mostrarBacklog()
        self.pausa()
    
    def opcao_10_jogar_proximo(self):
        """Joga o próximo jogo do backlog."""
        self.limpar_tela()
        
        print(f"\n{'='*80}")
        print(f"{'JOGAR PRÓXIMO DO BACKLOG':^80}")
        print(f"{'='*80}\n")
        
        jogo = self.steampy.jogarProximo()
        self.pausa()
    
    def opcao_11_ver_recentes(self):
        """Exibe os jogos recentes."""
        self.limpar_tela()
        
        print(f"\n")
        self.steampy.mostrarRecentes()
        self.pausa()
    
    def opcao_12_retomar_ultimo_jogo(self):
        """Retoma o último jogo jogado."""
        self.limpar_tela()
        
        print(f"\n{'='*80}")
        print(f"{'RETOMAR ÚLTIMO JOGO':^80}")
        print(f"{'='*80}\n")
        
        jogo = self.steampy.retomarUltimoJogo()
        self.pausa()
    
    def opcao_13_registrar_tempo(self):
        """Registra uma sessão de jogo."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado!")
            self.pausa()
            return
        
        print(f"\n{'='*80}")
        print(f"{'REGISTRAR TEMPO DE JOGO':^80}")
        print(f"{'='*80}\n")
        
        try:
            termo = input("🔍 Digite o nome do jogo: ").strip()
            
            if not termo:
                print("❌ Nenhum jogo informado!")
                self.pausa()
                return
            
            resultados = [j for j in self.steampy.jogos if termo.lower() in j.titulo.lower()]
            
            if not resultados:
                print(f"❌ Nenhum jogo encontrado!")
                self.pausa()
                return
            
            jogo = resultados[0] if len(resultados) == 1 else self._selecionar_jogo(resultados)
            
            if not jogo:
                self.pausa()
                return
            
            tempo = float(input("\n⏱️  Tempo jogado (horas): "))
            percentual = float(input("📊 Percentual completado (0-100): "))
            
            print("\n📝 Status da sessão:")
            print("  1. Pausado")
            print("  2. Em Progresso")
            print("  3. Completado")
            
            status_map = {
                '1': 'pausado',
                '2': 'em progresso',
                '3': 'completado'
            }
            
            status_opcao = input("\nEscolha o status (1-3): ").strip()
            status = status_map.get(status_opcao, 'em progresso')
            
            self.steampy.registrarSessao(jogo, tempo, percentual, status)
            
        except ValueError:
            print("❌ Valores inválidos!")
        
        self.pausa()
    
    def opcao_14_ver_historico(self):
        """Exibe o histórico completo de sessões."""
        self.limpar_tela()
        
        print(f"\n{'='*80}")
        print(f"{'HISTÓRICO COMPLETO DE SESSÕES':^80}")
        print(f"{'='*80}\n")
        
        if not self.steampy.sessoes:
            print("📭 Nenhuma sessão registrada!\n")
        else:
            tempo_total = sum(s.tempo for s in self.steampy.sessoes)
            print(f"Total de sessões: {len(self.steampy.sessoes)}")
            print(f"Tempo total: {tempo_total:.1f}h\n")
            print(f"{'='*80}\n")
            
            for idx, sessao in enumerate(self.steampy.sessoes, 1):
                print(f"{idx}. {sessao.jogo.titulo}")
                print(f"   Tempo: {sessao.tempo}h | Percentual: {sessao.percentual}% | Status: {sessao.status}")
                print(f"   Data: {sessao.data}\n")
        
        self.pausa()
    
    def opcao_15_ver_recomendacoes(self):
        """Exibe recomendações de jogos."""
        self.limpar_tela()
        
        if not self.jogos_carregados:
            print("\n❌ Nenhum catálogo carregado!")
            self.pausa()
            return
        
        print(f"\n{'='*80}")
        print(f"{'RECOMENDAÇÕES':^80}")
        print(f"{'='*80}\n")
        print("💡 Opções de recomendação:\n")
        print("  1. Top 5 geral")
        print("  2. Top 5 por gênero específico")
        print()
        
        opcao = input("Escolha uma opção (1-2): ").strip()
        
        if opcao == '1':
            self.steampy.recomendarJogos(limite=5)
        elif opcao == '2':
            genero = input("Qual gênero? ").strip()
            if genero:
                self.steampy.recomendarJogos(genero=genero, limite=5)
        else:
            print("❌ Opção inválida!")
        
        self.pausa()
    
    def opcao_16_ranking(self):
        """Exibe o ranking pessoal com base no comportamento do usuário."""
        self.limpar_tela()
        
        print(f"\n{'='*80}")
        print(f"{'RANKING PESSOAL':^80}")
        print(f"{'='*80}\n")
        print("🏆 Tipos de ranking disponíveis:\n")
        print("  1. Comportamento do Usuário (recomendado)")
        print("  2. Jogos Mais Jogados")
        print("  3. Gêneros Mais Jogados")
        print("  4. Consoles Mais Jogados")
        print("  5. Top Jogos Bem Avaliados (histórico)")
        print("  6. Top por Nota")
        print("  7. Top por Vendas")
        print()
        
        ranking_types = {
            '1': 'comportamento',
            '2': 'jogos_mais_jogados',
            '3': 'generos',
            '4': 'consoles',
            '5': 'nota_historico',
            '6': 'nota',
            '7': 'vendas'
        }
        
        opcao = input("Escolha o tipo de ranking (1-7): ").strip()
        
        if opcao in ranking_types:
            tipo = ranking_types[opcao]
            limite = 10
            
            if opcao in ['1', '2', '3', '4', '5']:
                try:
                    limite = int(input(f"Limite de itens (padrão 10): ") or 10)
                except ValueError:
                    limite = 10
            
            self.steampy.gerarRanking(tipo=tipo, limite=limite)
        else:
            print("❌ Opção inválida!")
        
        self.pausa()
    
    def opcao_17_salvar_dados(self):
        """Salva todos os dados do sistema."""
        self.limpar_tela()
        
        print(f"\n{'='*80}")
        print(f"{'SALVAR DADOS':^80}")
        print(f"{'='*80}\n")
        
        self.steampy.salvarTudo()
        self.pausa()
    
    def opcao_18_sair(self):
        """Encerra o programa."""
        self.limpar_tela()
        
        print(f"\n{'='*80}")
        print(f"{'SAIR DO SISTEMA':^80}")
        print(f"{'='*80}\n")
        
        print("💾 Salvando dados antes de sair...\n")
        self.steampy.salvarTudo()
        
        print(f"\n👋 Obrigado por usar SteamPy!")
        print(f"{'='*80}\n")
        
        self.rodando = False
    
    def _selecionar_jogo(self, jogos):
        """Auxiliar para selecionar um jogo da lista."""
        if len(jogos) == 1:
            return jogos[0]
        
        print(f"\n🎮 {len(jogos)} jogo(s) encontrado(s):\n")
        for idx, jogo in enumerate(jogos, 1):
            print(f"  {idx}. {jogo.titulo} ({jogo.console})")
        
        try:
            escolha = int(input("\nEscolha o número do jogo: ")) - 1
            if 0 <= escolha < len(jogos):
                return jogos[escolha]
        except ValueError:
            pass
        
        return None
    
    def executar(self):
        """Executa o loop principal do menu."""
        while self.rodando:
            self.exibir_menu_principal()
            
            try:
                opcao = input("Escolha uma opção (1-18): ").strip()
                
                opcoes = {
                    '1': self.opcao_1_carregar_catalogo,
                    '2': self.opcao_2_listar_jogos,
                    '3': self.opcao_3_buscar_jogo,
                    '4': self.opcao_4_filtrar_genero,
                    '5': self.opcao_5_filtrar_console,
                    '6': self.opcao_6_filtrar_nota,
                    '7': self.opcao_7_ordenar_catalogo,
                    '8': self.opcao_8_adicionar_backlog,
                    '9': self.opcao_9_ver_backlog,
                    '10': self.opcao_10_jogar_proximo,
                    '11': self.opcao_11_ver_recentes,
                    '12': self.opcao_12_retomar_ultimo_jogo,
                    '13': self.opcao_13_registrar_tempo,
                    '14': self.opcao_14_ver_historico,
                    '15': self.opcao_15_ver_recomendacoes,
                    '16': self.opcao_16_ranking,
                    '17': self.opcao_17_salvar_dados,
                    '18': self.opcao_18_sair,
                }
                
                if opcao in opcoes:
                    opcoes[opcao]()
                else:
                    print("\n❌ Opção inválida! Digite um número entre 1 e 18.")
                    input("\n➡️  Pressione ENTER para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Operação interrompida pelo usuário!")
                print("💾 Salvando dados...\n")
                self.steampy.salvarTudo()
                self.rodando = False
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("\n➡️  Pressione ENTER para continuar...")


def main():
    """Função principal."""
    menu = MenuSteamPy()
    menu.executar()


if __name__ == "__main__":
    main()
