from pathlib import Path
from src.spotify_api import get_top_50_tracks
from src.database import init_db, insert_tracks, prepare_tracks_data
from src.analysis import analyze_top_tracks

def main():
    # Set up paths
    root_dir = Path(__file__).parent
    data_dir = root_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    db_path = data_dir / 'spotify_tracks.db'

    print("Initializing database...")
    init_db(db_path)
    
    print("Fetching top 50 tracks...")
    top_tracks = get_top_50_tracks()
    
    print("Preparing data for insertion...")
    tracks_data = prepare_tracks_data(top_tracks)
    
    print("Inserting tracks into database...")
    insert_tracks(tracks_data, db_path)
    
    print("Data update completed successfully.")
    
    print("Analyzing tracks...")
    analyze_top_tracks()

if __name__ == "__main__":
    main()