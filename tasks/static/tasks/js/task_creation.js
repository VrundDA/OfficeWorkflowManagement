function renderTable() {
    let table = document.getElementById("subtasks-table");

    table.innerHTML = "";

    subtasks.forEach((task, index) => {
        table.innerHTML += `
            <tr>
                <td>${index+1}</td>
                <td class="subtask-complete">
                    <input class="form-check-input mt-0" type="checkbox" id="${index+1}" onchange="toggleFeature(${index+1})">
                </td>
                <td class="subtask-cell">
                    <label for="${index+1}">${task}</label>
                </td>
                <td>
                    <button onclick="editSubtask(${index})" class="btn btn-primary">Edit</button>
                    <button onclick="deleteSubtask(${index})" class="btn btn-danger">Delete</button>
                </td>
            </tr>
        `;
    });

    for (let i=0; i<subtasksComplete.length; i++) {
        const checkbox = document.getElementById(`${i+1}`);
        checkbox.checked = subtasksComplete[i];
    }
}

function deleteSubtask(index) {
    subtasks.splice(index,1);
    document.getElementById("subtasks-field").value = JSON.stringify(subtasks);
    document.getElementById("subtasks-field-complete").value = JSON.stringify(subtasksComplete);
    renderTable();  
}
function toggleFeature(index) {
    const checkbox = document.getElementById(`${index}`);
    if (checkbox.checked) {
        subtasksComplete[index-1] = true;
    }
    else {
        subtasksComplete[index-1] = false;
    }
    document.getElementById("subtasks-field-complete").value = JSON.stringify(subtasksComplete);
}
function addSubTask() {
    let text = document.getElementById("subtask-title").value;
    if (text) {
        subtasks.push(text);
    }
    const subtaskInput = document.getElementById("subtask-title");
    subtasksComplete.push(false);
    subtaskInput.value = "";
    document.getElementById("subtasks-field").value = JSON.stringify(subtasks)
    document.getElementById("subtasks-field-complete").value = JSON.stringify(subtasksComplete);
    renderTable();
}
function editSubtask(index) {
    let updated = prompt("Edit subtask", subtasks[index]);
    if (updated) {
        subtasks[index] = updated;
        document.getElementById("subtasks-field").value = JSON.stringify(subtasks)
        document.getElementById("subtasks-field-complete").value = JSON.stringify(subtasksComplete);
        renderTable();
    }
}

document.addEventListener(
    "DOMContentLoaded",
    function() {

        renderTable();

        document
            .getElementById("subtasks-field")
            .value =
            JSON.stringify(subtasks);
        document
            .getElementById("subtasks-field-complete")
            .value = 
            JSON.stringify(subtasksComplete);
    }
);