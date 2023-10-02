import sqlite3

K_BASE = 3   # was actually 2.13. directly determines the magnitude of change.
SCALING_FACTOR = 20   # was actually 26.67. affects the sensitivity of the rating system to the difference in ratings between players.
BONUS_FACTOR = 1.5  # Increases/decreases the K value in unexpected outcomes.

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def expected_score(R_A, R_B):
    """Compute expected score based on player ratings."""
    return 1 / (1 + 10**((R_B - R_A) / SCALING_FACTOR))

def update_elo_with_bonus(player_a_name, player_b_name, result_a, result_b, conn):
    """Updates the Elo ratings for two players after a match in the database."""
    # Fetch the current ratings from the database
    cursor = conn.cursor()
    cursor.execute("SELECT eloRating FROM players WHERE name=?", (player_a_name,))
    R_A = cursor.fetchone()[0]

    cursor.execute("SELECT eloRating FROM players WHERE name=?", (player_b_name,))
    R_B = cursor.fetchone()[0]

    E_A = expected_score(R_A, R_B)
    E_B = expected_score(R_B, R_A)

    # Check if the result was unexpected and adjust K accordingly
    if result_a > E_A:  # Player A's performance was better than expected
        K_A = K_BASE * BONUS_FACTOR
        K_B = K_BASE / BONUS_FACTOR
    elif result_a < E_A:  # Player B's performance was better than expected
        K_A = K_BASE / BONUS_FACTOR
        K_B = K_BASE * BONUS_FACTOR
    else:  # The result was as expected
        K_A = K_BASE
        K_B = K_BASE

    # Calculate new ratings
    R_A_new = R_A + K_A * (result_a - E_A)
    R_B_new = R_B + K_B * (result_b - E_B)

    # Store the new ratings back to the database
    cursor.execute("UPDATE players SET eloRating=? WHERE name=?", (R_A_new, player_a_name))
    cursor.execute("UPDATE players SET eloRating=? WHERE name=?", (R_B_new, player_b_name))
    conn.commit()

# Example usage:

conn = connect_to_db()

# After a match where Player A (lower rated) wins and Player B loses:
update_elo_with_bonus("Player A", "Player B", 1, 0, conn)

conn.close()
