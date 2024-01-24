import sqlite3

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def get_potential_opponents(conn):
    """Fetch all other players from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name, eloRating, rank FROM players")
    players = [
        {"name": row[0], "eloRating": row[1], "rank": row[2]}
        for row in cursor.fetchall()
    ]
    return players

def find_opponent_for_user(user, all_players):
    """Finds an opponent for the app user based on Elo rating."""
    # Sorting players by the difference in Elo rating
    sorted_players = sorted(all_players, key=lambda x: abs(x['eloRating'] - user['eloRating']))
    
    for potential_opponent in sorted_players:
        if potential_opponent['name'] != user['name']:
            return potential_opponent

    return None  # No opponent found

def main(user):
    # Connect to the database
    conn = connect_to_db()

    # Get potential opponents from the database
    all_players = get_potential_opponents(conn)

    # NOTE: A 24-hour waiting period should be implemented outside this script, typically at the application level.

    # Find a suitable opponent for the user
    opponent = find_opponent_for_user(user, all_players)

    if opponent:
        print(f"{user['name']} (Elo {user['eloRating']}) should play against {opponent['name']} (Elo {opponent['eloRating']})")
    else:
        print(f"No suitable opponent found for {user['name']} (Elo {user['eloRating']})")

    conn.close()  # Close the connection



# Example run
user = {"name": "John", "eloRating": 105, "rank": 20}  # This represents the app user.
main(user)
