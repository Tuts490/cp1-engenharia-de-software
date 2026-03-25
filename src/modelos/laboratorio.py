class Laboratorio:
    """Modelo que representa um laboratório disponível"""
    
    def __init__(self, id, nome, capacidade, recursos, predio, andar):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade      # Número máximo de alunos
        self.recursos = recursos          # Lista de recursos (ex: ["projetor", "quadro"])
        self.predio = predio              # Prédio onde fica o lab
        self.andar = andar                # Andar do prédio
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "capacidade": self.capacidade,
            "recursos": self.recursos,
            "predio": self.predio,
            "andar": self.andar
        }
    
    @staticmethod
    def from_dict(dados):
        return Laboratorio(
            id=dados["id"],
            nome=dados["nome"],
            capacidade=dados["capacidade"],
            recursos=dados["recursos"],
            predio=dados["predio"],
            andar=dados["andar"]
        )
    
    def __repr__(self):
        recursos_str = ", ".join(self.recursos) if self.recursos else "Nenhum"
        return f" {self.nome} | Capacidade: {self.capacidade} | Recursos: {recursos_str} | Local: {self.predio} - {self.andar}º andar"