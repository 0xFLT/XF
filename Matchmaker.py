import sqlite3

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def get_potential_opponents(conn):
    """Fetch all other players except the user from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name, ranking, playerActivity, playerHistorical, eloRating, playerStreak FROM players")
    players = [
        {"name": row[0], "ranking": row[1], "playerActivity": row[2], "playerHistorical": row[3], "eloRating": row[4], "playerStreak": row[5]}
        for row in cursor.fetchall()
    ]
    return players

def adjust_elo_for_user(user):
    """Modify the user's Elo rating based on additional factors."""
    factor = user['playerActivity'] * user['playerHistorical'] * (1 + user['playerStreak']/10)
    return user['eloRating'] + (user['eloRating'] / 10) * factor

def find_opponent_for_user(user, all_players):
    """Finds an opponent for the app user based on adjusted Elo rating."""
    user['adjustedElo'] = adjust_elo_for_user(user)
    sorted_players = sorted(all_players, key=lambda x: abs(x['eloRating'] - user['adjustedElo']))
    
    for potential_opponent in sorted_players:
        if potential_opponent['name'] != user['name']:
            return potential_opponent

    return None  # No opponent found

def main(user):
    # Connect to the database
    conn = connect_to_db()

    # Get potential opponents from the database
    all_players = get_potential_opponents(conn)

    # Find a suitable opponent for the user
    opponent = find_opponent_for_user(user, all_players)

    if opponent:
        print(f"{user['name']} (Adjusted Elo {user['adjustedElo']:.2f}) should play against {opponent['name']} (Elo {opponent['eloRating']:.2f})")
    else:
        print(f"No suitable opponent found for {user['name']} (Adjusted Elo {user['adjustedElo']:.2f})")

    conn.close()  # Close the connection

# Example run
user = {"name": "John", "eloRating": 105.0, "playerActivity": 0.9, "playerHistorical": 0.8, "playerStreak": 5}  # This represents the app user. 
main(user)
