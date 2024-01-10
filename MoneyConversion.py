import sqlite3
import datetime

# Constants
TOTAL_PLAYERS = 40  # Total number of players
TOTAL_MONEY_DISTRIBUTED = 2816  # Calculated from your provided data

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def predict_total_points(conn):
    """Predict the total points for the course based on the current rate of play."""
    cursor = conn.cursor()
    
    # Retrieve total points accumulated so far and the number of games played
    cursor.execute("SELECT SUM(points), COUNT(game_id) FROM game_results")
    total_points_so_far, total_games_played = cursor.fetchone()

    # Calculate the number of weeks in the current year up to now
    current_week = datetime.date.today().isocalendar()[1]
    
    # Project the total points for the year
    if current_week > 0:
        projected_total_points = (total_points_so_far / total_games_played) * (TOTAL_PLAYERS * 52)
    else:
        projected_total_points = 0
    
    return projected_total_points

def update_conversion_rate(conn):
    """Calculate and update the conversion rate from points to money."""
    projected_total_points = predict_total_points(conn)
    new_conversion_rate = TOTAL_MONEY_DISTRIBUTED / projected_total_points if projected_total_points else 0
    # Update this conversion rate in your database or application as needed
    return new_conversion_rate

# Example Usage
conn = connect_to_db()
new_conversion_rate = update_conversion_rate(conn)
print(f"New Conversion Rate: {new_conversion_rate}")

conn.close()

