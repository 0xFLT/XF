import sqlite3
import random

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def get_all_players(conn):
    """Fetch all players and their relevant data from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name, ranking, playerActivity, playerHistorical FROM players")
    players = [{"name": row[0], "ranking": row[1], "playerActivity": row[2], "playerHistorical": row[3]} for row in cursor.fetchall()]
    return players

def compute_match_score(player, total_players):
    """Calculate matchScore based on player data."""
    player_v_rank = total_players - player['ranking']
    return player['playerActivity'] * player_v_rank * player['playerHistorical']

def find_opponent(all_players, player):
    """Finds an opponent for the given player based on matchScore."""
    total_players = len(all_players)
    player_match_score = compute_match_score(player, total_players)

    # Compute matchScores for all players
    for p in all_players:
        p['matchScore'] = compute_match_score(p, total_players)

    # Filter potential opponents based on ranking difference
    potential_opponents = [p for p in all_players 
                           if player['ranking'] - 5 <= p['ranking'] <= player['ranking'] + 5 and p['name'] != player['name']]

    # Sort potential opponents based on matchScore difference
    potential_opponents.sort(key=lambda x: abs(x['matchScore'] - player_match_score))

    # Return the opponent with closest matchScore if available
    return potential_opponents[0] if potential_opponents else None

# Connect to the database
conn = connect_to_db()

# Assuming you have a player you're looking for an opponent for:
player = {"name": "John", "ranking": 3, "playerActivity": 1.2, "playerHistorical": 0.9}  # Can also come from a DB query.

all_players = get_all_players(conn)
opponent = find_opponent(all_players, player)

if opponent:
    print(f"{player['name']} (Rank {player['ranking']}, MatchScore {compute_match_score(player, len(all_players))}) should play against {opponent['name']} (Rank {opponent['ranking']}, MatchScore {opponent['matchScore']})")
else:
    print(f"No suitable opponent found for {player['name']} (Rank {player['ranking']})")

conn.close()  # Close the connection
