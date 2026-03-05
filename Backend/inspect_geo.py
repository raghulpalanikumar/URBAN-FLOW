
import pandas as pd
import os

DATA_PATH = r'd:\Work2\Manimaran\Backend\data\Banglore_traffic_Dataset.csv'

def inspect_data():
    if not os.path.exists(DATA_PATH):
        print("Data file not found.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # 1. Where is Hebbal Flyover?
    hebbal_locs = df[df['Road/Intersection Name'].str.contains('Hebbal Flyover', case=False, na=False)]['Area Name'].unique()
    print(f"Hebbal Flyover is associated with areas: {hebbal_locs}")

    # 2. What roads are in Jayanagar?
    jayanagar_roads = df[df['Area Name'].str.contains('Jayanagar', case=False, na=False)]['Road/Intersection Name'].unique()
    print(f"Roads in Jayanagar: {jayanagar_roads}")

    # 3. Check South End Circle Details for a specific date (to check incidents)
    # Just grab a sample
    sec_sample = df[df['Road/Intersection Name'].str.contains('South End Circle', case=False, na=False)].head(1)
    print("\nSample South End Circle Data:")
    print(sec_sample[['Date', 'Area Name', 'Road/Intersection Name', 'Incident Reports', 'Congestion Level']].to_string())

if __name__ == "__main__":
    inspect_data()
