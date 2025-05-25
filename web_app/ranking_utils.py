import os
from datetime import datetime

# Assuming ranking_jogo.txt is in the /app directory (root of the project)
# If app.py is in /app/web_app/, then the path from ranking_utils.py would be ../ranking_jogo.txt
# For now, let's try to keep it simple and assume it's in the same directory as where the app is run from,
# or use an absolute path if needed.
# Given the execution context, it's safer to assume it's at the root of the checkout.
RANKING_FILE_PATH = "/app/ranking_jogo.txt" # Use absolute path in the sandbox
MAX_RANKING_ENTRIES = 10 # Store top 10 scores

def get_rankings():
    """
    Reads ranking_jogo.txt, parses lines, sorts by moves (ascending),
    and returns a list of dictionaries.
    Each dictionary: {'name': str, 'moves': int, 'date': str}
    """
    if not os.path.exists(RANKING_FILE_PATH):
        # Create the file if it doesn't exist to prevent errors on first run
        try:
            with open(RANKING_FILE_PATH, "w", encoding="utf-8") as f:
                pass # Just create an empty file
        except IOError:
            # If running in a read-only environment or other permission issues
            return [] 


    rankings = []
    try:
        with open(RANKING_FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 3:
                    name, moves_str, date_str = parts
                    try:
                        moves = int(moves_str)
                        rankings.append({'name': name, 'moves': moves, 'date': date_str})
                    except ValueError:
                        print(f"Warning: Skipping malformed line in ranking file: {line}")
                        continue 
    except IOError:
        print(f"Warning: Could not read ranking file: {RANKING_FILE_PATH}")
        return [] # Return empty list if file cannot be read

    # Sort by moves (ascending), then by date (descending, optional, not in original)
    rankings.sort(key=lambda x: x['moves'])
    return rankings

def add_score(name, moves, date_str=None):
    """
    Adds a new score to ranking_jogo.txt, then re-sorts and truncates to MAX_RANKING_ENTRIES.
    name (str): Player's name
    moves (int): Number of moves
    date_str (str, optional): Date string. If None, current date/time will be used.
    """
    if date_str is None:
        # Using a simple date format, original used '%B %d, %Y %H:%M' with dateutil.tz
        # For simplicity and to avoid extra dependency, using standard datetime.
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    current_rankings = get_rankings() # This already handles empty/malformed entries

    # Check if player already exists with a better or equal score for the same name
    # The original code didn't explicitly handle this, it just added and re-sorted.
    # For now, let's stick to adding and re-sorting. User can have multiple entries.

    # Basic sanitization for name
    name = name.strip()
    if not name: # If name is empty after stripping, don't add score
        print("Warning: Empty name provided. Score not added.")
        return
    
    # Limit name length (e.g., to 50 characters)
    name = name[:50]
    
    new_entry = {'name': name, 'moves': moves, 'date': date_str}
    current_rankings.append(new_entry)
    
    # Sort by moves (ascending)
    current_rankings.sort(key=lambda x: x['moves'])
    
    # Keep only top N scores
    updated_rankings = current_rankings[:MAX_RANKING_ENTRIES]
    
    try:
        with open(RANKING_FILE_PATH, "w", encoding="utf-8") as f:
            for entry in updated_rankings:
                f.write(f"{entry['name']},{entry['moves']},{entry['date']}\n")
    except IOError:
        print(f"Warning: Could not write to ranking file: {RANKING_FILE_PATH}")
        # Decide how to handle this: maybe raise an exception or log more formally.
        # For now, the score might not be saved if this fails.

# --- Example Usage (for testing, not run when imported) ---
if __name__ == '__main__':
    # Test get_rankings with a non-existent or empty file
    print("Initial rankings (should be empty or from previous test):")
    print(get_rankings())
    print("-" * 20)

    # Test add_score
    print("Adding scores...")
    add_score("PlayerA", 15)
    add_score("PlayerB", 10)
    add_score("PlayerC", 20)
    add_score("PlayerD", 12, "2023-01-01 10:00:00") # Specific date

    print("\nRankings after adding initial scores:")
    for rank_entry in get_rankings():
        print(rank_entry)
    print("-" * 20)

    # Test adding more scores to see sorting and truncation
    print("Adding more scores to test truncation (MAX_RANKING_ENTRIES =", MAX_RANKING_ENTRIES, ")...")
    names = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12"]
    for i, name in enumerate(names):
        add_score(name, 5 + i*2) # Scores: 5, 7, 9, ..., 27

    print("\nFinal rankings (should be sorted and truncated):")
    final_ranks = get_rankings()
    for i, rank_entry in enumerate(final_ranks):
        print(f"{i+1}. {rank_entry}")
    
    assert len(final_ranks) <= MAX_RANKING_ENTRIES
    if len(final_ranks) > 1:
        assert final_ranks[0]['moves'] <= final_ranks[-1]['moves']

    print("\nTest completed. Check 'ranking_jogo.txt' file.")
