from datetime import datetime

class Reserva:
    """Modelo que representa uma reserva de laboratório"""
    
    def __init__(self, id, ra_aluno, id_laboratorio, data_inicio, data_fim, status="ativa"):
        self.id = id
        self.ra_aluno = ra_aluno
        self.id_laboratorio = id_laboratorio
        self.data_inicio = data_inicio    # Formato: "2024-03-25 14:00"
        self.data_fim = data_fim          # Formato: "2024-03-25 16:00"
        self.status = status              # "ativa", "cancelada", "concluida"
    
    def to_dict(self):
        return {
            "id": self.id,
            "ra_aluno": self.ra_aluno,
            "id_laboratorio": self.id_laboratorio,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim,
            "status": self.status
        }
    
    @staticmethod
    def from_dict(dados):
        return Reserva(
            id=dados["id"],
            ra_aluno=dados["ra_aluno"],
            id_laboratorio=dados["id_laboratorio"],
            data_inicio=dados["data_inicio"],
            data_fim=dados["data_fim"],
            status=dados.get("status", "ativa")
        )
    
    def __repr__(self):
        return f"Reserva #{self.id} | Lab {self.id_laboratorio} | {self.data_inicio} até {self.data_fim} | Status: {self.status}"