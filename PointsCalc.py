import sqlite3

# Constants
TOTAL_GAMES_PER_YEAR = 52  # Assuming weekly games

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def get_total_players(conn):
    """Retrieve the total number of players from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM players")
    total_players = cursor.fetchone()[0]
    return total_players

def calculate_points(R_A, rank, total_players):
    """Calculate points based on Elo Rating and Rank."""
    return R_A * 0.1 * 2 ** ((total_players - rank) / 4)

def update_points(player_name, conn):
    """Update points for a player after a match."""
    cursor = conn.cursor()

    # Get the total number of players on the course
    total_players = get_total_players(conn)

    # Fetch current rating and rank
    cursor.execute("SELECT eloRating, rank FROM players WHERE name=?", (player_name,))
    R_A, rank_A = cursor.fetchone()

    # Calculate Points
    points_A = calculate_points(R_A, rank_A, total_players)

    # Update Points in the database
    cursor.execute("UPDATE players SET points=? WHERE name=?", (points_A, player_name))

    conn.commit()

# Example usage after Elo ratings have been updated:
# conn = connect_to_db()
# update_points("Player A", conn)
# conn.close()
