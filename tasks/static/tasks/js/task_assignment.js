function assignTask(user_id, task_id, name) {

    if (user_id == 0) {
        document.getElementById(`assigned-user-${task_id}`).value = '';
        document.getElementById(`task-${task_id}`).value = task_id;

        const assignedPerson = document.getElementById(`assigned-person-${task_id}`);
        assignedPerson.textContent = `Assigned to: ${name}`;
    }

    document.getElementById(`assigned-user-${task_id}`).value = user_id;
    document.getElementById(`task-${task_id}`).value = task_id;
    
    const assignedPerson = document.getElementById(`assigned-person-${task_id}`);
    assignedPerson.textContent = `Assigned to: ${name}`;
}