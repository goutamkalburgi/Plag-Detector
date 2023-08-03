function run() {
    let userIn = document.getElementById('userIn').value;
    let languageChoice = document.getElementById('languageChoice').value;
    let operationChoice = document.getElementById('operationChoice').value;
    eel.main(userIn, languageChoice, operationChoice);  // Call the exposed Python function
}
