function disableButtons() {
    document.getElementById('all-way-back').setAttribute('disabled', 'disabled');
    document.getElementById('step-left').setAttribute('disabled', 'disabled');
    document.getElementById('step-right').setAttribute('disabled', 'disabled');
    document.getElementById('all-way-forward').setAttribute('disabled', 'disabled');
    document.getElementById('page-input').setAttribute('disabled', 'disabled');
}
function enableButtons() {
    document.getElementById('all-way-back').removeAttribute('disabled');
    document.getElementById('step-left').removeAttribute('disabled');
    document.getElementById('step-right').removeAttribute('disabled');
    document.getElementById('all-way-forward').removeAttribute('disabled');
    document.getElementById('page-input').removeAttribute('disabled');
}
function removeInputs(){
    for(var i = 11; i < 100; i++){ 
        if(!(i%10)) continue;
        var gridElement = document.querySelector('input[name="' + i + '"]');
        gridElement.style.color = 'black';
        gridElement.value = '';
    }
}


let assignment, variables, intermediate_domains, failed;
let grid_inputs;
let solvable;
let step_number;
let show_mistakes = false;

function cleanVariables(){
    grid_inputs = assignment = variables = intermediate_domains = failed = solvable = step_number = null;
}

function toggleMistakeVisibility(){
    show_mistakes = !show_mistakes;    
    if(step_number) changeStep(step_number);
}

let colors = Array.from({ length: 81 }, (_, index) => {
    const red = Math.sin(0.3 * index + 0) * 127 + 128;
    const green = Math.sin(0.3 * index + 2) * 127 + 128;
    const blue = Math.sin(0.3 * index + 4) * 127 + 128;
    return `rgb(${red | 0},${green | 0},${blue | 0})`;
});

function changeStep(step) {
    removeInputs();
    step = parseInt(step);
    if (!isNaN(step)) {
        var assignmentsLength = assignment ? assignment.length : 0;

        if (step < 0) {
            step = 0;
        }
        else if (step > assignmentsLength) {
            step = assignmentsLength;
        }
        step_number = step;
    }
    else step = 0;
    let idx = -1;
    grid_inputs.forEach(
        (input) => {
            let [gridNumber, value] = input;
            var gridElement = document.querySelector('input[name="' + gridNumber + '"]');
            gridElement.value = value;
        }
    )
    for(var i = 0; i < step; i++){ 
        let [gridNumber, value, guessed]  = assignment[i].flat()
        if(guessed) idx++;
        var gridElement = document.querySelector('input[name="' + gridNumber + '"]');
        gridElement.style.color = colors[idx];
        if(show_mistakes){ 
            value = String(value);
            if(failed[gridNumber]){
                failed[gridNumber].forEach((fail)=>value+=(','+String(fail)));
                gridElement.style.textDecoration = 'underline';
                gridElement.style.textDecorationColor = 'red';
            }
        }
        else gridElement.style.textDecoration = 'none';
        gridElement.value = value;
    }
    const pageInput = document.getElementById('page-input');
    pageInput.value = step;
}

window.onload = function() {
    var inputs = document.querySelectorAll('input[type="text"]');
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('input', function(event) {
            var input = event.target;
            var value = input.value.trim();
            if(String(value).match(/^[1-9](,[1-9])*,?$/)) input.value = value;
            else input.value = String(input.value).slice(0, -1);
            if (input.value.length > 1) {
                input.style.textDecoration = 'underline';
                input.style.textDecorationColor = 'red';
            } else {
                input.style.textDecoration = 'none';
            }
        });
    }
    document.getElementById('clear-all').addEventListener('click', function() {
            removeInputs()
        });
    document.getElementById('solve').addEventListener('click', function() {
        cleanVariables();
        const pageInput = document.getElementById('page-input');
        pageInput.value = null;
        var formData = {};
        var inputs = document.querySelectorAll('input[type="text"]');
        inputs.forEach(function(input) {
            formData[input.name] = input.value;
        });
        grid_inputs = Object.entries(formData).filter(([_,y]) => y!=='');
        fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if(data.solvable){
                assignment = data.assignment;
                variables = data.variables;
                intermediate_domains = data.intermediate_domains;
                failed = data.failed;
                enableButtons();
                // number of assignments which were "guessed"
                changeStep(assignment.length)
            }
            else{
                disableButtons();
                alert("This Sudoku grid is unsolvable!")
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}