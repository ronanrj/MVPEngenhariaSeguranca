/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/pacientes';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.pacientes.forEach(item => insertList(item.name,                                                
                                                item.age,
                                                item.sex,
                                                item.cp,
                                                item.trtbps,
                                                item.chol,
                                                item.fbs,
                                                item.restecg,
                                                item.thalachh,
                                                item.exng,
                                                item.oldpeak,
                                                item.outcome
                                              ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()




/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputName,
                        inputAge ,
                        inputSex,
                        inputCp, 
                        inputTrtbps,
                        inputChol,
                        inputFbs,
                        inputRestecg,
                        inputThalachh,
                        inputExng,
                        inputOldpeak
                        ) => {
    
  const formData = new FormData();
  formData.append('name', inputName);
  formData.append('age', inputAge);
  formData.append('sex', inputSex);
  formData.append('cp', inputCp);
  formData.append('trtbps', inputTrtbps);
  formData.append('chol', inputChol);
  formData.append('fbs', inputFbs );
  formData.append('restecg', inputRestecg );
  formData.append('thalachh', inputThalachh );
  formData.append('exng', inputExng );
  formData.append('oldpeak', inputOldpeak );

  let url = 'http://127.0.0.1:5000/paciente';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/paciente?name='+item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
  let inputName = document.getElementById("newInput").value;
  let inputAge = document.getElementById("newAge").value;
  let inputSex =	document.getElementById("newSex").value;
  let inputCp =	document.getElementById("newCp").value;
  let inputTrtbps =	document.getElementById("newTrtbps").value;
  let inputChol =	document.getElementById("newChol").value;
  let inputFbs =	document.getElementById("newFbs").value;
  let inputRestecg =	document.getElementById("newRestecg").value;
  let inputThalachh =	document.getElementById("newThalachh").value;
  let inputExng =	document.getElementById("newExng").value;
  let inputOldpeak =	document.getElementById("newOldpeak").value;

  // Verifique se o nome do produto já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/pacientes?nome=${inputName}`;
  fetch(checkUrl, {
    method: 'get'
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.pacientes && data.pacientes.some(item => item.name === inputName)) {
        alert("O paciente já está cadastrado.\nCadastre o paciente com um nome diferente ou atualize o existente.");
      } else if (inputName === '') {
        alert("O nome do paciente não pode ser vazio!");
      // } else if (isNaN(inputPreg) || isNaN(inputPlas) || isNaN(inputPres) || isNaN(inputSkin) || isNaN(inputTest) || isNaN(inputMass) || isNaN(inputPedi) || isNaN(inputAge)) {
      //   alert("Esse(s) campo(s) precisam ser números!");
      } else {
        insertList(inputName, inputAge, inputSex, inputCp, inputTrtbps, inputChol, inputFbs, inputRestecg, inputThalachh, inputExng, inputOldpeak);
        postItem(inputName, inputAge, inputSex, inputCp, inputTrtbps, inputChol, inputFbs, inputRestecg, inputThalachh, inputExng, inputOldpeak);
        alert("Item adicionado!");
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (namePatient,age,sex,cp,trtbps,chol,fbs,restecg,thalachh,exng,oldpeak,outcome) => {
  var item = [namePatient,age,sex,cp,trtbps,chol,fbs,restecg,thalachh,exng,oldpeak,outcome];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);


  document.getElementById("newInput").value = "";
  document.getElementById("newAge").value = "";
  document.getElementById("newSex").value = "";
  document.getElementById("newCp").value = "";
  document.getElementById("newTrtbps").value = "";
  document.getElementById("newChol").value = "";
  document.getElementById("newFbs").value = "";
  document.getElementById("newRestecg").value = "";
  document.getElementById("newThalachh").value = "";
  document.getElementById("newExng").value = "";
  document.getElementById("newOldpeak").value = "";

  removeElement();
}