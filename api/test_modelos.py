# Importando as classes necessárias
import pandas as pd  # Faltava a importação do pandas
from model import *

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros    
url_dados_X = "./MachineLearning/data/X_test_dataset_heart.csv"
url_dados_y = "./MachineLearning/data/y_test_dataset_heart.csv"  # Arquivo com a coluna de saída
colunas = ['age', 'sex', 'cp', 'trtbps', 'chol', 'fbs', 'restecg', 'thalachh', 'exng', 'oldpeak']  # Incluindo apenas as colunas necessárias

# Carga dos dados - Incluindo a coluna 'output'
# Carga das features
dataset = carregador.carregar_dados(url_dados_X, colunas)
X = dataset.values  # Features

# Carga da coluna alvo
y = pd.read_csv(url_dados_y).values.ravel()  # Carregar a coluna de saída separadamente


# Verificando o shape dos dados
print(f"Shape de X: {X.shape}")  # Deve ser (n_samples, 10)
print(f"Shape de y: {y.shape}")  # Deve ser (n_samples,)

# Método para testar o modelo Naive Bayes a partir do arquivo correspondente
def test_modelo_nb():
    # Importando o pipeline salvo (que contém o scaler e o modelo)
    pipeline_path = './MachineLearning/pipelines/nb_heart_pipeline.pkl'
    modelo_pipeline = modelo.carrega_modelo(pipeline_path)

    # Avaliando o pipeline diretamente com os dados de teste
    acuracia_nb = avaliador.avaliar(modelo_pipeline, X, y)
    
    # Testando as métricas do Naive Bayes
    assert acuracia_nb >= 0.78
