function MarkAsCompleted(task_id) {

    let index = tasks.indexOf(task_id);
    const completedButton = document.getElementById(`${task_id}`);
    completedButton.disabled = false;
    for (let i=0; i<subtasks[index].length; i++) {
        if (!document.getElementById(`${subtasks[index][i]}`).checked) {
            completedButton.disabled = true;
            break;
        }
    }
}

document.addEventListener(
    "DOMContentLoaded",
    function() {
        for (let i=0; i<tasks.length; i++) {
            MarkAsCompleted(tasks[i]);
        }
    }
)