let boton = document.getElementById("botón");
let Historial=document.getElementById("lista");
boton.addEventListener("click", agregarItem);
let lista = [];
let contador = 0;

function agregarItem() {
    // Obtener los valores de los campos del formulario
  try{
    
    let hist="\n";
    let texto = document.getElementById("texto").value;
    let numbers = document.getElementById("numbers").value;
    let fecha = document.getElementById("fecha").value;
    let opcion1 = document.getElementById("opcion1");
    let opcion2 = document.getElementById("opcion2");
    let opcion3 = document.getElementById("opcion3");
    let opciones = [opcion1, opcion2, opcion3];
    let valor = "";

    if (opcion1.checked) {
     valor = opcion1.value;
        } else if (opcion2.checked) {
          valor = opcion2.value;
        } else if (opcion3.checked) {
        valor = opcion3.value;
}
let item =texto + " " + numbers + " " + fecha + " " + valor;

    
  checkT(texto);
  checkOp(opciones);
  checkN(numbers);



  // Añadir el nuevo elemento a la lista
  lista.push(item);
  hist+=lista[contador];
  Historial.innerText+=hist;
  contador++;
  
}
catch(error){
alert(error)
}

}



//error en el rango de números
function checkN(numbers) {
    if(numbers==0){
      throw new Error("El argumento no debe ser nulo");
    }
    if (!(numbers >= 1 && numbers <= 10)) {
      throw new Error("El argumento debe estar entre 1 y 10");
    }
  }
  

//error en la longitud ed un texto
  function checkT(texto) {
    if (texto.length==0) {
      throw new Error( "El texto no debe ser nulo");
    }
    if(texto.length>=15){
      throw new Error("El texto no debe tener mas de 15 caracteres")
    }
  }
function checkOp(opciones){
  let ningunaMarcada = true;

  for (let i = 0; i < opciones.length; i++) {
    if (opciones[i].checked) {
      ningunaMarcada = false;
      break;
    }
  }
  if (ningunaMarcada)throw new Error("Sin opciones marcadas")
}
 