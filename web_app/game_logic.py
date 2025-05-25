LIGHT_OFF = "\U0001F7E5"  # Red square
LIGHT_ON = "\U0001F7E8"   # Yellow square

class Game:
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.board = [[LIGHT_OFF for _ in range(cols)] for _ in range(rows)]

    def get_board(self):
        return self.board

    def _is_valid_cell(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def _get_neighbors(self, row, col):
        # Corrected to be 1-indexed for compatibility with original logic, then converted to 0-indexed
        # The original verificaBorda logic seems to be 1-indexed based on its usage.
        # However, the board here is 0-indexed. We need to be careful with conversion.
        # For simplicity, this internal logic will remain 0-indexed.
        # The toggle_cell method will handle 1-indexed input if that's how it's called from app.py

        neighbors = []
        # The cell itself
        neighbors.append((row, col))
        # Top
        if row > 0:
            neighbors.append((row - 1, col))
        # Bottom
        if row < self.rows - 1:
            neighbors.append((row + 1, col))
        # Left
        if col > 0:
            neighbors.append((row, col - 1))
        # Right
        if col < self.cols - 1:
            neighbors.append((row, col + 1))
        return neighbors

    def toggle_cell_and_neighbors(self, row, col):
        """
        Toggles the state of the cell at (row, col) and its direct N, S, E, W neighbors.
        Assumes row and col are 0-indexed.
        """
        if not self._is_valid_cell(row, col):
            # Or raise an error, depending on desired behavior
            return

        cells_to_toggle = []
        # The cell itself
        cells_to_toggle.append((row, col))
        # Top neighbor
        if row > 0:
            cells_to_toggle.append((row - 1, col))
        # Bottom neighbor
        if row < self.rows - 1:
            cells_to_toggle.append((row + 1, col))
        # Left neighbor
        if col > 0:
            cells_to_toggle.append((row, col - 1))
        # Right neighbor
        if col < self.cols - 1:
            cells_to_toggle.append((row, col + 1))
        
        for r, c in cells_to_toggle:
            if self._is_valid_cell(r, c):
                if self.board[r][c] == LIGHT_OFF:
                    self.board[r][c] = LIGHT_ON
                else:
                    self.board[r][c] = LIGHT_OFF

    def check_win(self):
        """
        Checks if all lights on the board are ON.
        Returns True if all lights are ON, False otherwise.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == LIGHT_OFF:
                    return False
        return True

    def reset_board(self):
        self.board = [[LIGHT_OFF for _ in range(self.cols)] for _ in range(self.rows)]

# Example usage (not part of the library, just for testing)
if __name__ == '__main__':
    game = Game()
    print("Initial board:")
    for row in game.get_board():
        print(row)

    print("\nToggling cell (0,0) (0-indexed):") # Corresponds to (1,1) in 1-indexed system
    game.toggle_cell_and_neighbors(0,0) # Toggles (0,0), (0,1), (1,0)
    for row in game.get_board():
        print(row)
    
    print(f"\nWin condition: {game.check_win()}")

    # Test case based on original verificaBorda for center piece (2,2) -> 0-indexed (1,1)
    # Original input (3,3) -> 0-indexed (2,2)
    # Expected toggles: (2,2), (1,2), (2,1), (3,2), (2,3)
    game.reset_board()
    print("\nToggling cell (2,2) (0-indexed):")
    game.toggle_cell_and_neighbors(2,2)
    # Expected:
    # X O X X X
    # O O O X X
    # X O X X X
    # X X X X X
    # X X X X X
    # (if original was all X)
    # After toggle:
    # board[2][2] = O
    # board[1][2] = O
    # board[2][1] = O
    # board[3][2] = O
    # board[2][3] = O
    for row_idx, row_val in enumerate(game.get_board()):
        print(f"Row {row_idx}: {row_val}")

    print(f"\nWin condition: {game.check_win()}")

    # Make all lights ON to test win condition
    # This is a bit of a hacky way to turn them all on for testing
    # by repeatedly toggling the center of a 3x3 subgrid
    # For a 5x5, this is more complex.
    # Let's manually set them for a clear win test
    game.board = [[LIGHT_ON for _ in range(5)] for _ in range(5)]
    print("\nAll lights ON board:")
    for row in game.get_board():
        print(row)
    print(f"Win condition: {game.check_win()}")
