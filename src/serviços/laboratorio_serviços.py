import json
from ..modelos.laboratorio import Laboratorio

class LaboratorioService:
    """Gerencia os laboratórios disponíveis"""
    
    ARQUIVO_DADOS = "src/data/laboratorios.json"
    
    def __init__(self):
        self.laboratorios = []
        self.carregar_laboratorios()
    
    def carregar_laboratorios(self):
        """Carrega os laboratórios do arquivo JSON"""
        try:
            with open(self.ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.laboratorios = [Laboratorio.from_dict(lab) for lab in dados]
        except FileNotFoundError:
            self.laboratorios = []
            self.criar_laboratorios_iniciais()
    
    def salvar_laboratorios(self):
        """Salva os laboratórios no arquivo JSON"""
        with open(self.ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            json.dump([lab.to_dict() for lab in self.laboratorios], f, indent=2, ensure_ascii=False)
    
    def criar_laboratorios_iniciais(self):
        """Cria laboratórios de exemplo"""
        self.laboratorios = [
            Laboratorio(1, "Lab de Informática - A", 30, ["computadores", "projetor"], "Paulista", 2),
            Laboratorio(2, "Lab de Informática - B", 30, ["computadores"], "Paulista", 2),
            Laboratorio(3, "Lab de Redes", 20, ["equipamentos de rede", "projetor"], "Paulista", 3),
            Laboratorio(4, "Lab de IoT", 15, ["Arduinos", "sensores"], "Vila Olímpia", 1),
            Laboratorio(5, "Sala de Estudos", 40, ["quadro branco", "mesas grandes"], "Paulista", 1),
        ]
        self.salvar_laboratorios()
    
    def listar_todos(self):
        """Retorna todos os laboratórios"""
        return self.laboratorios
    
    def buscar_por_id(self, id_lab):
        """Busca um laboratório pelo ID"""
        for lab in self.laboratorios:
            if lab.id == id_lab:
                return lab
        return None
    
    def listar_por_capacidade(self, min_capacidade):
        """Filtra laboratórios por capacidade mínima"""
        return [lab for lab in self.laboratorios if lab.capacidade >= min_capacidade]
    
    def exibir_todos(self):
        """Exibe todos os laboratórios formatados"""
        if not self.laboratorios:
            print("Nenhum laboratório cadastrado.")
            return
        
        print("\n" + "="*60)
        print("📋 LABORATÓRIOS DISPONÍVEIS")
        print("="*60)
        for lab in self.laboratorios:
            print(f"\n[{lab.id}] {lab}")
        print("\n" + "="*60)