function normalize(text) {
    return text.toLowerCase().replace(/[^a-z0-9]/g,"");
}

function filterTasks() {
    const search = normalize(document.getElementById("task-search").value.toLowerCase());

    const cards = document.querySelectorAll(".task-card");

    cards.forEach(card => {
        const text = normalize(card.dataset.search.toLowerCase());
        if (text.includes(search)) {
            card.style.display = "";
        }
        else {
            card.style.display = "None";
        }
    });
}