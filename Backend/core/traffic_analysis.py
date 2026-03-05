
import pandas as pd

def clean_numeric_columns(df):
    """Ensure numeric columns are actually numeric."""
    numeric_cols = ['Congestion Level', 'Average Speed', 'Traffic Volume', 'Incident Reports']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def get_area_traffic(df, area, latest_date):
    """Get traffic data for a specific area on the given date."""
    if df.empty:
        return pd.DataFrame()
    if latest_date is None:
        latest_date = df['Date'].max()
    area_traffic = df[
        (df['Date'] == latest_date) & 
        (df['Area Name'].str.contains(area, case=False, na=False))
    ].copy()
    
    if area_traffic.empty:
        # Fallback logic
        area_specific_df = df[df['Area Name'].str.contains(area, case=False, na=False)]
        if not area_specific_df.empty:
            latest_area_date = area_specific_df['Date'].max()
            area_traffic = area_specific_df[area_specific_df['Date'] == latest_area_date].copy()
            # We assume the caller handles logging fallback usage
    
    return area_traffic

def determine_actual_area_for_road(df, road, current_area):
    """Check if the road is actually in the specified area, otherwise find its correct area."""
    road_matches = df[df['Road/Intersection Name'].str.contains(road, case=False, na=False)]
    if not road_matches.empty:
        correct_area_row = road_matches.sort_values(by='Date', ascending=False).iloc[0]
        actual_area = correct_area_row['Area Name']
        if actual_area.lower() != current_area.lower():
            return actual_area, correct_area_row['Date']
    return None, None

def get_alternatives(area_traffic, closed_road):
    """Identify alternatives in the same area excluding the closed road."""
    return area_traffic[
        ~area_traffic['Road/Intersection Name'].str.contains(closed_road, case=False, na=False)
    ].copy()

def get_peripheral_alternatives(df, neighbors, latest_date):
    """Find best roads in neighboring areas."""
    nearby_data = []
    
    for neighbor in neighbors:
        neighbor_traffic = df[
            (df['Date'] == latest_date) & 
            (df['Area Name'].str.contains(neighbor, case=False, na=False))
        ].copy()
        
        if neighbor_traffic.empty:
             # Fallback
             n_df = df[df['Area Name'].str.contains(neighbor, case=False, na=False)]
             if not n_df.empty:
                 latest = n_df['Date'].max()
                 neighbor_traffic = n_df[n_df['Date'] == latest].copy()
        
        if not neighbor_traffic.empty:
            best_neighbor_road = neighbor_traffic.sort_values(by='Congestion Level', ascending=True).iloc[0]
            nearby_data.append(best_neighbor_road)
            
    return pd.DataFrame(nearby_data) if nearby_data else pd.DataFrame()

def rank_routes(alternatives):
    """Rank routes by congestion (asc) and speed (desc)."""
    if alternatives.empty:
        return alternatives
        
    if 'is_peripheral' not in alternatives.columns:
        alternatives['is_peripheral'] = False
        
    viable = alternatives[alternatives['Congestion Level'] < 100]
    if viable.empty:
        viable = alternatives
        
    return viable.sort_values(by=['Congestion Level', 'Average Speed'], ascending=[True, False])

def get_top_alternatives_stats(ranked_alternatives, limit=5):
    """Format top alternatives for display/context."""
    top_list = []
    context_str = ""
    
    top = ranked_alternatives.head(limit)
    for _, row in top.iterrows():
        is_peri = row.get('is_peripheral', False)
        p_tag = " (Peripheral Route)" if is_peri else ""
        
        stats = {
            "name": f"{row['Area Name']}: {row['Road/Intersection Name']}" if is_peri else row['Road/Intersection Name'],
            "congestion": row['Congestion Level'],
            "speed": row['Average Speed'],
            "incidents": row.get('Incident Reports', 0),
            "volume": row.get('Traffic Volume', 0),
            "is_peripheral": is_peri
        }
        top_list.append(stats)
        
        context_str += (
            f"- Road: {row['Road/Intersection Name']} [{row['Area Name']}]{p_tag}\n"
            f"  Congestion: {row['Congestion Level']}%\n"
            f"  Speed: {row['Average Speed']:.2f} km/h\n"
            f"  Incidents: {row['Incident Reports']}\n\n"
        )
            
    return top_list, context_str

def get_sorted_locations(df):
    """Return sorted unique areas and roads."""
    if df.empty:
        return [], []
    areas = sorted(df['Area Name'].dropna().unique().tolist())
    roads = sorted(df['Road/Intersection Name'].dropna().unique().tolist())
    return areas, roads

def get_source_traffic_context(df, source, latest_date):
    """Get context data for source traffic for route planning."""
    source_traffic = df[
        (df['Date'] == latest_date) & 
        (df['Area Name'].str.contains(source, case=False, na=False))
    ]
    if source_traffic.empty:
         source_traffic = df[df['Area Name'].str.contains(source, case=False, na=False)].sort_values('Date').tail(10)

    context_str = ""
    if not source_traffic.empty:
        top = source_traffic.sort_values(by='Traffic Volume', ascending=False).head(5)
        for _, row in top.iterrows():
            context_str += f"- {row['Road/Intersection Name']}: {row['Congestion Level']}%\n"
            
    return context_str, len(source_traffic)
