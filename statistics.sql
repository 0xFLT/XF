-- Create Players Table
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    eloRating REAL NOT NULL,
    total_points REAL NOT NULL DEFAULT 0,
    join_date DATE NOT NULL,
    subscription_expiry DATE NOT NULL,
    last_played_date DATE  -- To track the last played date for Elo decay
);

-- Create Games Table
CREATE TABLE games (
    game_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    player_a_id INTEGER NOT NULL,
    player_b_id INTEGER NOT NULL,
    margin_of_victory INTEGER,
    winner_id INTEGER,  -- To record the winner of the game
    FOREIGN KEY (player_a_id) REFERENCES players (player_id),
    FOREIGN KEY (player_b_id) REFERENCES players (player_id),
    FOREIGN KEY (winner_id) REFERENCES players (player_id)
);

-- Create Elo History Table
CREATE TABLE elo_history (
    history_id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL,
    old_elo_rating REAL NOT NULL,  -- To track the old Elo rating
    new_elo_rating REAL NOT NULL,  -- To track the new Elo rating after update
    date_of_change DATE NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players (player_id)
);

-- Create Points History Table
CREATE TABLE points_history (
    history_id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL,
    game_points REAL NOT NULL,  -- To track the points earned in a specific game
    total_points REAL NOT NULL,  -- To track the cumulative total points
    date_of_change DATE NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players (player_id)
);

-- Create Course Info Table
CREATE TABLE course_info (
    info_id INTEGER PRIMARY KEY,
    annual_fee REAL NOT NULL,
    fee_change_date DATE NOT NULL,
    paying_players INTEGER NOT NULL
);

-- Create Player Activity Log
CREATE TABLE player_activity_log (
    log_id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL,
    activity_date DATE NOT NULL,
    activity_type TEXT NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players (player_id)
);
