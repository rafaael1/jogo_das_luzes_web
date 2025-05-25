document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('game-board');
    const moveCounterElement = document.getElementById('move-counter');
    const resetButton = document.getElementById('reset-button');
    const numRows = 5; // Should ideally come from server or be consistent
    const numCols = 5; // Should ideally come from server or be consistent

    const LIGHT_OFF_CSS_CLASS = 'light-off';
    const LIGHT_ON_CSS_CLASS = 'light-on';

    let boardState = []; // 2D array representing the board characters (e.g., 'X', 'O')
    let moves = 0;
    let SERVER_LIGHT_ON_CHAR = ''; // To be fetched from server
    let SERVER_LIGHT_OFF_CHAR = ''; // To be fetched from server

    async function fetchInitialGameState() {
        try {
            const response = await fetch('/api/gamestate');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            boardState = data.board;
            moves = data.moves;
            SERVER_LIGHT_ON_CHAR = data.light_on_char;
            SERVER_LIGHT_OFF_CHAR = data.light_off_char;
            updateMoveCounter();
            renderBoard();
        } catch (error) {
            console.error("Error fetching initial game state:", error);
            // Display error to user or retry
        }
    }

    function renderBoard() {
        boardElement.innerHTML = ''; // Clear previous board
        if (!boardState || boardState.length === 0) {
            console.error("Board state is not initialized or empty.");
            return;
        }
        for (let r = 0; r < numRows; r++) {
            for (let c = 0; c < numCols; c++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                // Determine class based on character from server
                if (boardState[r][c] === SERVER_LIGHT_ON_CHAR) {
                    cell.classList.add(LIGHT_ON_CSS_CLASS);
                } else {
                    cell.classList.add(LIGHT_OFF_CSS_CLASS);
                }
                cell.dataset.row = r;
                cell.dataset.col = c;
                cell.addEventListener('click', handleCellClick);
                boardElement.appendChild(cell);
            }
        }
    }

    function updateMoveCounter() {
        moveCounterElement.textContent = moves;
    }

    function setBoardInteractive(isInteractive) {
        const cells = boardElement.querySelectorAll('.cell');
        if (isInteractive) {
            boardElement.classList.remove('disabled'); // Assuming 'disabled' class on boardElement to block clicks
            cells.forEach(cell => cell.classList.remove('disabled')); // Or on individual cells
        } else {
            boardElement.classList.add('disabled');
            cells.forEach(cell => cell.classList.add('disabled'));
        }
    }

    async function handleCellClick(event) {
        // If the board or cell is already disabled, do nothing
        if (event.target.classList.contains('disabled') || boardElement.classList.contains('disabled')) {
            return;
        }

        const row = parseInt(event.target.dataset.row);
        const col = parseInt(event.target.dataset.col);

        setBoardInteractive(false); // Disable board

        try {
            const response = await fetch(`/api/click/${row}/${col}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            boardState = data.board;
            moves = data.moves;
            
            updateMoveCounter();
            renderBoard(); // This will re-enable cells if they are individually managed or just redraw

            if (data.win) {
                // Board remains non-interactive until after prompt and score submission/cancellation
                setTimeout(async () => { // Make this async to await fetch
                    const playerName = window.prompt(`Congratulations! You won in ${data.moves} moves!\nEnter your name for the leaderboard:`);
                    if (playerName && playerName.trim() !== "") {
                        // No explicit button to disable for prompt, browser handles modal nature
                        try {
                            const submitResponse = await fetch('/api/submit_score', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({ name: playerName.trim(), moves: data.moves }),
                            });
                            const submitResult = await submitResponse.json();
                            if (submitResponse.ok && submitResult.success) {
                                alert(submitResult.message + "\nYou will now be redirected to the ranking page.");
                                window.location.href = '/ranking'; // Redirect to ranking page
                            } else {
                                alert("Failed to submit score: " + (submitResult.message || "Unknown error"));
                                setBoardInteractive(true); // Re-enable board if score submission fails and user stays on page
                            }
                        } catch (submitError) {
                            console.error("Error submitting score:", submitError);
                            alert("An error occurred while submitting your score.");
                            setBoardInteractive(true); // Re-enable board
                        }
                    } else {
                        alert("You won, but your score was not saved because no name was provided.");
                        setBoardInteractive(true); // Re-enable board as game is over but score not saved
                    }
                }, 100); // Small delay to allow UI update before prompt
            } else {
                 setBoardInteractive(true); // Re-enable board if not a win
            }
        } catch (error) {
            console.error("Error during cell click:", error);
            alert("An error occurred during your move. Please try again."); // User-friendly message
            setBoardInteractive(true); // Re-enable board on error
        }
    }
    
    async function handleResetGame() {
        resetButton.disabled = true; // Disable reset button
        try {
            const response = await fetch('/api/reset');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            boardState = data.board;
            moves = data.moves;
            updateMoveCounter();
            renderBoard(); // This will redraw the board, implicitly making it interactive again
        } catch (error) {
            console.error("Error resetting game:", error);
            alert("Failed to reset game. Please try again.");
        } finally {
            resetButton.disabled = false; // Re-enable reset button
            setBoardInteractive(true); // Ensure board is interactive
        }
    }

    resetButton.addEventListener('click', handleResetGame);

    // Initial setup: Fetch game state from server
    fetchInitialGameState();
});
