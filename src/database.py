import sqlite3
from datetime import date
import pandas as pd

# Function 1: Initialize Database
def init_db(db_path):
    """
    Creates the 'tracks' and 'playlists' tables in the database if they don't exist.
    Also creates an index on the 'tracks' table for faster querying.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tracks table
    c.execute('''CREATE TABLE IF NOT EXISTS tracks
                 (date TEXT, playlist_id TEXT, rank INTEGER, track_id TEXT, name TEXT, artist TEXT, 
                 popularity INTEGER, danceability REAL, energy REAL, key INTEGER, 
                 loudness REAL, mode INTEGER, speechiness REAL, acousticness REAL, 
                 instrumentalness REAL, liveness REAL, valence REAL, tempo REAL, 
                 duration_ms INTEGER, time_signature INTEGER)''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_date_playlist ON tracks(date, playlist_id)')
    
    # Create playlists table
    c.execute('''CREATE TABLE IF NOT EXISTS playlists
                 (playlist_id TEXT PRIMARY KEY, name TEXT, description TEXT, 
                 owner TEXT, last_updated TEXT)''')
    
    conn.commit()
    conn.close()

# Function 2: Insert Tracks
def insert_tracks(tracks_data, db_path):
    """
    Inserts multiple tracks into the 'tracks' table.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executemany('''INSERT INTO tracks VALUES 
                     (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', tracks_data)
    conn.commit()
    conn.close()

# Function 3: Prepare Tracks Data
def prepare_tracks_data(top_tracks, playlist_id):
    """
    Prepares track data for insertion into the database.
    Formats the data and adds the current date and playlist ID.
    """
    today = date.today().isoformat()
    return [
        (today, playlist_id, i+1, track['id'], track['name'], track['artist'], track['popularity'],
         track['danceability'], track['energy'], track['key'], track['loudness'],
         track['mode'], track['speechiness'], track['acousticness'], track['instrumentalness'],
         track['liveness'], track['valence'], track['tempo'], track['duration_ms'],
         track['time_signature'])
        for i, track in enumerate(top_tracks)
    ]

# Function 4: Insert Playlist Info
def insert_playlist_info(db_path, playlist_id, sp):
    """
    Inserts or updates playlist information in the 'playlists' table.
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
    Retrieves track data for a specific playlist, optionally filtered by date range.
    Returns a pandas DataFrame.
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
    Retrieves information about all playlists stored in the database.
    Returns a pandas DataFrame.
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM playlists"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
