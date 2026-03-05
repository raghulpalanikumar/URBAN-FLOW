import os
import pandas as pd

# Load the dataset
# Assuming this file is in Backend/utils/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'Banglore_traffic_Dataset.csv')

df = pd.DataFrame()
LATEST_DATE = None

def load_data():
    global df, LATEST_DATE
    try:
        if not os.path.exists(DATA_PATH):
            print(f"Warning: Data file not found at {DATA_PATH}")
            return
            
        print(f"Loading data from: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
        # Ensure Date is datetime if needed
        df['Date'] = pd.to_datetime(df['Date'])
        LATEST_DATE = df['Date'].max()
        print(f"Data loaded. Latest date in dataset: {LATEST_DATE}")
    except Exception as e:
        print(f"Error loading data: {e}")
        df = pd.DataFrame()

# Initial load
load_data()

def get_dataframe():
    global df
    if df.empty:
        load_data()
    return df.copy() if not df.empty else pd.DataFrame()

def get_latest_date():
    global LATEST_DATE
    if df.empty:
        load_data()
    return LATEST_DATE
