const items = document.querySelectorAll(".item");
const sortableList = document.querySelector(".sortableList");

items.forEach(item => {
    item.addEventListener("dragstart", () => {
        setTimeout(() => item.classList.add("dragging"), 0);
    });
    item.addEventListener("dragend", () => item.classList.remove("dragging"));
})

const initSortableList = (e) => {

    const draggingItem = sortableList.querySelector(".dragging");
    const siblings = [...sortableList.querySelectorAll(".item:not(.dragging)")];

    let nextSibling = siblings.find(sibling => {
        return e.clientY <= sibling.offsetTop + sibling.offsetHeight / 2;
    });

    sortableList.insertBefore(draggingItem, nextSibling);

}

sortableList.addEventListener("dragover", initSortableList);


const createTaskButton = document.getElementById('createTask');
const taskDialog = document.getElementById("taskDialog");
const closeDialogButton = document.getElementById("closeDialogButton");

createTaskButton.addEventListener("click", () => {
    // Show the dialog
    taskDialog.showModal();
});

closeDialogButton.addEventListener("click", () => {
    // Close the dialog
    taskDialog.close();
});

const form = taskDialog.querySelector("form");
form.addEventListener("submit", (event) => {
    event.preventDefault();

    try {
        const taskName = document.getElementById("taskName").value;
        const description = document.getElementById("description").value;
        const reoccurring = document.getElementById("flexSwitchCheckDefault").checked;
        const time = document.getElementById("time").value;

        // Create an object with the form data
        const dataToSend = {
            name: taskName,
            description: description,
            reoccurring: reoccurring,
            time: time
        };

        const url = '/tasks/'
        const response = fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend),
        });
        const gameState = response.json();

        if (response.ok) {
            const serverResponse = response.json(); 
        }
        else {
            console.error('Error sending POST request', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error sending move:', error);
    }
})

    
