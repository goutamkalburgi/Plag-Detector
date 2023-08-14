// Wait for the DOM to be completely loaded before running the following code
document.addEventListener('DOMContentLoaded', (event) => {

    // Pre-defined menu and step class names
    const menus = ['step-menu1', 'step-menu2', 'step-menu3'];
    const steps = ['form-step-1', 'form-step-2', 'form-step-3'];

    // Iterate over each menu and bind click event listeners
    menus.forEach((menuClass, index) => {
        const menu = document.querySelector(`.${menuClass}`);
        menu.addEventListener('click', () => {

            // When a menu is clicked, activate the corresponding step and deactivate others
            steps.forEach((stepClass, stepIndex) => {
                if (stepIndex === index) {
                    activateStepMenu(menu, document.querySelector(`.${stepClass}`));
                } else {
                    deactivateStepMenu(document.querySelector(`.${menus[stepIndex]}`), document.querySelector(`.${stepClass}`));
                }
            });
        });
    });

    // Helper function to activate a step and its corresponding menu
    function activateStepMenu(stepMenu, step) {
        stepMenu.classList.add('active');
        step.classList.add('active');
    }

    // Helper function to deactivate a step and its corresponding menu
    function deactivateStepMenu(stepMenu, step) {
        stepMenu.classList.remove('active');
        step.classList.remove('active');
    }

    // Handle disabling of runButton based on userInput's value
    const userInput = document.getElementById('userIn');
    const runButton = document.getElementById('run-button');
    runButton.disabled = !userInput.value;

    // Disable or enable runButton based on whether userInput has a value
    userInput.addEventListener('input', function () {
        runButton.disabled = !userInput.value.trim();
    });

    const operationChoice = document.getElementById('operationChoice');
    const operationDescription = document.getElementById('operationDescription');

    function setDescriptionByChoice(value) {
        switch (value) {
            case "3":
                operationDescription.textContent = "This will extract the submissions of the sections, extract the individual submissions and flatten the directory such that all relevant programming files are in the main student submissions folder and run moss.";
                break;
            case "1":
                operationDescription.textContent = "It will only extract submissions and individual submissions and flatten the directory.";
                break;
            default:
                operationDescription.textContent = "";
                break;
        }
    }

    operationChoice.addEventListener('change', function () {
        setDescriptionByChoice(this.value);
    });

    // Set the initial description based on the default selected value
    setDescriptionByChoice(operationChoice.value);
});

// Main function to initiate the process
function run() {
    // Fetch the user input and selections
    const userIn = document.getElementById('userIn').value;
    const languageChoice = document.getElementById('languageChoice').value;
    const operationChoice = document.getElementById('operationChoice').value;

    // Display the loading indicator and change the UI tab
    displayLoading();
    changeTab();
    moveProgressBar();

    // Invoke the exposed Python function with the gathered input
    eel.main(userIn, languageChoice, operationChoice);
}

// Show loading state in the UI
function displayLoading() {
    const loading = document.getElementById('myProgress');
    const resultHTML = document.getElementById('result');
    const logContainer = document.getElementById('logContainer');

    loading.style.display = "block";
    resultHTML.innerHTML = "";
    resultHTML.href = "";
    logContainer.innerHTML = "";
}

// Switch to the second UI tab
function changeTab() {
    const stepMenuTwo = document.querySelector('.step-menu2');
    const changeTabEvent = new Event('click');
    stepMenuTwo.dispatchEvent(changeTabEvent);
}

// Asynchronous function to allow the user to select a directory
async function browseFolder() {
    const path = await eel.exposed_select_directory()();
    if (path) {
        document.getElementById('userIn').value = path;
        const userInput = document.getElementById('userIn');
        const inputEvent = new Event('input');
        userInput.dispatchEvent(inputEvent);
    }
}

// Progress bar functionality for indicating progress in the UI
let i = 0;
function moveProgressBar() {
    if (i === 0) {
        i = 1;
        const elem = document.getElementById("myBar");
        let width = 1;
        const id = setInterval(frame, 20);

        // Function to gradually increase the progress bar's width
        function frame() {
            if (width >= 90) {
                clearInterval(id);
                i = 0;
            } else {
                width++;
                elem.style.width = width + "%";
                elem.innerHTML = width + "%";
            }
        }
    }
}

eel.expose(completeProgressBar);
function completeProgressBar() {
    if (i === 0) {
        const elem = document.getElementById("myBar");
        let width = 91; // Starting at 90%
        const id = setInterval(frame, 20);

        // Function to increase the progress bar's width from 90% to 100%
        function frame() {
            if (width >= 100) {
                clearInterval(id);
                elem.innerHTML = "100%";
            } else {
                width++;
                elem.style.width = width + "%";
                elem.innerHTML = width + "%";
            }
        }
    } else {
        const intervalID = setInterval(() => {
            if (i === 0) {
                clearInterval(intervalID); // stop checking
                completeProgressBar(); // call moveProgressBar again
            }
        }, 100); // check every 100ms
    }
}

eel.expose(appendToLog);
function appendToLog(message, withTick) {
    const logContainer = document.getElementById('logContainer');
    const messageElement = document.createElement('p');

    messageElement.classList.add('margin-vertical-8', 'font-size-16');

    const tick = document.createElement('span');
    if (withTick) {
        tick.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 448 512"><!-- Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path fill="#008000" d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L160 338.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>'; // check svg
    } else {
        tick.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 384 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path fill="#ff0000" d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/></svg>'; // xmark svg
    }
    tick.firstChild.classList.add('tickSvg');  // Add the class to the SVG
    messageElement.appendChild(tick);

    // Look for content within single quotes, then determine if it's a URL.
    const urlRegex = /'(https?:\/\/[^']+)'/gi;

    // Look for content within single quotes, then determine if it's a directory path.
    const pathRegex = /'(([A-Z]:\\|\/)[^']+)'/gi;

    let modifiedMessage = message.replace(urlRegex, (match, group1) => `<a href="${group1}" target="_blank">${group1}</a>`);
    modifiedMessage = modifiedMessage.replace(pathRegex, (match, group1) => `<a href="file://${group1}" target="_blank">${group1}</a>`);

    messageElement.innerHTML += modifiedMessage;
    logContainer.appendChild(messageElement);
}