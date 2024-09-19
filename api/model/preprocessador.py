from sklearn.model_selection import train_test_split
import pickle
import numpy as np

class PreProcessador:

    def separa_teste_treino(self, dataset, percentual_teste, seed=7):
        """ Cuida de todo o pré-processamento. """
 
        # Aqui está sendo chamando uma função que vai dividir os dados em treino e teste.
        # O método `__preparar_holdout` faz a divisão de forma aleatória, 
        # garantindo que uma parte dos dados seja usada para treinar o modelo 
        # e a outra parte para testar o desempenho dele.
        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(dataset,
                                                                  percentual_teste,
                                                                  seed)
        # normalização/padronização        
        return (X_train, X_test, Y_train, Y_test)
    
    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """ Divide os dados em treino e teste usando o método holdout.
        Assume que a variável target está na última coluna.
        O parâmetro test_size é o percentual de dados de teste.
        """
        
        dados = dataset.values
        X = dados[:, 0:-1]
        Y = dados[:, -1]
        return train_test_split(X, Y, test_size=percentual_teste, random_state=seed)
    
    def preparar_form(self,form):
        """ Prepara os dados recebidos do front para serem usados no modelo. """
        X_input = np.array([form.age,
                            form.sex,
                            form.cp,
                            form.trtbps,
                            form.chol,
                            form.fbs,
                            form.restecg,
                            form.thalachh,
                            form.exng,
                            form.oldpeak
                        ])
        
        # Print dos dados recebidos
        print("Dados recebidos do formulário:", X_input)
        
        # O modelo de Machine Learning espera receber os dados de entrada
        # em um formato específico, como se fossem várias linhas de dados (amostras).
        # Mesmo que estejamos passando apenas uma amostra, precisamos "ajustar" a forma dos dados
        # para que o modelo entenda que é uma única linha com várias colunas .
        # O `reshape(1, -1)` faz exatamente isso: ele transforma o input em uma matriz de 1 linha e várias colunas.
        X_input = X_input.reshape(1, -1)
        return X_input
    
    def scaler(self,X_train):
        """ Normaliza os dados. """
        # normalização/padronização
        scaler = pickle.load(open('./MachineLearning/scalers/standard_scaler_heart.pkl', 'rb'))
        reescaled_X_train = self.scaler.transform(X_train)
        return reescaled_X_train
