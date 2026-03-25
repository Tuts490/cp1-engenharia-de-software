class Usuario:
    """Modelo que representa um usuário do sistema"""
    
    def __init__(self, rm, nome, email, senha, tipo="aluno"):
        self.rm = rm                    # Rm do aluno (identificador único)
        self.nome = nome                # Nome completo
        self.email = email              # E-mail institucional
        self.senha = senha              # Senha (em produção, usar hash)
        self.tipo = tipo                # "aluno" ou "coordenador"
    
    def to_dict(self):
        """Converte o objeto para dicionário (para salvar em JSON)"""
        return {
            "rm": self.rm,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "tipo": self.tipo
        }
    
    @staticmethod
    def from_dict(dados):
        """Cria um objeto Usuario a partir de um dicionário"""
        return Usuario(
            rm=dados["rm"],
            nome=dados["nome"],
            email=dados["email"],
            senha=dados["senha"],
            tipo=dados.get("tipo", "aluno")
        )
    
    def __repr__(self):
        return f"{self.nome} (RM: {self.rm})"