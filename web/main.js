function run() {
    let userIn = document.getElementById('userIn').value;
    let languageChoice = document.getElementById('languageChoice').value;
    let operationChoice = document.getElementById('operationChoice').value;
    eel.main(userIn, languageChoice, operationChoice);  // Call the exposed Python function
}

async function browseFolder() {
    let path = await eel.select_directory()();
    console.log(path);
    if (path) {  // If path is not None or invalid
        document.getElementById('userIn').value = path;
    }
}




