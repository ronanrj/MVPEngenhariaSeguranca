from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Pregnancies,Glucose,BloodPressure,SkinThickness,test,BMI,DiabetesPedigreeFunction,Age,Outcome

class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    name= Column("Name", String(50))
    age= Column("Age", Integer)
    sex = Column("Sex", Integer)
    cp = Column("Cp", Integer)
    trtbps = Column("Trtbps", Integer)
    chol = Column("Chol", Integer)
    fbs = Column("Fbs", Integer)
    restecg = Column("Restecg", Integer)
    thalachh = Column("Thalachh", Integer)
    exng = Column("Exng", Integer)
    oldpeak = Column("Oldpeak", Float)
    outcome = Column("Diagnostic", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, name:str,  age:int, sex:int, cp:int,
                 trtbps:int, chol:int, fbs:int, restecg:int, thalachh:int,
                 exng:int, oldpeak:float, outcome:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Paciente

        Arguments:
        name: Nome do paciente
            age: Idade da pessoa
            sex: Gênero da pessoa
            cp: Tipo de dor no peito
            trtbps: Pressão arterial em repouso (em mm Hg)
            chol: Colesterol em mg/dl obtido via sensor de IMC
            fbs: (Glicose em jejum > 120 mg/dl) (1 = verdadeiro; 0 = falso)
            restecg: Resultados do eletrocardiograma em repouso
            thalachh: Frequência cardíaca máxima alcançada
            exng: Angina induzida por exercício (1 = sim; 0 = não)
            oldpeak: Pico anterior
            outcome: Diagnostico
            data_insercao: Data em que o paciente foi inserido na base
        """
        self.name=name
        self.age = age
        self.sex = sex
        self.cp = cp
        self.trtbps = trtbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalachh = thalachh
        self.exng = exng
        self.oldpeak = oldpeak
        self.outcome = outcome

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao