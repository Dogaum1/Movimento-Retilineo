var button_style = 
`
background-color: #2ea44f; 
border: 1px solid rgba(27, 31, 35, .15); 
border-radius: 6px;
box-shadow: rgba(27, 31, 35, .1) 0 1px 0;
box-sizing: border-box;
color: #fff;
cursor: pointer;
display: inline-block;
font-family: -apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji";
font-size: 14px;
font-weight: 600;
line-height: 20px;
padding: 6px 16px;
position: relative;
text-align: center;
text-decoration: none;
user-select: none;
-webkit-user-select: none;
touch-action: manipulation;
vertical-align: middle;
white-space: nowrap;
`
var label_style = 
`
    background-color: rgb(0, 105, 146);
    color: white;
    border: 1px solid rgba(27, 31, 35, 0.15);
    border-radius: 6px;
    line-height: 20px;
    height: 22px;
    padding: 6px 16px;
    text-align: center;
    display: inline-block;
    margin-right: -20px;
`
var input_style = 
`
    color: black;
    background: white;
    border-radius: 6px;
    font-size: 14px;
    line-height: 20px;
    padding: 6px 16px;
    text-align: center;
    width: 100;
`

var buttons = document.getElementsByTagName('button');

for (let i = 0; i < buttons.length; i++) {
    let button = buttons[i];
    button.style.cssText = button_style
    if(button.innerText == "Executar"){
        var run_button = button
    }
}

for(let i = 1; i <= 4; i++){
    var object = document.getElementById(i);
    if(i % 2 == 0){
        object.style.cssText = input_style
    }else{
        object.style.cssText = label_style
    }
}

var aceleration_variation_label = document.getElementById('8');
aceleration_variation_label.style.cssText = label_style
aceleration_variation_label.style.cssText += 'width: 1100px;'

var graph_style = `margin: 30px; box-shadow: 2px 2px 15px black;`

var graph_id_list = ['graph0', 'graph1', 'graph2']
for(let i = 0; i < 3; i++){
    var object = document.getElementById(graph_id_list[i]);
    console.log(object)
    object.style.cssText += graph_style
}

var body = document.body
body_style = document.createElement('style');
body_style.type = 'text/css';
body.appendChild(body_style);
body.style.cssText = 'text-align: -webkit-center;'

var msg = ""
run_button.onclick = function readyToRun(){
    msg = ""
    if(object_initial_aceleration_input.value == ""){
        msg += "Informe a aceleração do objeto!\n"
    }
    if(isNaN(object_initial_aceleration_input.value)){
        msg += "Digite apenas numeros para informar a aceleração!\n"
    }
    if(object_initial_velocity_input.value == ""){
        msg += "Informe a avelocidade inicial do objeto!\n"
    }
    if(isNaN(object_initial_velocity_input.value)){
        msg += "Digite apenas numeros para informar a velocidade inicial!"
    }
    if(!msg == ""){
        alert(msg)
    }
}