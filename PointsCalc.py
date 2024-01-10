import sqlite3

# Constants
TOTAL_GAMES_PER_YEAR = 52  # Assuming weekly games
TOTAL_PLAYERS = 40  # Total number of players

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def calculate_points(R_A, rank, total_players):
    """Calculate points based on Elo Rating and Rank."""
    return R_A * 0.1 * 2 ** ((total_players - rank) / 4)

def update_points(player_name, conn):
    """Update points for a player after a match."""
    cursor = conn.cursor()

    # Fetch current rating and rank
    cursor.execute("SELECT eloRating, rank FROM players WHERE name=?", (player_name,))
    R_A, rank_A = cursor.fetchone()

    # Calculate Points
    points_A = calculate_points(R_A, rank_A, TOTAL_PLAYERS)

    # Update Points in DB
    cursor.execute("UPDATE players SET points=? WHERE name=?", (points_A, player_name))

    conn.commit()

# Example usage after Elo ratings have been updated:
conn = connect_to_db()
update_points("Player A", conn)
conn.close()

