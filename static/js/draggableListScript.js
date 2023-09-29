document.addEventListener("DOMContentLoaded", function () {
    fetch("/dbTask/")
        .then((response) => response.json())
        .then((data) => {
            if (data.tasks) {
                fillList(data.tasks);
            }
        });

    const createTaskButton = document.getElementById("createTask");
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

    submitCreateTaskButton = document.getElementById("submitCreateTaskButton");
    submitCreateTaskButton.addEventListener("click", function (event) {
        event.preventDefault();

        name = document.getElementById("taskName").value;
        description = document.getElementById("description").value;
        recurring = document.getElementById("flexSwitchCheckDefault").checked;
        time = document.getElementById("time").value;

        var dataToSend = {
            name: name,
            description: description,
            recurring: recurring,
            time: time,
        };

        fetch("/dbTask/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(dataToSend),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.message === "Task successfully created!") {
                    if (data.tasks) {
                        fillList(data.tasks);
                        taskDialog.close();
                    }
                }
            })
            .catch((error) => console.error(error));
    });

    function fillList(tasks) {
        const ul = document.querySelector(".sortableList"); // Get the unordered list element

        // Clear existing list items (optional)
        ul.innerHTML = "";

        tasks.forEach((task) => {
            // Create a new list item
            const li = document.createElement("li");
            li.classList.add("item");
            li.draggable = true;

            // Create the details div
            const detailsDiv = document.createElement("div");
            detailsDiv.classList.add("details");

            // Create the span for task name
            const span = document.createElement("span");
            span.textContent = task.name;

            // Append the span to the details div
            detailsDiv.appendChild(span);

            // Create the drag handle icon
            const dragIcon = document.createElement("i");
            dragIcon.classList.add("uil", "uil-draggabledots");

            // Append the details div and drag icon to the list item
            li.appendChild(detailsDiv);
            li.appendChild(dragIcon);

            // Append the list item to the unordered list
            ul.appendChild(li);
        })

        const items = document.querySelectorAll(".item");

        items.forEach((item) => {
            item.addEventListener("dragstart", () => {
                setTimeout(() => item.classList.add("dragging"), 0);
            });
            item.addEventListener("dragend", () => item.classList.remove("dragging"));
        });

        const initSortableList = (e) => {
            const draggingItem = ul.querySelector(".dragging");
            const siblings = [...ul.querySelectorAll(".item:not(.dragging)")];
            let nextSibling = null;

            // Calculate the position to insert the draggingItem based on mouseY position
            siblings.forEach((sibling) => {
                const boundingBox = sibling.getBoundingClientRect();
                const siblingMiddleY = boundingBox.top + boundingBox.height / 2;

                if (e.clientY > siblingMiddleY) {
                    nextSibling = sibling.nextElementSibling;
                }
            });

            // Check if draggingItem is at the very top or very bottom of the list
            const isDraggingToTop = e.clientY < siblings[0].getBoundingClientRect().top;
            const isDraggingToBottom = nextSibling === null;

            if (nextSibling !== draggingItem) {
                if (isDraggingToTop) {
                    // If dragging to the top, insert before the first item
                    ul.insertBefore(draggingItem, siblings[0]);
                } else if (isDraggingToBottom) {
                    // If dragging to the bottom, insert after the last item
                    ul.appendChild(draggingItem);
                } else {
                    // Otherwise, insert before nextSibling
                    ul.insertBefore(draggingItem, nextSibling);
                }
            }
        };

        ul.addEventListener("dragover", initSortableList);
    }
});
