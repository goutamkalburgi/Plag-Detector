document.addEventListener('DOMContentLoaded', (event) => {
  const stepMenuOne = document.querySelector('.step-menu1');
  const stepMenuTwo = document.querySelector('.step-menu2');
  const stepMenuThree = document.querySelector('.step-menu3');

  const stepOne = document.querySelector('.form-step-1');
  const stepTwo = document.querySelector('.form-step-2');
  const stepThree = document.querySelector('.form-step-3');

  stepMenuOne.addEventListener('click', function(){
    activateStepMenu(stepMenuOne, stepOne);
    deactivateStepMenu(stepMenuTwo, stepTwo);
    deactivateStepMenu(stepMenuThree, stepThree);
  });

  stepMenuTwo.addEventListener('click', function(){
    activateStepMenu(stepMenuTwo, stepTwo);
    deactivateStepMenu(stepMenuOne, stepOne);
    deactivateStepMenu(stepMenuThree, stepThree);
  });

  stepMenuThree.addEventListener('click', function(){
    activateStepMenu(stepMenuThree, stepThree);
    deactivateStepMenu(stepMenuOne, stepOne);
    deactivateStepMenu(stepMenuTwo, stepTwo);
  });

  function activateStepMenu(stepMenu, step){
    stepMenu.classList.add('active');
    step.classList.add('active');
  }

  function deactivateStepMenu(stepMenu, step){
    stepMenu.classList.remove('active');
    step.classList.remove('active');
  }
  const userInput = document.getElementById('userIn');
  const runButton = document.getElementById('run-button');

  // Start with the button disabled
  runButton.disabled = true;

  userInput.addEventListener('input', function() {
    if(userInput.value === '') {
      runButton.disabled = true;
    } else {
      runButton.disabled = false;
    }
  });
});
