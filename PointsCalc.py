import sqlite3

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def get_total_players(conn):
    """
    Retrieve the total number of players from the database.
    Here we assume 'activep = 1' indicates a player who chose that course on their profile.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM totalActive WHERE activep = 1")
    total_players = cursor.fetchone()[0]
    return total_players

def get_player_rank(player_id, conn):
    """Retrieve the rank of a player from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT rank FROM players WHERE player_id=?", (player_id,))
    rank = cursor.fetchone()[0]
    return rank

def calculate_points(elo, rank, total_players):
    """
    Calculate points using the single-formula approach that ensures:
    - Rank 1 yields a 'top value' above the player's Elo.
    - Rank N yields exactly the player's Elo.
    - 10-player top ~ 300 (if Elo=200), 100-player top ~ 1000, etc.

    Points = Elo + [ (Elo/200)*(222.2 + 7.78*N) - Elo ] * ((N - rank)/(N - 1))

    Where:
      N = total_players,
      rank = 1..N,
      Elo range = 50..200,
      constants 222.2, 7.78 make top=300 at N=10, ~1000 at N=100 if Elo=200.
    """
    # Avoid division by zero if total_players == 1
    if total_players <= 1:
        # If there's only 1 player, rank=1 => points = Elo (no competition)
        return elo

    # Compute the "top value" for this player's Elo on this course size
    top_value = (elo / 200.0) * (222.2 + 7.78 * total_players)

    # The difference between that top value and just the player's Elo
    difference = top_value - elo

    # Fraction that goes from 1 for rank=1 down to 0 for rank=N
    fraction = (total_players - rank) / float(total_players - 1)

    # Final points
    points = elo + difference * fraction
    return points

def assign_winner_points(points_winner, points_loser, winner):
    """
    Assign the higher points among two players to the winner.
    The logic remains the same: winner takes the larger of the two computed totals.
    """
    return (points_winner, points_loser) if winner == 'A' else (points_loser, points_winner)

def update_points(player_a_id, player_b_id, player_a_wins, conn):
    """
    Update points for players after a match, using old Elo ratings and the new formula.
    The winner is assigned the higher point total.
    """
    cursor = conn.cursor()

    # Get the total number of paying/active players on this course
    total_players = get_total_players(conn)

    # Fetch old ratings and current ranks
    cursor.execute("SELECT eloRating FROM players WHERE player_id=?", (player_a_id,))
    old_rating_A = cursor.fetchone()[0]
    rank_A = get_player_rank(player_a_id, conn)

    cursor.execute("SELECT eloRating FROM players WHERE player_id=?", (player_b_id,))
    old_rating_B = cursor.fetchone()[0]
    rank_B = get_player_rank(player_b_id, conn)

    # Calculate points using old Elo and the new formula
    points_A = calculate_points(old_rating_A, rank_A, total_players)
    points_B = calculate_points(old_rating_B, rank_B, total_players)

    # Assign the higher points to the winner
    points_A, points_B = assign_winner_points(points_A, points_B, 'A' if player_a_wins else 'B')

    # Update Points in the database
    cursor.execute("UPDATE players SET points=? WHERE player_id=?", (points_A, player_a_id))
    cursor.execute("UPDATE players SET points=? WHERE player_id=?", (points_B, player_b_id))

    conn.commit()

# Example usage:
# conn = connect_to_db()
# update_points(player_a_id=1, player_b_id=2, player_a_wins=True, conn=conn)
# conn.close()
