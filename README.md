# TrackTrend
<img width="1721" alt="Screenshot 2024-09-10 at 8 25 11 PM" src="https://github.com/user-attachments/assets/3c263642-73ca-4801-b7d4-1bbee09c7816">
This project analyzes the Spotify Global Top 50 playlist, including data collection, processing, and visualization using Jupyter notebooks.
Insights uncovered: 
* Songs ranging from 2.8 - 3 minutes in length account for 42.4% of the top 50 indicating a popularity-time efficiency.
* Songs with higher danceability and energy scores tend to rank higher.
* Direct corelation between danceability and popularity
## Setup

1. Clone this repository
2. Create a Conda environment:
   ```
   conda env create -f environment.yml
   ```
3. Activate the environment:
   ```
   conda activate spotify_analysis
   ```
4. Set up your `.env` file with your Spotify API credentials:
   ```
   SPOTIPY_CLIENT_ID=your_client_id_here
   SPOTIPY_CLIENT_SECRET=your_client_secret_here
   ```
5. Launch Jupyter Lab:
   ```
   jupyter lab
   ```
6. Run the Jupyter notebooks in the `notebooks/` directory in order:
   - 01_data_collection.ipynb
   - 02_data_processing.ipynb
   - 03_exploratory_analysis.ipynb
   - 04_time_series_analysis.ipynb (when implemented)

## Project Structure

- `notebooks/`: Jupyter notebooks for analysis
- `src/`: Python modules with reusable functions
- `data/`: Stores the SQLite database
- `visualizations/`: Stores generated plots and visualizations

## Data Collection and Analysis

The data collection, processing, and analysis are all performed within Jupyter notebooks. Follow these steps:

1. Open `01_data_collection.ipynb` to fetch data from Spotify and store it in the database.
2. Use `02_data_processing.ipynb` to clean and preprocess the collected data.
3. Explore the data and create visualizations in `03_exploratory_analysis.ipynb`.
4. (Future) Perform time series analysis in `04_time_series_analysis.ipynb`.

## Updating Data

To update the dataset with the latest Top 50 tracks, re-run the cells in `01_data_collection.ipynb`.

## Visualization

Visualizations generated during the analysis can be found in the `visualizations/` directory.
