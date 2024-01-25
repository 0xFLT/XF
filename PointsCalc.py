import sqlite3

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

def assign_winner_points(points_winner, points_loser, winner):
    """Assign the highest points among two players to the winner."""
    return (points_winner, points_loser) if winner == 'A' else (points_loser, points_winner)

def update_points(player_a_id, player_b_id, player_a_wins, conn):
    """Update points for players after a match, using old Elo ratings and assigning higher points to the winner."""
    cursor = conn.cursor()

    # Get the total number of players on the course
    total_players = get_total_players(conn)

    # Fetch old ratings and ranks
    cursor.execute("SELECT eloRating, rank FROM players WHERE player_id=?", (player_a_id,))
    old_rating_A, rank_A = cursor.fetchone()
    cursor.execute("SELECT eloRating, rank FROM players WHERE player_id=?", (player_b_id,))
    old_rating_B, rank_B = cursor.fetchone()

    # Calculate Points using old Elo ratings
    points_A = calculate_points(old_rating_A, rank_A, total_players)
    points_B = calculate_points(old_rating_B, rank_B, total_players)

    # Assign the higher points to the winner
    points_A, points_B = assign_winner_points(points_A, points_B, 'A' if player_a_wins else 'B')

    # Update Points in the database
    cursor.execute("UPDATE players SET points=? WHERE player_id=?", (points_A, player_a_id))
    cursor.execute("UPDATE players SET points=? WHERE player_id=?", (points_B, player_b_id))

    conn.commit()

# Example usage
# conn = connect_to_db()
# update_points(1, 2, True, conn)  # Assuming player IDs 1 and 2, True if Player 1 wins
# conn.close()

