var positivo = document.getElementById('positivo')
var negativo = document.getElementById('negativo')
var descripcion = document.getElementById('descripcion')
var comboBox = document.getElementById('comboBox')


console.log('hola')

function Habilitar(){
    if(positivo.checked){
        console.log('1')
        comboBox.disabled = true;
    }

    else{
        comboBox.disabled = false;
    }
}