import sqlite3
import datetime

def connect_to_db():
    """Connect to SQLite database and return the connection."""
    conn = sqlite3.connect('statistics.db')
    return conn

def get_total_money_distributed(conn):
    """Retrieve the total money distributed from the database."""
    cursor = conn.cursor()
    # Assuming the number of paying players is stored in a table 'course_info'
    cursor.execute("SELECT paying_players FROM course_info")
    paying_players = cursor.fetchone()[0]
    annual_fee = 88  # Fixed annual fee per player
    total_money_collected = paying_players * annual_fee
    return total_money_collected * 0.8  # 80% of the total money collected

def predict_total_points(conn):
    """Predict the total points for the course based on the current rate of play."""
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(points), COUNT(game_id) FROM game_results")
    total_points_so_far, total_games_played = cursor.fetchone()
    
    current_week = datetime.date.today().isocalendar()[1]
    if current_week > 0:
        projected_total_points = (total_points_so_far / total_games_played) * (paying_players * 52)
    else:
        projected_total_points = 0
    
    return projected_total_points

def update_conversion_rate(conn):
    """Calculate and update the conversion rate from points to money."""
    total_money_distributed = get_total_money_distributed(conn)
    projected_total_points = predict_total_points(conn)
    new_conversion_rate = total_money_distributed / projected_total_points if projected_total_points else 0
    # Update this conversion rate in your database or application as needed
    return new_conversion_rate

# Example Usage
conn = connect_to_db()
new_conversion_rate = update_conversion_rate(conn)
print(f"New Conversion Rate: {new_conversion_rate}")

conn.close()

