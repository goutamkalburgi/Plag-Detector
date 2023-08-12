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
    userInput.addEventListener('input', function() {
        runButton.disabled = !userInput.value.trim();
    });
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
      
      // Invoke the exposed Python function with the gathered input
      eel.main(userIn, languageChoice, operationChoice); 
  }
  
  // Show loading state in the UI
  function displayLoading() {
      const loading = document.getElementById('myProgress');
      const resultHTML = document.getElementById('result');
      const output = document.getElementById('output');
      
      loading.style.display = "block"; 
      resultHTML.innerHTML = "";
      resultHTML.href = "";
      output.innerHTML = "";
  }
  
  // Switch to the second UI tab
  function changeTab() {
      const stepMenuTwo = document.querySelector('.step-menu2');
      const changeTabEvent = new Event('click');
      stepMenuTwo.dispatchEvent(changeTabEvent);
      moveProgressBar(); 
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
  
  // Eel-exposed function to display the output result in the UI
  eel.expose(update_result);
  function update_result(result) {
      const userIn = document.getElementById('userIn').value;
      const resultHTML = document.getElementById('result');
      const loading = document.getElementById('myProgress');
      const output = document.getElementById('output');
      
      output.innerHTML = "Please find the output file in: " + userIn + "/results";
      loading.style.display = "none"; 
      const lines = result.split('\n');
      const lastLine = lines[lines.length - 2];
  
      resultHTML.href = lastLine;
      resultHTML.innerHTML = lastLine;
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
  