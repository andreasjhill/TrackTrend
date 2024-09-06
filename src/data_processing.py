import pandas as pd

def load_and_clean_data(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM tracks", conn)
    conn.close()

    # Remove duplicates if any
    df.drop_duplicates(subset=['track_id', 'date'], keep='first', inplace=True)

    # Convert 'date' to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Ensure numeric columns are of the correct type
    numeric_columns = ['popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 
                       'speechiness', 'acousticness', 'instrumentalness', 'liveness', 
                       'valence', 'tempo', 'duration_ms', 'time_signature']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def check_missing_values(df):
    return df.isnull().sum()