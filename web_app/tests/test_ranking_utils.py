import unittest
import os
from datetime import datetime

# Adjust the import path based on how tests will be run.
# If running `python -m unittest discover web_app.tests` from /app,
# then web_app.ranking_utils should be accessible.
# However, ranking_utils itself uses "/app/ranking_jogo.txt".
# We need to import the module in a way that we can patch its RANKING_FILE_PATH.
from web_app import ranking_utils
from web_app.ranking_utils import MAX_RANKING_ENTRIES # Import the constant

class TestRankingUtils(unittest.TestCase):

    def setUp(self):
        # Store the original RANKING_FILE_PATH and set a test-specific one
        self.original_ranking_file_path = ranking_utils.RANKING_FILE_PATH
        self.test_ranking_file_path = "/app/test_ranking_jogo.txt"  # Test file at /app root
        ranking_utils.RANKING_FILE_PATH = self.test_ranking_file_path

        # Ensure the test ranking file is clean before each test
        if os.path.exists(self.test_ranking_file_path):
            os.remove(self.test_ranking_file_path)

    def tearDown(self):
        # Restore the original RANKING_FILE_PATH
        ranking_utils.RANKING_FILE_PATH = self.original_ranking_file_path

        # Clean up the test ranking file after each test
        if os.path.exists(self.test_ranking_file_path):
            os.remove(self.test_ranking_file_path)

    def test_get_rankings_non_existent_file(self):
        """Test get_rankings when the ranking file does not exist."""
        # setUp ensures the file does not exist initially
        rankings = ranking_utils.get_rankings()
        self.assertEqual(rankings, [])
        # get_rankings is expected to create the file if it doesn't exist
        self.assertTrue(os.path.exists(self.test_ranking_file_path))

    def test_get_rankings_empty_file(self):
        """Test get_rankings when the ranking file is empty."""
        # Create an empty file
        open(self.test_ranking_file_path, 'w', encoding='utf-8').close()
        
        rankings = ranking_utils.get_rankings()
        self.assertEqual(rankings, [])

    def test_get_rankings_valid_entries(self):
        """Test get_rankings with a file containing valid entries."""
        valid_entries_data = [
            {'name': "PlayerB", 'moves': 5, 'date': "2023-01-02 10:00:00"},
            {'name': "PlayerA", 'moves': 10, 'date': "2023-01-01 12:00:00"},
            {'name': "PlayerC", 'moves': 15, 'date': "2023-01-03 14:00:00"},
        ]
        # The get_rankings function sorts by moves, so prepare data accordingly for assertion
        expected_sorted_rankings = sorted(valid_entries_data, key=lambda x: x['moves'])

        with open(self.test_ranking_file_path, 'w', encoding='utf-8') as f:
            # Write entries in a potentially unsorted manner to also test sorting by get_rankings
            f.write("PlayerA,10,2023-01-01 12:00:00\n")
            f.write("PlayerC,15,2023-01-03 14:00:00\n")
            f.write("PlayerB,5,2023-01-02 10:00:00\n")
            
        rankings = ranking_utils.get_rankings()
        
        self.assertEqual(len(rankings), len(expected_sorted_rankings))
        self.assertListEqual(rankings, expected_sorted_rankings)
        
        # Check types for the first entry
        if rankings:
            self.assertIsInstance(rankings[0]['name'], str)
            self.assertIsInstance(rankings[0]['moves'], int)
            self.assertIsInstance(rankings[0]['date'], str)

    def test_get_rankings_malformed_entries(self):
        """Test get_rankings with a file containing malformed entries."""
        # Expected valid entry
        valid_entry = {'name': "ValidPlayer", 'moves': 20, 'date': "2023-01-04 16:00:00"}

        with open(self.test_ranking_file_path, 'w', encoding='utf-8') as f:
            f.write("MalformedLineOnlyOneField\n")
            f.write(f"{valid_entry['name']},{valid_entry['moves']},{valid_entry['date']}\n")
            f.write("AnotherPlayer,NotANumber,2023-01-05 18:00:00\n")
            f.write("PlayerD,25,2023-01-06 20:00:00,ExtraField\n") # This will be skipped due to len(parts) !=3
            f.write(",30,2023-01-07 22:00:00\n") # Empty name, but technically valid format for get_rankings
                                                # ranking_utils.add_score would sanitize empty names, but get_rankings reads what's there.
                                                # For now, let's assume empty name is read as is by get_rankings.
                                                # The spec for add_score sanitizes, get_rankings just parses.
            
        rankings = ranking_utils.get_rankings()
        
        # Current get_rankings skips lines that don't split into 3 parts, or where moves isn't int.
        # "PlayerD,25,2023-01-06 20:00:00,ExtraField" -> skipped (len != 3)
        # ",30,2023-01-07 22:00:00" -> name="", moves=30, date="2023-01-07 22:00:00" (parsed)
        
        expected_parsed_rankings = [
            valid_entry,
            {'name': "", 'moves': 30, 'date': "2023-01-07 22:00:00"}
        ]
        # Sort expected by moves for comparison
        expected_parsed_rankings.sort(key=lambda x: x['moves'])

        self.assertEqual(len(rankings), len(expected_parsed_rankings))
        self.assertListEqual(rankings, expected_parsed_rankings)

    # --- Tests for add_score ---

    def test_add_score_empty_file(self):
        """Test adding a score to an empty/non-existent file."""
        ranking_utils.add_score("Player1", 10, "2023-01-01 10:00:00")
        rankings = ranking_utils.get_rankings()
        self.assertEqual(len(rankings), 1)
        self.assertEqual(rankings[0]['name'], "Player1")
        self.assertEqual(rankings[0]['moves'], 10)
        self.assertEqual(rankings[0]['date'], "2023-01-01 10:00:00")

    def test_add_score_new_best_score(self):
        """Test adding a score that becomes the new best score."""
        ranking_utils.add_score("PlayerA", 10, "2023-01-01 10:00:00")
        ranking_utils.add_score("PlayerB", 15, "2023-01-02 10:00:00")
        
        # New best score
        ranking_utils.add_score("PlayerC", 5, "2023-01-03 10:00:00")
        
        rankings = ranking_utils.get_rankings()
        self.assertEqual(len(rankings), 3)
        self.assertEqual(rankings[0]['name'], "PlayerC")
        self.assertEqual(rankings[0]['moves'], 5)
        self.assertEqual(rankings[1]['name'], "PlayerA")
        self.assertEqual(rankings[2]['name'], "PlayerB")

    def test_add_score_not_top_score_list_not_full(self):
        """Test adding a score that is not a top score, list not full."""
        ranking_utils.add_score("PlayerA", 5, "2023-01-01 10:00:00")
        ranking_utils.add_score("PlayerB", 15, "2023-01-02 10:00:00")
        
        # New score, not the best, not the worst
        ranking_utils.add_score("PlayerC", 10, "2023-01-03 10:00:00")
        
        rankings = ranking_utils.get_rankings()
        self.assertEqual(len(rankings), 3)
        self.assertEqual(rankings[0]['name'], "PlayerA") # Best score
        self.assertEqual(rankings[1]['name'], "PlayerC") # Middle score
        self.assertEqual(rankings[2]['name'], "PlayerB") # Worst score

    def test_add_score_list_full_new_score_makes_list(self):
        """Test adding a score when list is full, new score makes the list."""
        # Fill the list with MAX_RANKING_ENTRIES scores
        for i in range(MAX_RANKING_ENTRIES):
            ranking_utils.add_score(f"Player{i}", (i + 1) * 10, f"2023-01-01 10:0{i}:00")
        
        # Current worst score is (MAX_RANKING_ENTRIES * 10)
        # Add a score that is better than the worst
        better_score_moves = (MAX_RANKING_ENTRIES * 10) - 5 
        ranking_utils.add_score("NewBest", better_score_moves, "2023-02-01 10:00:00")
        
        rankings = ranking_utils.get_rankings()
        self.assertEqual(len(rankings), MAX_RANKING_ENTRIES)
        
        # Check if "NewBest" is in the list
        self.assertTrue(any(r['name'] == "NewBest" for r in rankings))
        
        # "NewBest" (95 moves) should be the last entry in the sorted list of top scores,
        # as Player0 (10 moves) is the best.
        self.assertEqual(rankings[MAX_RANKING_ENTRIES-1]['name'], "NewBest")
        
        # The new score should be in, and the original worst score (Player<MAX-1> with MAX*10 moves) should be out.
        # Original scores were Player0 (10 moves) ... Player9 (100 moves) if MAX_RANKING_ENTRIES = 10
        # New score is 95 moves for "NewBest". So "Player9" (100 moves) should be out.
        self.assertFalse(any(r['name'] == f"Player{MAX_RANKING_ENTRIES-1}" and r['moves'] == MAX_RANKING_ENTRIES*10 for r in rankings))


    def test_add_score_list_full_new_score_not_good_enough(self):
        """Test adding a score when list is full, new score is not good enough."""
        # Fill the list with MAX_RANKING_ENTRIES scores, all better than the new one
        for i in range(MAX_RANKING_ENTRIES):
            ranking_utils.add_score(f"Player{i}", (i + 1) * 5, f"2023-01-01 10:0{i}:00") # Moves: 5, 10, ..., MAX*5
        
        worst_score_in_list_moves = MAX_RANKING_ENTRIES * 5
        # Add a score that is worse than all existing scores
        ranking_utils.add_score("WorsePlayer", worst_score_in_list_moves + 5, "2023-02-01 10:00:00")
        
        rankings = ranking_utils.get_rankings()
        self.assertEqual(len(rankings), MAX_RANKING_ENTRIES)
        self.assertFalse(any(r['name'] == "WorsePlayer" for r in rankings))

    def test_add_score_name_sanitization(self):
        """Test name sanitization (trimming and length limit)."""
        # Test trimming
        ranking_utils.add_score("  PlayerX  ", 5, "2023-01-01 12:00:00")
        rankings = ranking_utils.get_rankings()
        self.assertEqual(rankings[0]['name'], "PlayerX")

        # Clean up for next part of the test
        if os.path.exists(self.test_ranking_file_path):
            os.remove(self.test_ranking_file_path)

        # Test length limit
        long_name = "A" * 60  # Name longer than 50 characters
        expected_truncated_name = "A" * 50
        ranking_utils.add_score(long_name, 10, "2023-01-02 12:00:00")
        rankings = ranking_utils.get_rankings()
        self.assertEqual(rankings[0]['name'], expected_truncated_name)
        self.assertEqual(len(rankings[0]['name']), 50)

    def test_add_score_reject_empty_name(self):
        """Test that scores with empty names after stripping are rejected."""
        ranking_utils.add_score("   ", 15, "2023-01-01 13:00:00") # Name is all spaces
        rankings = ranking_utils.get_rankings()
        # Expect that no score was added because the name became empty after stripping
        self.assertEqual(len(rankings), 0)

        # Add a valid score to ensure the file is not empty and the previous one was indeed rejected
        ranking_utils.add_score("ValidPlayer", 20, "2023-01-01 14:00:00")
        rankings = ranking_utils.get_rankings()
        self.assertEqual(len(rankings), 1)
        self.assertEqual(rankings[0]['name'], "ValidPlayer")


if __name__ == '__main__':
    unittest.main()
