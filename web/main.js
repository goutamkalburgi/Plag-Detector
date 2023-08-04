function run() {
    let userIn = document.getElementById('userIn').value;
    let languageChoice = document.getElementById('languageChoice').value;
    let operationChoice = document.getElementById('operationChoice').value;
    let loading = document.getElementById('myProgress');
    let resultHTML = document.getElementById('result');
    loading.style.display = "block"; 
    resultHTML.innerHTML = "";
    resultHTML.href = "";
    
    const stepMenuTwo = document.querySelector('.step-menu2');
    let changeTabEvent = new Event('click');
    stepMenuTwo.dispatchEvent(changeTabEvent);
    move(); 
    eel.main(userIn, languageChoice, operationChoice);  // Call the exposed Python function
}

async function browseFolder() {
    let path = await eel.select_directory()();
    console.log(path);
    if (path) {  // If path is not None or invalid
        document.getElementById('userIn').value = path;
        let userInput = document.getElementById('userIn');
        let inputEvent = new Event('input');
        userInput.dispatchEvent(inputEvent);

    }
}

eel.expose(update_result);
function update_result(result) {
    let resultHTML = document.getElementById('result');
    let loading = document.getElementById('myProgress');
    loading.style.display = "none"; 
    // Split the message into lines
    let lines = result.split('\n');

    // Get the last line of the message
    let lastLine = lines[lines.length - 2];

    resultHTML.href = lastLine;

    // Update the message box with the last line
    resultHTML.innerHTML = lastLine;
}

var i = 0;
function move() {
  if (i == 0) {
    i = 1;
    var elem = document.getElementById("myBar");
    var width = 1;
    var id = setInterval(frame, 10);
    function frame() {
      if (width >= 100) {
        clearInterval(id);
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
      }
    }
  }
}





