import csv
import json
from datetime import datetime
from pathlib import Path
from filabacklog import FilaBackLog
from pilharecentes import PilhaRecentes
from jogo import Jogo
from sessaojogo import SessaoJogo


class SteamPy:
    """
    Gerenciador de biblioteca de jogos com funcionalidades de backlog, histórico e recomendações.
    """

    def __init__(self):
        self.jogos = []
        self.backlog = FilaBackLog()
        self.recentes = PilhaRecentes()
        self.sessoes = []
        
        # Arquivos de persistência
        self._historico_arquivo = 'historicoJogo.txt'
        self._backlog_arquivo = 'backlog.txt'
        self._recentes_arquivo = 'recentes.txt'
        self._games_arquivo = 'games.csv'
        
        # Carregar dados salvos ao inicializar
        self._inicializar_dados()

    # ===========================
    # INICIALIZAÇÃO E PERSISTÊNCIA
    # ===========================

    def _inicializar_dados(self):
        """
        Carrega dados salvos ao inicializar o sistema.
        Tenta carregar backlog, histórico e recentes se existirem.
        """
        self.carregarBacklogTxt()
        self.carregarHistoricoTxt()
        self.carregarRecentesTxt()

    # ===========================
    # CARREGAMENTO DE DADOS
    # ===========================

    def carregarJogos(self, nome_arquivo):
        """
        Carrega jogos a partir de um arquivo CSV.
        
        Args:
            nome_arquivo (str): Caminho para o arquivo CSV
            
        Returns:
            bool: True se carregamento bem-sucedido, False caso contrário
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se o arquivo estiver vazio ou mal formatado
        """
        try:
            caminho = Path(nome_arquivo)
            
            if not caminho.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {nome_arquivo}")
            
            if not caminho.suffix.lower() == '.csv':
                raise ValueError("Arquivo deve ser do tipo CSV")
            
            jogos_carregados = 0
            linhas_invalidas = 0
            indice = 1
            
            with open(caminho, newline='', encoding='utf-8') as csvfile:
                leitor = csv.DictReader(csvfile)
                
                if leitor.fieldnames is None:
                    raise ValueError("Arquivo CSV vazio ou mal formatado")
                
                for num_linha, linha in enumerate(leitor, start=2):  # Começa em 2 (pois 1 é cabeçalho)
                    try:
                        jogo = self._criar_jogo_de_linha(linha, indice)
                        if jogo:
                            self.jogos.append(jogo)
                            jogos_carregados += 1
                            indice += 1
                    except ValueError as e:
                        linhas_invalidas += 1
                        print(f"⚠️  Linha {num_linha} - {e}")
                        continue
            
            if jogos_carregados == 0:
                raise ValueError("Nenhum jogo válido foi carregado")
            
            print(f"\n✅ {jogos_carregados} jogos carregados com sucesso!")
            if linhas_invalidas > 0:
                print(f"⚠️  {linhas_invalidas} linha(s) ignorada(s) por erro(s)")
            print(f"📁 Arquivo: {caminho.name}\n")
            return True
            
        except FileNotFoundError as e:
            print(f"❌ Erro: {e}")
            return False
        except ValueError as e:
            print(f"❌ Erro de validação: {e}")
            return False
        except Exception as e:
            print(f"❌ Erro inesperado ao carregar jogos: {e}")
            return False

    # ===========================
    # BACKLOG - PERSISTÊNCIA TXT
    # ===========================

    def salvarBacklogTxt(self, nome_arquivo=None):
        """
        Salva o backlog em arquivo TXT.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se salvo com sucesso
        """
        arquivo = nome_arquivo or self._backlog_arquivo
        
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(f"=== BACKLOG STEAMPY ===\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de jogos: {self.backlog.tamanho()}\n")
                f.write(f"{'='*50}\n\n")
                
                if self.backlog.is_empty():
                    f.write("Backlog vazio\n")
                else:
                    for idx, jogo in enumerate(self.backlog.dados, 1):
                        f.write(f"{idx}. ID: {jogo.idJogo}\n")
                        f.write(f"   Título: {jogo.titulo}\n")
                        f.write(f"   Console: {jogo.console}\n")
                        f.write(f"   Gênero: {jogo.genero}\n")
                        f.write(f"   Nota: {jogo.criticScore}\n")
                        f.write(f"\n")
            
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar backlog: {e}")
            return False

    def carregarBacklogTxt(self, nome_arquivo=None):
        """
        Carrega o backlog a partir de um arquivo TXT.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se carregado com sucesso
        """
        arquivo = nome_arquivo or self._backlog_arquivo
        
        try:
            if not Path(arquivo).exists():
                return False
            
            with open(arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            # Procura por IDs no arquivo
            ids_backlog = []
            for linha in linhas:
                if linha.startswith("ID: "):
                    id_jogo = linha.replace("ID: ", "").strip()
                    ids_backlog.append(id_jogo)
            
            # Reconstrói o backlog a partir dos jogos carregados
            for jogo in self.jogos:
                if jogo.idJogo in ids_backlog:
                    self.backlog.enqueue(jogo)
            
            if ids_backlog:
                # print(f"✅ Backlog carregado ({len(ids_backlog)} jogos)")
                pass
            return True
            
        except Exception as e:
            print(f"⚠️  Erro ao carregar backlog: {e}")
            return False

    # ===========================
    # HISTÓRICO - PERSISTÊNCIA TXT
    # ===========================

    def salvarHistoricoTxt(self, nome_arquivo=None):
        """
        Salva o histórico de sessões em arquivo TXT.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se salvo com sucesso
        """
        arquivo = nome_arquivo or self._historico_arquivo
        
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(f"=== HISTÓRICO DE SESSÕES STEAMPY ===\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de sessões: {len(self.sessoes)}\n")
                f.write(f"{'='*50}\n\n")
                
                if not self.sessoes:
                    f.write("Nenhuma sessão registrada\n")
                else:
                    tempo_total = sum(s.tempo for s in self.sessoes)
                    f.write(f"Tempo total jogado: {tempo_total:.1f}h\n\n")
                    
                    for idx, sessao in enumerate(self.sessoes, 1):
                        f.write(f"{idx}. Jogo: {sessao.jogo.titulo}\n")
                        f.write(f"   Console: {sessao.jogo.console}\n")
                        f.write(f"   Tempo: {sessao.tempo}h\n")
                        f.write(f"   Percentual: {sessao.percentual}%\n")
                        f.write(f"   Status: {sessao.status}\n")
                        f.write(f"   Data: {sessao.data}\n")
                        f.write(f"\n")
            
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar histórico: {e}")
            return False

    def carregarHistoricoTxt(self, nome_arquivo=None):
        """
        Carrega o histórico de sessões a partir de um arquivo TXT.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se carregado com sucesso
        """
        arquivo = nome_arquivo or self._historico_arquivo
        
        try:
            if not Path(arquivo).exists():
                return False
            
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Parse do arquivo para extrair sessões
            sessoes_count = 0
            linhas = conteudo.split('\n')
            
            sessao_atual = {}
            jogo_titulo = None
            
            for linha in linhas:
                if linha.strip().startswith("Jogo: "):
                    jogo_titulo = linha.replace("Jogo: ", "").strip()
                elif linha.strip().startswith("Tempo: "):
                    tempo = float(linha.replace("Tempo: ", "").replace("h", "").strip())
                    sessao_atual['tempo'] = tempo
                elif linha.strip().startswith("Percentual: "):
                    percentual = float(linha.replace("Percentual: ", "").replace("%", "").strip())
                    sessao_atual['percentual'] = percentual
                elif linha.strip().startswith("Status: "):
                    status = linha.replace("Status: ", "").strip()
                    sessao_atual['status'] = status
                elif linha.strip().startswith("Data: ") and jogo_titulo:
                    data = linha.replace("Data: ", "").strip()
                    sessao_atual['data'] = data
                    
                    # Encontra o jogo correspondente
                    jogo_encontrado = None
                    for jogo in self.jogos:
                        if jogo.titulo == jogo_titulo:
                            jogo_encontrado = jogo
                            break
                    
                    if jogo_encontrado and all(k in sessao_atual for k in ['tempo', 'percentual', 'status', 'data']):
                        sessao = SessaoJogo(
                            jogo_encontrado,
                            sessao_atual['tempo'],
                            sessao_atual['percentual'],
                            sessao_atual['status'],
                            sessao_atual['data']
                        )
                        self.sessoes.append(sessao)
                        sessoes_count += 1
                        sessao_atual = {}
                        jogo_titulo = None
            
            if sessoes_count > 0:
                # print(f"✅ Histórico carregado ({sessoes_count} sessões)")
                pass
            return True
            
        except Exception as e:
            print(f"⚠️  Erro ao carregar histórico: {e}")
            return False

    # ===========================
    # RECENTES - PERSISTÊNCIA TXT
    # ===========================

    def salvarRecentesTxt(self, nome_arquivo=None):
        """
        Salva os jogos recentes em arquivo TXT.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se salvo com sucesso
        """
        arquivo = nome_arquivo or self._recentes_arquivo
        
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(f"=== JOGOS RECENTES STEAMPY ===\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de jogos recentes: {self.recentes.tamanho()}\n")
                f.write(f"{'='*50}\n\n")
                
                if self.recentes.is_empty():
                    f.write("Nenhum jogo recente\n")
                else:
                    for idx in range(len(self.recentes.dados)-1, -1, -1):
                        jogo = self.recentes.dados[idx]
                        f.write(f"{len(self.recentes.dados)-idx}. ID: {jogo.idJogo}\n")
                        f.write(f"   Título: {jogo.titulo}\n")
                        f.write(f"   Console: {jogo.console}\n")
                        f.write(f"   Gênero: {jogo.genero}\n")
                        f.write(f"\n")
            
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar recentes: {e}")
            return False

    def carregarRecentesTxt(self, nome_arquivo=None):
        """
        Carrega os jogos recentes a partir de um arquivo TXT.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se carregado com sucesso
        """
        arquivo = nome_arquivo or self._recentes_arquivo
        
        try:
            if not Path(arquivo).exists():
                return False
            
            with open(arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            # Procura por IDs no arquivo
            ids_recentes = []
            for linha in linhas:
                if linha.strip().startswith("ID: "):
                    id_jogo = linha.replace("ID: ", "").strip()
                    ids_recentes.append(id_jogo)
            
            # Reconstrói os recentes a partir dos jogos carregados
            # Mantém a ordem inversa (do antigo para o novo)
            for id_jogo in ids_recentes:
                for jogo in self.jogos:
                    if jogo.idJogo == id_jogo:
                        self.recentes.push(jogo)
                        break
            
            if ids_recentes:
                # print(f"✅ Recentes carregado ({len(ids_recentes)} jogos)")
                pass
            return True
            
        except Exception as e:
            print(f"⚠️  Erro ao carregar recentes: {e}")
            return False

    def _criar_jogo_de_linha(self, linha, indice):
        """
        Cria um objeto Jogo a partir de uma linha do CSV.
        
        Args:
            linha (dict): Dicionário com dados da linha
            indice (int): Índice da linha para gerar ID único
            
        Returns:
            Jogo: Objeto Jogo criado
            
        Raises:
            ValueError: Se algum campo obrigatório estiver faltando
        """
        # Campos obrigatórios conforme dataset.csv
        campos_obrigatorios = ['title', 'console', 'genre']
        
        for campo in campos_obrigatorios:
            if campo not in linha or not linha[campo].strip():
                raise ValueError(f"Campo obrigatório ausente ou vazio: {campo}")
        
        try:
            # Gera ID único baseado no índice
            jogo_id = str(indice).zfill(5)
            
            # Converte campos numéricos com validação
            try:
                critic_score = float(linha.get('critic_score', 0)) if linha.get('critic_score', '').strip() else 0.0
            except ValueError:
                raise ValueError(f"critic_score inválido: {linha.get('critic_score')}")
            
            try:
                total_sales = float(linha.get('total_sales', 0)) if linha.get('total_sales', '').strip() else 0.0
            except ValueError:
                raise ValueError(f"total_sales inválido: {linha.get('total_sales')}")
            
            try:
                na_sales = float(linha.get('na_sales', 0)) if linha.get('na_sales', '').strip() else 0.0
            except ValueError:
                raise ValueError(f"na_sales inválido: {linha.get('na_sales')}")
            
            try:
                jp_sales = float(linha.get('jp_sales', 0)) if linha.get('jp_sales', '').strip() else 0.0
            except ValueError:
                raise ValueError(f"jp_sales inválido: {linha.get('jp_sales')}")
            
            try:
                pal_sales = float(linha.get('pal_sales', 0)) if linha.get('pal_sales', '').strip() else 0.0
            except ValueError:
                raise ValueError(f"pal_sales inválido: {linha.get('pal_sales')}")
            
            try:
                other_sales = float(linha.get('other_sales', 0)) if linha.get('other_sales', '').strip() else 0.0
            except ValueError:
                raise ValueError(f"other_sales inválido: {linha.get('other_sales')}")
            
            jogo = Jogo(
                jogo_id,
                linha['title'].strip(),
                linha['console'].strip(),
                linha['genre'].strip(),
                linha.get('publisher', 'N/A').strip(),
                linha.get('developer', 'N/A').strip(),
                critic_score,
                total_sales,
                na_sales,
                jp_sales,
                pal_sales,
                other_sales,
                linha.get('release_date', 'N/A').strip()
            )
            return jogo
        except ValueError as e:
            raise ValueError(f"Erro ao processar jogo: {e}")

    # ===========================
    # LISTAGEM E VISUALIZAÇÃO
    # ===========================

    def listarJogos(self):
        """
        Lista todos os jogos carregados no sistema.
        
        Returns:
            list: Lista de todos os jogos
        """
        if not self.jogos:
            print("📭 Nenhum jogo carregado no sistema.")
            return []
        
        print(f"\n{'='*80}")
        print(f"{'BIBLIOTECA DE JOGOS':^80}")
        print(f"{'='*80}")
        print(f"Total de jogos: {len(self.jogos)}\n")
        
        for idx, jogo in enumerate(self.jogos, 1):
            print(f"{idx}. {jogo.linhaBacklog()}")
        
        print(f"{'='*80}\n")
        return self.jogos

    # ===========================
    # BUSCAS
    # ===========================

    def buscarJogoPorNome(self, termo):
        """
        Busca jogos pelo nome (busca parcial, case-insensitive).
        
        Args:
            termo (str): Termo de busca
            
        Returns:
            list: Lista de jogos que correspondem ao termo
        """
        if not termo:
            print("⚠️  Termo de busca vazio!")
            return []
        
        termo_lower = termo.lower().strip()
        resultados = [j for j in self.jogos if termo_lower in j.titulo.lower()]
        
        if not resultados:
            print(f"❌ Nenhum jogo encontrado com o termo '{termo}'")
            return []
        
        print(f"\n🔍 {len(resultados)} jogo(s) encontrado(s) para '{termo}':")
        for jogo in resultados:
            jogo.exibir()
        
        return resultados

    def filtrarPorGenero(self, genero):
        """
        Filtra jogos por gênero.
        
        Args:
            genero (str): Gênero desejado
            
        Returns:
            list: Lista de jogos do gênero especificado
        """
        if not genero:
            print("⚠️  Gênero vazio!")
            return []
        
        genero_lower = genero.lower().strip()
        resultados = [j for j in self.jogos if j.genero.lower() == genero_lower]
        
        if not resultados:
            print(f"❌ Nenhum jogo encontrado no gênero '{genero}'")
            return []
        
        print(f"\n🎮 {len(resultados)} jogo(s) encontrado(s) no gênero '{genero}':")
        for jogo in resultados:
            jogo.exibir()
        
        return resultados

    def filtrarPorConsole(self, console):
        """
        Filtra jogos por console.
        
        Args:
            console (str): Console desejado
            
        Returns:
            list: Lista de jogos para o console especificado
        """
        if not console:
            print("⚠️  Console vazio!")
            return []
        
        console_lower = console.lower().strip()
        resultados = [j for j in self.jogos if j.console.lower() == console_lower]
        
        if not resultados:
            print(f"❌ Nenhum jogo encontrado para o console '{console}'")
            return []
        
        print(f"\n💾 {len(resultados)} jogo(s) encontrado(s) para '{console}':")
        for jogo in resultados:
            jogo.exibir()
        
        return resultados

    def filtrarPorNota(self, nota_minima):
        """
        Filtra jogos por nota mínima de crítica.
        
        Args:
            nota_minima (float): Nota mínima desejada (0-100)
            
        Returns:
            list: Lista de jogos com nota >= nota_minima
        """
        try:
            nota_minima = float(nota_minima)
            
            if nota_minima < 0 or nota_minima > 100:
                raise ValueError("Nota deve estar entre 0 e 100")
            
            resultados = [j for j in self.jogos if j.criticScore >= nota_minima]
            
            if not resultados:
                print(f"❌ Nenhum jogo encontrado com nota >= {nota_minima}")
                return []
            
            print(f"\n⭐ {len(resultados)} jogo(s) encontrado(s) com nota >= {nota_minima}:")
            for jogo in resultados:
                jogo.exibir()
            
            return resultados
            
        except ValueError as e:
            print(f"❌ Erro: {e}")
            return []

    # ===========================
    # ORDENAÇÃO
    # ===========================

    def ordenarJogos(self, criterio='titulo'):
        """
        Ordena e exibe os jogos conforme o critério especificado.
        
        Args:
            criterio (str): 'titulo', 'nota', 'vendas', 'console'
            
        Returns:
            list: Lista de jogos ordenada
        """
        criterios_validos = {
            'titulo': lambda j: j.titulo.lower(),
            'nota': lambda j: j.criticScore,
            'vendas': lambda j: j.totalVendas,
            'console': lambda j: j.console.lower(),
            'genero': lambda j: j.genero.lower()
        }
        
        if criterio.lower() not in criterios_validos:
            print(f"❌ Critério inválido. Válidos: {', '.join(criterios_validos.keys())}")
            return []
        
        # Determinar se deve ordenar decrescente para alguns critérios
        reverse = criterio.lower() in ['nota', 'vendas']
        
        jogos_ordenados = sorted(
            self.jogos,
            key=criterios_validos[criterio.lower()],
            reverse=reverse
        )
        
        print(f"\n📋 Jogos ordenados por {criterio}:")
        for idx, jogo in enumerate(jogos_ordenados, 1):
            print(f"{idx}. {jogo.titulo} ({jogo.console}) - Nota: {jogo.criticScore}")
        
        return jogos_ordenados

    # ===========================
    # BACKLOG
    # ===========================

    def adicionarAoBacklog(self, jogo):
        """
        Adiciona um jogo ao backlog.
        
        Args:
            jogo (Jogo): Objeto Jogo a adicionar
            
        Returns:
            bool: True se adicionado com sucesso
        """
        if not jogo:
            print("❌ Jogo inválido!")
            return False
        
        if self.backlog.contem(jogo.idJogo):
            print(f"⚠️  '{jogo.titulo}' já está no backlog!")
            return False
        
        self.backlog.enqueue(jogo)
        self.salvarBacklogTxt()
        print(f"✅ '{jogo.titulo}' adicionado ao backlog!")
        return True

    def mostrarBacklog(self):
        """
        Exibe o backlog de forma formatada.
        """
        if self.backlog.is_empty():
            print("📭 Backlog vazio!")
            return
        
        print(f"\n{'='*80}")
        print(f"{'BACKLOG':^80}")
        print(f"{'='*80}")
        self.backlog.mostrar()
        print(f"{'='*80}\n")

    def jogarProximo(self):
        """
        Remove o próximo jogo do backlog e o coloca no histórico de recentes.
        
        Returns:
            Jogo: Jogo removido ou None se backlog vazio
        """
        jogo = self.backlog.dequeue()
        if jogo:
            self.recentes.push(jogo)
            self.salvarBacklogTxt()
            self.salvarRecentesTxt()
            print(f"\n🎮 Jogando: {jogo.titulo}")
            return jogo
        else:
            print("❌ Backlog vazio! Nenhum jogo para jogar.")
            return None

    def salvarBacklog(self, nome_arquivo=None):
        """
        Salva o backlog em arquivo JSON.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se salvo com sucesso
        """
        arquivo = nome_arquivo or self._backlog_arquivo
        
        try:
            dados = {
                'timestamp': datetime.now().isoformat(),
                'backlog': [
                    {
                        'id': jogo.idJogo,
                        'titulo': jogo.titulo,
                        'console': jogo.console
                    }
                    for jogo in self.backlog.dados
                ]
            }
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Backlog salvo em '{arquivo}'!")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar backlog: {e}")
            return False

    def carregarBacklog(self, nome_arquivo=None):
        """
        Carrega o backlog a partir de um arquivo JSON.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se carregado com sucesso
        """
        arquivo = nome_arquivo or self._backlog_arquivo
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            backlog_ids = [item['id'] for item in dados.get('backlog', [])]
            
            for jogo in self.jogos:
                if jogo.idJogo in backlog_ids:
                    self.backlog.enqueue(jogo)
            
            print(f"✅ Backlog carregado de '{arquivo}' ({len(backlog_ids)} jogos)!")
            return True
        except FileNotFoundError:
            print(f"⚠️  Arquivo '{arquivo}' não encontrado.")
            return False
        except Exception as e:
            print(f"❌ Erro ao carregar backlog: {e}")
            return False

    # ===========================
    # SESSÕES
    # ===========================

    def registrarSessao(self, jogo, tempo, percentual, status):
        """
        Registra uma sessão de jogo.
        
        Args:
            jogo (Jogo): Jogo jogado
            tempo (float): Tempo em horas
            percentual (float): Percentual completado (0-100)
            status (str): Status ('pausado', 'completado', 'em progresso')
            
        Returns:
            bool: True se registrado com sucesso
        """
        try:
            if tempo < 0:
                raise ValueError("Tempo não pode ser negativo")
            if percentual < 0 or percentual > 100:
                raise ValueError("Percentual deve estar entre 0 e 100")
            if status.lower() not in ['pausado', 'completado', 'em progresso']:
                raise ValueError("Status inválido")
            
            sessao = SessaoJogo(jogo, tempo, percentual, status)
            self.sessoes.append(sessao)
            self.recentes.push(jogo)
            
            self.salvarHistoricoTxt()
            self.salvarRecentesTxt()
            
            print(f"✅ Sessão registrada para '{jogo.titulo}'")
            return True
        except ValueError as e:
            print(f"❌ Erro ao registrar sessão: {e}")
            return False

    def mostrarRecentes(self):
        """
        Exibe os jogos recentes (últimos jogados).
        """
        if self.recentes.is_empty():
            print("📭 Nenhum jogo recente!")
            return
        
        print(f"\n{'='*80}")
        print(f"{'JOGOS RECENTES':^80}")
        print(f"{'='*80}")
        self.recentes.mostrar()
        print(f"{'='*80}\n")

    def retomarUltimoJogo(self):
        """
        Retoma o último jogo jogado.
        
        Returns:
            Jogo: Último jogo ou None
        """
        if self.recentes.is_empty():
            print("❌ Nenhum jogo recente para retomar!")
            return None
        
        ultimo = self.recentes.dados[-1]
        print(f"🔄 Retomando: {ultimo.titulo}")
        return ultimo

    def salvarHistorico(self, nome_arquivo=None):
        """
        Salva o histórico de sessões em arquivo JSON.
        
        Args:
            nome_arquivo (str): Nome do arquivo (usa padrão se None)
            
        Returns:
            bool: True se salvo com sucesso
        """
        arquivo = nome_arquivo or self._historico_arquivo
        
        try:
            dados = {
                'timestamp': datetime.now().isoformat(),
                'sessoes': [
                    {
                        'jogo': sessao.jogo.titulo,
                        'tempo_horas': sessao.tempo,
                        'percentual': sessao.percentual,
                        'status': sessao.status,
                        'data': sessao.data
                    }
                    for sessao in self.sessoes
                ]
            }
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Histórico salvo em '{arquivo}'!")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar histórico: {e}")
            return False

    # ===========================
    # RECOMENDAÇÕES E RANKING
    # ===========================

    def recomendarJogos(self, genero=None, limite=5):
        """
        Recomenda jogos baseado em gênero e nota.
        
        Args:
            genero (str): Gênero específico (None para todos)
            limite (int): Número de recomendações
            
        Returns:
            list: Lista de jogos recomendados
        """
        if not self.jogos:
            print("❌ Nenhum jogo disponível para recomendação!")
            return []
        
        jogos_filtrados = self.jogos
        
        if genero:
            genero_lower = genero.lower()
            jogos_filtrados = [j for j in jogos_filtrados if j.genero.lower() == genero_lower]
        
        if not jogos_filtrados:
            print(f"❌ Nenhum jogo encontrado para recomendar com os critérios especificados!")
            return []
        
        recomendados = sorted(jogos_filtrados, key=lambda j: j.criticScore, reverse=True)[:limite]
        
        print(f"\n🌟 Recomendações" + (f" para {genero}" if genero else "") + f":")
        for idx, jogo in enumerate(recomendados, 1):
            print(f"{idx}. {jogo.titulo} ({jogo.console}) - ⭐ {jogo.criticScore}")
        
        return recomendados

    def gerarRanking(self, tipo='comportamento', limite=10):
        """
        Gera um ranking de jogos baseado em diferentes critérios.
        
        Args:
            tipo (str): 'comportamento', 'nota', 'vendas', 'jogos_mais_jogados', 
                       'generos', 'consoles', 'nota_historico'
            limite (int): Número de itens no ranking
            
        Returns:
            list: Lista com o ranking
        """
        if not self.jogos:
            print("❌ Nenhum jogo disponível para gerar ranking!")
            return []
        
        tipo = tipo.lower()
        
        # ===== RANKING COMPORTAMENTO DO USUÁRIO (padrão) =====
        if tipo == 'comportamento':
            print(f"\n{'='*80}")
            print(f"{'RANKING BASEADO EM COMPORTAMENTO DO USUÁRIO':^80}")
            print(f"{'='*80}")
            
            # 1. JOGOS MAIS JOGADOS
            print(f"\n🎮 TOP {limite} JOGOS MAIS JOGADOS:")
            jogos_jogados = {}
            for sessao in self.sessoes:
                if sessao.jogo.idJogo not in jogos_jogados:
                    jogos_jogados[sessao.jogo.idJogo] = {
                        'jogo': sessao.jogo,
                        'sessoes': 0,
                        'tempo_total': 0
                    }
                jogos_jogados[sessao.jogo.idJogo]['sessoes'] += 1
                jogos_jogados[sessao.jogo.idJogo]['tempo_total'] += sessao.tempo
            
            if jogos_jogados:
                ranking_jogados = sorted(
                    jogos_jogados.items(),
                    key=lambda x: (x[1]['sessoes'], x[1]['tempo_total']),
                    reverse=True
                )[:limite]
                
                for idx, (jogo_id, dados) in enumerate(ranking_jogados, 1):
                    print(f"{idx}. {dados['jogo'].titulo} ({dados['jogo'].console}) - "
                          f"{dados['sessoes']} sessões | {dados['tempo_total']:.1f}h")
            else:
                print("   📭 Nenhum jogo jogado ainda")
            
            # 2. GÊNERO COM MAIOR FREQUÊNCIA
            print(f"\n📚 GÊNEROS COM MAIOR FREQUÊNCIA:")
            generos_freq = {}
            for sessao in self.sessoes:
                genero = sessao.jogo.genero
                generos_freq[genero] = generos_freq.get(genero, 0) + 1
            
            if generos_freq:
                ranking_generos = sorted(
                    generos_freq.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:limite]
                
                for idx, (genero, freq) in enumerate(ranking_generos, 1):
                    print(f"{idx}. {genero} - {freq} sessões")
            else:
                print("   📭 Nenhum gênero com histórico de jogo")
            
            # 3. CONSOLES MAIS JOGADOS
            print(f"\n💾 CONSOLES MAIS JOGADOS:")
            consoles_freq = {}
            for sessao in self.sessoes:
                console = sessao.jogo.console
                consoles_freq[console] = consoles_freq.get(console, 0) + 1
            
            if consoles_freq:
                ranking_consoles = sorted(
                    consoles_freq.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:limite]
                
                for idx, (console, freq) in enumerate(ranking_consoles, 1):
                    print(f"{idx}. {console} - {freq} sessões")
            else:
                print("   📭 Nenhum console com histórico de jogo")
            
            # 4. TOP JOGOS POR NOTA (ENTRE OS JÁ JOGADOS)
            print(f"\n⭐ TOP {limite} JOGOS MAIS BEM AVALIADOS (ENTRE OS JÁ JOGADOS):")
            jogos_jogados_ids = set(sessao.jogo.idJogo for sessao in self.sessoes)
            jogos_avaliados = [j for j in self.jogos if j.idJogo in jogos_jogados_ids]
            
            if jogos_avaliados:
                ranking_nota_historico = sorted(
                    jogos_avaliados,
                    key=lambda j: j.criticScore,
                    reverse=True
                )[:limite]
                
                for idx, jogo in enumerate(ranking_nota_historico, 1):
                    # Encontra dados de sessão para este jogo
                    sessoes_jogo = [s for s in self.sessoes if s.jogo.idJogo == jogo.idJogo]
                    tempo = sum(s.tempo for s in sessoes_jogo)
                    print(f"{idx}. {jogo.titulo} ({jogo.console}) - ⭐ {jogo.criticScore} | {tempo:.1f}h")
            else:
                print("   📭 Nenhum jogo foi jogado para avaliar")
            
            print(f"\n{'='*80}\n")
            return []
        
        # ===== RANKING TRADICIONAL POR NOTA =====
        elif tipo == 'nota':
            ranking = sorted(self.jogos, key=lambda j: j.criticScore, reverse=True)[:limite]
            print(f"\n🏆 TOP {limite} JOGOS POR NOTA:")
            for idx, jogo in enumerate(ranking, 1):
                print(f"{idx}. {jogo.titulo} ({jogo.console}) - ⭐ {jogo.criticScore}")
            return ranking
        
        # ===== RANKING POR VENDAS =====
        elif tipo == 'vendas':
            ranking = sorted(self.jogos, key=lambda j: j.totalVendas, reverse=True)[:limite]
            print(f"\n💰 TOP {limite} JOGOS POR VENDAS:")
            for idx, jogo in enumerate(ranking, 1):
                print(f"{idx}. {jogo.titulo} ({jogo.console}) - 💵 ${jogo.totalVendas}M")
            return ranking
        
        # ===== RANKING JOGOS MAIS JOGADOS (ISOLADO) =====
        elif tipo == 'jogos_mais_jogados':
            jogos_jogados = {}
            for sessao in self.sessoes:
                if sessao.jogo.idJogo not in jogos_jogados:
                    jogos_jogados[sessao.jogo.idJogo] = {
                        'jogo': sessao.jogo,
                        'sessoes': 0,
                        'tempo_total': 0
                    }
                jogos_jogados[sessao.jogo.idJogo]['sessoes'] += 1
                jogos_jogados[sessao.jogo.idJogo]['tempo_total'] += sessao.tempo
            
            if not jogos_jogados:
                print("❌ Nenhum jogo foi jogado!")
                return []
            
            ranking = sorted(
                jogos_jogados.items(),
                key=lambda x: (x[1]['sessoes'], x[1]['tempo_total']),
                reverse=True
            )[:limite]
            
            print(f"\n🎮 TOP {limite} JOGOS MAIS JOGADOS:")
            for idx, (jogo_id, dados) in enumerate(ranking, 1):
                print(f"{idx}. {dados['jogo'].titulo} - {dados['sessoes']} sessões | {dados['tempo_total']:.1f}h")
            
            return [item[1]['jogo'] for item in ranking]
        
        # ===== RANKING GÊNEROS =====
        elif tipo == 'generos':
            generos_freq = {}
            for sessao in self.sessoes:
                genero = sessao.jogo.genero
                generos_freq[genero] = generos_freq.get(genero, 0) + 1
            
            if not generos_freq:
                print("❌ Nenhum gênero com histórico de jogo!")
                return []
            
            ranking = sorted(generos_freq.items(), key=lambda x: x[1], reverse=True)[:limite]
            
            print(f"\n📚 TOP {limite} GÊNEROS MAIS JOGADOS:")
            for idx, (genero, freq) in enumerate(ranking, 1):
                print(f"{idx}. {genero} - {freq} sessões")
            
            return []
        
        # ===== RANKING CONSOLES =====
        elif tipo == 'consoles':
            consoles_freq = {}
            for sessao in self.sessoes:
                console = sessao.jogo.console
                consoles_freq[console] = consoles_freq.get(console, 0) + 1
            
            if not consoles_freq:
                print("❌ Nenhum console com histórico de jogo!")
                return []
            
            ranking = sorted(consoles_freq.items(), key=lambda x: x[1], reverse=True)[:limite]
            
            print(f"\n💾 TOP {limite} CONSOLES MAIS JOGADOS:")
            for idx, (console, freq) in enumerate(ranking, 1):
                print(f"{idx}. {console} - {freq} sessões")
            
            return []
        
        # ===== RANKING NOTA HISTÓRICO =====
        elif tipo == 'nota_historico':
            jogos_jogados_ids = set(sessao.jogo.idJogo for sessao in self.sessoes)
            jogos_avaliados = [j for j in self.jogos if j.idJogo in jogos_jogados_ids]
            
            if not jogos_avaliados:
                print("❌ Nenhum jogo foi jogado para avaliar!")
                return []
            
            ranking = sorted(jogos_avaliados, key=lambda j: j.criticScore, reverse=True)[:limite]
            
            print(f"\n⭐ TOP {limite} JOGOS MAIS BEM AVALIADOS (ENTRE OS JÁ JOGADOS):")
            for idx, jogo in enumerate(ranking, 1):
                sessoes_jogo = [s for s in self.sessoes if s.jogo.idJogo == jogo.idJogo]
                tempo = sum(s.tempo for s in sessoes_jogo)
                print(f"{idx}. {jogo.titulo} ({jogo.console}) - ⭐ {jogo.criticScore} | {tempo:.1f}h")
            
            return ranking
        
        else:
            print(f"❌ Tipo de ranking inválido: {tipo}")
            print(f"   Opções válidas: comportamento, nota, vendas, jogos_mais_jogados, generos, consoles, nota_historico")
            return []

    # ===========================
    # DASHBOARD
    # ===========================

    def salvarTudo(self):
        """
        Salva todos os dados do sistema (backlog, histórico e recentes).
        
        Returns:
            bool: True se todos os dados foram salvos com sucesso
        """
        try:
            self.salvarBacklogTxt()
            self.salvarHistoricoTxt()
            self.salvarRecentesTxt()
            print(f"\n✅ Todos os dados foram salvos com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")
            return False

    def exibirDashboard(self):
        """
        Exibe um dashboard com resumo geral do sistema.
        """
        print(f"\n{'='*80}")
        print(f"{'DASHBOARD STEAMPY':^80}")
        print(f"{'='*80}")
        
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   • Total de jogos: {len(self.jogos)}")
        print(f"   • Backlog: {self.backlog.tamanho()} jogos")
        print(f"   • Sessões registradas: {len(self.sessoes)}")
        print(f"   • Jogos recentes: {self.recentes.tamanho()}")
        
        if self.jogos:
            nota_media = sum(j.criticScore for j in self.jogos) / len(self.jogos)
            vendas_total = sum(j.totalVendas for j in self.jogos)
            print(f"\n📈 DADOS DOS JOGOS:")
            print(f"   • Nota média: {nota_media:.2f}")
            print(f"   • Vendas totais: ${vendas_total:.2f}M")
            
            # Gêneros
            generos = set(j.genero for j in self.jogos)
            print(f"   • Gêneros disponíveis: {len(generos)}")
            
            # Consoles
            consoles = set(j.console for j in self.jogos)
            print(f"   • Consoles: {len(consoles)}")
        
        if self.sessoes:
            tempo_total = sum(s.tempo for s in self.sessoes)
            percentual_medio = sum(s.percentual for s in self.sessoes) / len(self.sessoes)
            print(f"\n🎮 SESSÕES:")
            print(f"   • Tempo total jogado: {tempo_total:.1f}h")
            print(f"   • Percentual médio: {percentual_medio:.1f}%")
        
        print(f"\n{'='*80}\n")