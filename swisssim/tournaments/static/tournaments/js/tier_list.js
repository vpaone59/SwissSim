document.addEventListener('DOMContentLoaded', function () {
    const tierListId = 'tierlist-{{ tournament.id }}';
    let draggableItems = document.querySelectorAll('.draggable-item');
    let currentDraggedItem = null;

    // Load saved tier list from local storage
    loadTierList();

    // Initialize drag events
    draggableItems.forEach(item => {
        item.setAttribute('draggable', true);

        item.addEventListener('dragstart', function (e) {
            currentDraggedItem = this;
            this.classList.add('dragging');
            e.dataTransfer.setData('text/plain', this.innerHTML);
            e.dataTransfer.effectAllowed = 'move';
        });

        item.addEventListener('dragend', function () {
            this.classList.remove('dragging');
            currentDraggedItem = null;
            saveTierList(); // Save after drag completes
        });
    });

    // Make tier containers and team pool droppable
    const dropTargets = document.querySelectorAll('.tier-container, #teamPool');

    dropTargets.forEach(container => {
        container.addEventListener('dragover', function (e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            this.classList.add('dragover');
        });

        container.addEventListener('dragleave', function () {
            this.classList.remove('dragover');
        });

        container.addEventListener('drop', function (e) {
            e.preventDefault();
            this.classList.remove('dragover');

            if (currentDraggedItem) {
                // Find the row element inside the container
                const rowElement = this.querySelector('.row');
                if (rowElement) {
                    rowElement.appendChild(currentDraggedItem);
                }
            }
        });
    });

    // Reset button
    document.getElementById('reset-tierlist').addEventListener('click', function () {
        if (confirm('Are you sure you want to reset your tier list? This cannot be undone.')) {
            localStorage.removeItem(tierListId);
            const teamPool = document.getElementById('teamPool');

            // Move all teams back to team pool
            document.querySelectorAll('.tier-container .draggable-item').forEach(item => {
                teamPool.appendChild(item);
            });
        }
    });

    // Save button (explicitly save)
    document.getElementById('save-tierlist').addEventListener('click', function () {
        saveTierList();
        alert('Tier list saved!');
    });

    // Save tier list to local storage
    function saveTierList() {
        const tierData = {};

        document.querySelectorAll('.tier-container').forEach(container => {
            const tier = container.dataset.tier;
            const teamIds = [];

            container.querySelectorAll('.team-card').forEach(card => {
                teamIds.push(card.dataset.teamId);
            });

            tierData[tier] = teamIds;
        });

        localStorage.setItem(tierListId, JSON.stringify(tierData));
    }

    // Load tier list from local storage
    function loadTierList() {
        const savedData = localStorage.getItem(tierListId);

        if (savedData) {
            const tierData = JSON.parse(savedData);

            for (const tier in tierData) {
                const tierContainer = document.querySelector(`.tier-container[data-tier="${tier}"]`);
                if (tierContainer) {
                    const rowElement = tierContainer.querySelector('.row');

                    tierData[tier].forEach(teamId => {
                        const teamCard = document.querySelector(`.team-card[data-team-id="${teamId}"]`);

                        if (teamCard) {
                            const draggableItem = teamCard.closest('.draggable-item');
                            if (draggableItem && rowElement) {
                                rowElement.appendChild(draggableItem);
                            }
                        }
                    });
                }
            }
        }
    }
});