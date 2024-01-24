import sqlite3
import datetime

# Constants
K_BASE = 3
SCALING_FACTOR = 20
BONUS_FACTOR = 1.5

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def expected_score(R_A, R_B):
    """Compute expected score based on player ratings."""
    return 1 / (1 + 10 ** ((R_B - R_A) / SCALING_FACTOR))

def calculate_k_factor(margin_of_victory):
    """Calculate an adjusted K-factor based on the margin of victory."""
    return K_BASE + (BONUS_FACTOR * margin_of_victory)

def update_elo_ratings(player_a_name, player_b_name, margin_of_victory, conn):
    """Updates the Elo ratings for two players based on the margin of victory."""
    cursor = conn.cursor()

    # Fetch current ratings
    cursor.execute("SELECT eloRating FROM players WHERE name=?", (player_a_name,))
    R_A = cursor.fetchone()[0]
    cursor.execute("SELECT eloRating FROM players WHERE name=?", (player_b_name,))
    R_B = cursor.fetchone()[0]

    E_A = expected_score(R_A, R_B)
    E_B = expected_score(R_B, R_A)

    # Determine the result (1 for win, 0 for loss)
    result_a = 1 if margin_of_victory > 0 else 0
    result_b = 1 - result_a

    # Calculate the adjusted K-factor
    K = calculate_k_factor(abs(margin_of_victory))

    # Calculate new ratings
    R_A_new = R_A + K * (result_a - E_A)
    R_B_new = R_B + K * (result_b - E_B)

    # Update Elo Ratings in the database
    cursor.execute("UPDATE players SET eloRating=? WHERE name=?", (R_A_new, player_a_name))
    cursor.execute("UPDATE players SET eloRating=? WHERE name=?", (R_B_new, player_b_name))

    conn.commit()

def decay_elo_ratings(conn):
    """Apply Elo rating decay only to players who haven't played in the last 7 days.
    This function is intended to be called by a cron job on a weekly basis."""
    decay_factor = 0.999  # 0.1% decay
    cursor = conn.cursor()
    cursor.execute("SELECT name, eloRating, last_played_date FROM players")
    
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    
    for player in cursor.fetchall():
        name, eloRating, last_played_date = player

        # Convert last played date from string to date object
        last_played_date = datetime.datetime.strptime(last_played_date, '%Y-%m-%d').date()

        # Check if the player hasn't played in the last 7 days
        if last_played_date < seven_days_ago:
            updated_elo = eloRating * decay_factor
            cursor.execute("UPDATE players SET eloRating=? WHERE name=?", (updated_elo, name))
    
    conn.commit()


# Example usage
# Note: The decay_elo_ratings function should be called by a cron job, not during regular script execution.
# conn = connect_to_db()
# decay_elo_ratings(conn)
# conn.close()
