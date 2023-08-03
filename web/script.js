const stepMenuOne = document.querySelector('.formbold-step-menu1')
const stepMenuTwo = document.querySelector('.formbold-step-menu2')
const stepMenuThree = document.querySelector('.formbold-step-menu3')

const stepOne = document.querySelector('.formbold-form-step-1')
const stepTwo = document.querySelector('.formbold-form-step-2')
const stepThree = document.querySelector('.formbold-form-step-3')

const formSubmitBtn = document.querySelector('.formbold-btn')
const formBackBtn = document.querySelector('.formbold-back-btn')

stepMenuOne.addEventListener('click', function(){
activateStepMenu(stepMenuOne, stepOne);
deactivateStepMenu(stepMenuTwo, stepTwo);
deactivateStepMenu(stepMenuThree, stepThree);
formSubmitBtn.textContent = 'Next Step';
});

stepMenuTwo.addEventListener('click', function(){
activateStepMenu(stepMenuTwo, stepTwo);
deactivateStepMenu(stepMenuOne, stepOne);
deactivateStepMenu(stepMenuThree, stepThree);
formSubmitBtn.textContent = 'Next Step';
});

stepMenuThree.addEventListener('click', function(){
activateStepMenu(stepMenuThree, stepThree);
deactivateStepMenu(stepMenuOne, stepOne);
deactivateStepMenu(stepMenuTwo, stepTwo);
formSubmitBtn.textContent = 'Submit';
});

formSubmitBtn.addEventListener("click", function(event){
event.preventDefault()
if(stepMenuOne.className == 'formbold-step-menu1 active') {
    activateStepMenu(stepMenuTwo, stepTwo);
    deactivateStepMenu(stepMenuOne, stepOne);
} else if(stepMenuTwo.className == 'formbold-step-menu2 active') {
    activateStepMenu(stepMenuThree, stepThree);
    deactivateStepMenu(stepMenuTwo, stepTwo);
} else if(stepMenuThree.className == 'formbold-step-menu3 active') {
    document.querySelector('form').submit()
}
})

formBackBtn.addEventListener("click", function (event) {
event.preventDefault()

if(stepMenuTwo.className == 'formbold-step-menu2 active') {
    activateStepMenu(stepMenuOne, stepOne);
    deactivateStepMenu(stepMenuTwo, stepTwo);
    formBackBtn.classList.remove('active')
} else if(stepMenuThree.className == 'formbold-step-menu3 active') {
    activateStepMenu(stepMenuTwo, stepTwo);
    deactivateStepMenu(stepMenuThree, stepThree);
}
})

function activateStepMenu(stepMenu, step){
stepMenu.classList.add('active');
step.classList.add('active');
formBackBtn.classList.add('active');
}

function deactivateStepMenu(stepMenu, step){
stepMenu.classList.remove('active');
step.classList.remove('active');
}
