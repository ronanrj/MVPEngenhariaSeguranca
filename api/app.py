from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Adição, visualização, remoção e predição de pacientes com Diabetes")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de pacientes
@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_pacientes():
    """Lista todos os pacientes cadastrados na base
    Args:
       none
        
    Returns:
        list: lista de pacientes cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os pacientes")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os pacientes
    pacientes = session.query(Paciente).all()
    
    if not pacientes:
        # Se não houver pacientes
        return {"pacientes": []}, 200
    else:
        logger.debug(f"%d pacientes econtrados" % len(pacientes))
        print(pacientes)
        return apresenta_pacientes(pacientes), 200


# Rota de adição de paciente
@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: PacienteSchema):
    """Adiciona um novo paciente à base de dados
        Conjunto de dados de análise e previsão de ataque cardíaco

        Args:
            name (str): Nome do paciente
            age (int): Idade da pessoa
            sex (int): Gênero da pessoa (1 = homem; 0 = mulher)
            cp (int): Tipo de dor no peito:
                - Valor 1: angina típica
                - Valor 2: angina atípica
                - Valor 3: dor não anginosa
                - Valor 4: assintomático
            trtbps (int): Pressão arterial em repouso (em mm Hg)
            chol (int): Colesterol em mg/dl obtido via sensor de IMC
            fbs (int): Glicose em jejum > 120 mg/dl (1 = verdadeiro; 0 = falso)
            restecg (int): Resultados do eletrocardiograma em repouso:
                - Valor 0: normal
                - Valor 1: com anormalidade na onda ST-T (inversões da onda T e/ou elevação ou depressão do segmento ST de > 0,05 mV)
            thalachh (int): Frequência cardíaca máxima alcançada
            exng (int): Angina induzida por exercício (1 = sim; 0 = não)
            oldpeak (float): Pico anterior (valor real)
            diagnostic (int): Diagnóstico do paciente (0 = sem doença, 1 = com doença)

        Returns:
            dict: Representação do paciente e diagnóstico associado
    """
    #Instanciar as classes
    
    preProcessador = PreProcessador()
    pipeline = Pipeline()
    model = Model()

    # Recuperando os dados do formulário
    name = form.name
    age = form.age
    sex = form.sex
    cp = form.cp
    trtbps = form.trtbps
    chol = form.chol
    fbs = form.fbs
    restecg = form.restecg
    thalachh = form.thalachh
    exng = form.exng
    oldpeak = form.oldpeak
        
    # Preparando os dados para o modelo
    try:
        X_input = preProcessador.preparar_form(form)
        print(f"Dados processados para predição: {X_input}")
        logger.debug(f"Dados processados para predição: {X_input}")
    except ValueError as e:
        return {"message": f"Erro no preprocessamento: {str(e)}"}, 400
    # Carregando modelo
    model_path = './MachineLearning/pipelines/nb_heart_pipeline.pkl'
    try:
        modelo = pipeline.carrega_pipeline(model_path)
        logger.debug("Modelo carregado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar o modelo: {e}")
        return {"message": f"Erro ao carregar o modelo: {str(e)}"}, 400    
    # Realizando a predição
    try:
        outcome = int(model.preditor(modelo, X_input)[0])
        print(f"Valor predito pelo modelo: {outcome}")
        logger.debug(f"Predição realizada com sucesso: {outcome}")
    except Exception as e:
        logger.error(f"Erro na predição: {e}")
        return {"message": f"Erro na predição: {str(e)}"}, 400     
         
    paciente = Paciente(
        name = name,
        age = age,
        sex = sex,
        cp = cp,
        trtbps = trtbps,
        chol = chol,
        fbs = fbs,
        restecg = restecg,
        thalachh = thalachh,
        exng = exng,
        oldpeak = oldpeak,
        outcome = outcome
    )
    logger.debug(f"Adicionando produto de nome: '{paciente.name}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se paciente já existe na base
        if session.query(Paciente).filter(Paciente.name == form.name).first():
            error_msg = "Paciente já existente na base :/"
            logger.warning(f"Erro ao adicionar paciente '{paciente.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando paciente
        session.add(paciente)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado paciente de nome: '{paciente.name}'")
        return apresenta_paciente(paciente), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente '{paciente.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca de paciente por nome
@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):    
    """Faz a busca por um paciente cadastrado na base a partir do nome

    Args:
        nome (str): nome do paciente
        
    Returns:
        dict: representação do paciente e diagnóstico associado
    """
    
    paciente_nome = query.name
    logger.debug(f"Coletando dados sobre produto #{paciente_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    
    if not paciente:
        # se o paciente não foi encontrado
        error_msg = f"Paciente {paciente_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{paciente_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Paciente econtrado: '{paciente.name}'")
        # retorna a representação do paciente
        return apresenta_paciente(paciente), 200
   
    
# Rota de remoção de paciente por nome
@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteViewSchema, "404": ErrorSchema})
def delete_paciente(query: PacienteBuscaSchema):
    """Remove um paciente cadastrado na base a partir do nome

    Args:
        nome (str): nome do paciente
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    paciente_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre paciente #{paciente_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando paciente
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()
    
    if not paciente:
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente '{paciente_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(paciente)
        session.commit()
        logger.debug(f"Deletado paciente #{paciente_nome}")
        return {"message": f"Paciente {paciente_nome} removido com sucesso!"}, 200
    
if __name__ == '__main__':
    app.run(debug=True)