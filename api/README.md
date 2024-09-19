# ProjetoMVP - análise e previsão de ataque cardíaco
ProjetoMVP - Este projeto faz parte da entrega para conclusão do mvp da sprint Qualidade de Software, Segurança e Sistemas Inteligentes do curso de pós graduação da PUC RIO. O objetivo do projeto é a análise e previsão de ataque cardíaco, no qual por uma entrada de um formulário, a api utilizando um modelo já treinado, analisa os dados de entrada e  retorna a possibilidade do usuário ter um ataque cardíaco.

##  Dataset utilizado

> https://www.kaggle.com/datasets/rashikrahmanpritom/heart-attack-analysis-prediction-dataset
---
## Como executar 

Após clonar o repositório, é necessário ir ao diretório raiz da api, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

> Ambiente virtual Python

Cria o ambiente virtual com o comando
```
 python -m venv env
```

Após, ativar o ambiente com o comando no powershell
```
.\env\Scripts\Activate.ps1
```

Após, será necessário ter todas as libs python listadas no `requirements.txt` instaladas.

```
(env)$ pip install -r requirements.txt
```

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

# Projeto FrontEnd - análise e previsão de ataque cardíaco

Projeto - análise e previsão de ataque cardíaco com consumo de api

## Como executar

Basta fazer o download do projeto e abrir o arquivo index.html no seu browser.
