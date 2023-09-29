document.addEventListener('DOMContentLoaded', function() {

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

    submitCreateTaskButton = document.getElementById('submitCreateTaskButton');
    submitCreateTaskButton.addEventListener('click', function(event) {
        event.preventDefault();

        name = document.getElementById("taskName").value;
        description = document.getElementById("description").value;
        recurring = document.getElementById("flexSwitchCheckDefault").checked;
        time = document.getElementById("time").value;

        var dataToSend = {
            name: name,
            description: description,
            recurring: recurring,
            time: time
        }

        fetch("/dbTask/", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend),
        })
        .then(response => response.json())
        .then(data => {
            alert("aaaa");
        })
        .catch(error => console.error(error));
    });
});
