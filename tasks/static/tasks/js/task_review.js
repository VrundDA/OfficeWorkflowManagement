function ReviewTask(task_id) {

    const ReviewButton = document.getElementById(`${task_id}`);
    let index = tasks.indexOf(task_id);
    ReviewButton.disabled = false;
    for (let i=0; i<subtasks[index].length; i++) {
        if (!document.getElementById(`${subtasks[index][i]}`).checked) {
            ReviewButton.disabled = true;
            break;
        }
    }
}

document.addEventListener(
    "DOMContentLoaded",
    function() {
        for (let i=0; i<tasks.length; i++) {
            ReviewTask(tasks[i]);
        }
    }
)