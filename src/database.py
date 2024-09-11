import sqlite3
from datetime import date
import pandas as pd

# Function 1: Initialize Database
def init_db(db_path):
    """
    Create 'tracks' table in database if it doesn't exist.
    create index on 'tracks' table for faster querying.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tracks table
    c.execute('''CREATE TABLE IF NOT EXISTS tracks
                 (date TEXT, rank INTEGER, track_id TEXT, name TEXT, artist TEXT, 
                 popularity INTEGER, danceability REAL, energy REAL, key INTEGER, 
                 loudness REAL, mode INTEGER, speechiness REAL, acousticness REAL, 
                 instrumentalness REAL, liveness REAL, valence REAL, tempo REAL, 
                 duration_ms INTEGER, time_signature INTEGER)''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_date ON tracks(date)')
    
    conn.commit()
    conn.close()

# Function 2: Insert Tracks
def insert_tracks(tracks_data, db_path):
    """
    Insert the tracks into the 'tracks' table.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executemany('''INSERT INTO tracks VALUES 
                     (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', tracks_data)
    conn.commit()
    conn.close()

# Function 3: Prepare Tracks Data
def prepare_tracks_data(top_tracks):
    """
    Prepare track data for insertion into the database.
    Format the data and add the current date.
    """
    today = date.today().isoformat()
    return [
        (today, i+1, track['id'], track['name'], track['artist'], track['popularity'],
         track['danceability'], track['energy'], track['key'], track['loudness'],
         track['mode'], track['speechiness'], track['acousticness'], track['instrumentalness'],
         track['liveness'], track['valence'], track['tempo'], track['duration_ms'],
         track['time_signature'])
        for i, track in enumerate(top_tracks)
    ]

# Function 4: Insert Playlist Info
def insert_playlist_info(db_path, playlist_id, sp):
    """
    Insert or update playlist information in the 'playlists' table.
    """
    playlist_info = sp.playlist(playlist_id)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO playlists VALUES (?, ?, ?, ?, ?)''',
              (playlist_id, playlist_info['name'], playlist_info['description'],
               playlist_info['owner']['display_name'], date.today().isoformat()))
    conn.commit()
    conn.close()

# Function 5: Get Playlist Data
def get_playlist_data(db_path, playlist_id, start_date=None, end_date=None):
    """
    Retrieve track data for a specific playlist, optionally filtered by date range.
    Return pandas DataFrame.
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM tracks WHERE playlist_id = ?"
    params = [playlist_id]
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Function 6: Get All Playlists
def get_all_playlists(db_path):
    """
    Retrieve info about all playlists stored in the database.
    Return pandas DataFrame.
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM playlists"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_track_history(db_path, track_id, playlist_id):
    """
    Retrieve ranking history of a specific track in a playlist.
    """
    conn = sqlite3.connect(db_path)
    query = """
    SELECT date, rank, popularity
    FROM tracks
    WHERE track_id = ? AND playlist_id = ?
    ORDER BY date
    """
    df = pd.read_sql_query(query, conn, params=[track_id, playlist_id])
    conn.close()
    return df

def get_rank_changes(db_path, playlist_id, date1, date2):
    """
    Compare track rank between two dates for a specific playlist.
    """
    conn = sqlite3.connect(db_path)
    query = """
    SELECT t1.track_id, t1.name, t1.artist, t1.rank as rank1, t2.rank as rank2,
           t2.rank - t1.rank as rank_change
    FROM tracks t1
    JOIN tracks t2 ON t1.track_id = t2.track_id AND t1.playlist_id = t2.playlist_id
    WHERE t1.playlist_id = ? AND t1.date = ? AND t2.date = ?
    ORDER BY rank_change
    """
    df = pd.read_sql_query(query, conn, params=[playlist_id, date1, date2])
    conn.close()
    return df