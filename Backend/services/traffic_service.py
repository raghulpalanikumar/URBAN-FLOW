from utils.data_loader import get_dataframe, get_latest_date
from services.llm_service import query_ollama
from config.traffic_config import ADJACENCY_MAP
from core.traffic_analysis import (
    clean_numeric_columns, get_area_traffic, determine_actual_area_for_road,
    get_alternatives, get_peripheral_alternatives, rank_routes,
    get_top_alternatives_stats, get_sorted_locations, get_source_traffic_context
)
from core.prompt_builder import build_diversion_prompt, build_route_prompt
import pandas as pd


def _fallback_diversion_recommendation(closed_road, area, best_route_info, top_alternatives_list):
    """Rule-based recommendation when Ollama is unavailable or returns 500."""
    road_name = best_route_info.get("road_name", "alternative route")
    congestion = best_route_info.get("congestion_level", 0)
    speed = best_route_info.get("avg_speed", 0)
    incidents = best_route_info.get("incidents", 0)
    is_peripheral = best_route_info.get("is_peripheral", False)
    lines = [
        "**Strategy**: Data-driven diversion (reasoning engine temporarily unavailable).",
        "",
        "**Recommended Action**: Use the following route based on current traffic data:",
        f"- **Route**: {road_name}",
        f"- **Congestion**: {congestion}%",
        f"- **Average Speed**: {speed} km/h",
        f"- **Incidents**: {incidents}",
        "",
        "**Reasoning**: This route was selected from available alternatives by congestion and speed. "
        + ("It is in a neighboring area to avoid congestion in " + area + "." if is_peripheral else "It is within " + area + "."),
    ]
    if top_alternatives_list:
        lines.append("")
        lines.append("Other options (if the above is busy):")
        for alt in top_alternatives_list[1:4]:
            lines.append(f"- {alt.get('name', '')} (Congestion: {alt.get('congestion', 'N/A')}%)")
    return "\n".join(lines)

def get_diversion_logic(closed_road, area):
    """
    Orchestrates the diversion logic:
    1. Loads data.
    2. Analyzes traffic (local and peripheral).
    3. Ranks alternatives.
    4. Constructs prompt.
    5. Calls LLM.
    """
    df = get_dataframe()
    LATEST_DATE = get_latest_date()
    if LATEST_DATE is None or df.empty:
        return {"error": "Traffic data not available. Ensure Backend/data/Banglore_traffic_Dataset.csv exists.", "status": 500}

    # Clean data
    df = clean_numeric_columns(df)

    # 1. Get current traffic snapshot
    area_traffic = get_area_traffic(df, area, LATEST_DATE)

    # 🚨 INTELLIGENT FIX: Check if the closed road is actually in this area
    correction_notice = None
    road_in_area = area_traffic[area_traffic['Road/Intersection Name'].str.contains(closed_road, case=False, na=False)]
    
    if road_in_area.empty:
        actual_area, correct_date = determine_actual_area_for_road(df, closed_road, area)
        if actual_area:
            correction_notice = f"Note: '{closed_road}' is located in '{actual_area}', not '{area}'. Analyzing traffic in '{actual_area}' instead."
            print(f"Auto-correction: Switching context from {area} to {actual_area}")
            area = actual_area
            # Refresh traffic for new area
            area_traffic = df[
                (df['Date'] == correct_date) & 
                (df['Area Name'].str.contains(area, case=False, na=False))
            ].copy()

    # 2. Identify the closed road and potential alternatives IN THE SAME AREA
    alternatives = get_alternatives(area_traffic, closed_road)
    
    # Context Construction
    context_data = f"Current Traffic Status for Target Area: {area}\n"
    if not area_traffic.empty:
        sample_date = area_traffic.iloc[0]['Date']
        context_data += f"Data Reference Date: {sample_date}\n\n"

    # --- INTELLIGENT PERIPHERAL SEARCH ---
    # If no alternatives in area OR existing alternatives are dangerously congested (>90%)
    if alternatives.empty or (not alternatives.empty and alternatives['Congestion Level'].min() > 90):
        context_data += f"🚨 CRITICAL SITUATION: High congestion detected in {area} or no direct alternatives.\n"
        context_data += "Scanning Peripheral Zones for better routes...\n\n"
        
        neighbors = ADJACENCY_MAP.get(area, [])
        nearby_df = get_peripheral_alternatives(df, neighbors, LATEST_DATE)
        
        if not nearby_df.empty:
            nearby_df['is_peripheral'] = True
            alternatives = pd.concat([alternatives, nearby_df], ignore_index=True)
            context_data += f"Found {len(nearby_df)} peripheral routes in {', '.join(neighbors)}.\n"

    # 3. Rank and Select Best Route
    ranked_alternatives = rank_routes(alternatives)
    best_route_info = {}
    top_alternatives_list = []
    
    if not ranked_alternatives.empty:
        best_row = ranked_alternatives.iloc[0]
        
        is_peripheral = best_row.get('is_peripheral', False)
        area_prefix = f"[{best_row['Area Name']}] " if is_peripheral else ""
        
        best_route_info = {
            "road_name": f"{area_prefix}{best_row['Road/Intersection Name']}",
            "congestion_level": float(best_row['Congestion Level']),
            "avg_speed": float(best_row['Average Speed']),
            "traffic_volume": int(best_row['Traffic Volume']),
            "incidents": int(best_row['Incident Reports']),
            "is_peripheral": bool(is_peripheral),
            "original_area": best_row['Area Name']
        }

        context_data += "\nAvailable & Peripheral Routes (Ranked):\n"
        
        # Get formatted stats for top 5
        top_alternatives_list, context_str = get_top_alternatives_stats(ranked_alternatives)
        context_data += context_str

    else:
        context_data += "No viable roads found in dataset.\n"

    # 4. Construct Prompt
    prompt = build_diversion_prompt(closed_road, area, context_data, best_route_info)

    # 5. Call LLM (with fallback if Ollama returns 500 or is unavailable)
    reasoning_output = query_ollama(prompt)
    if isinstance(reasoning_output, str) and reasoning_output.strip().startswith("Error:"):
        reasoning_output = _fallback_diversion_recommendation(
            closed_road, area, best_route_info, top_alternatives_list
        )

    return {
        "closed_road": closed_road,
        "area": area,
        "recommendation": reasoning_output,
        "analyzed_alternatives_count": len(alternatives),
        "diversion_details": best_route_info,
        "all_alternatives": top_alternatives_list,
        "correction_notice": correction_notice
    }

def get_locations_logic():
    df = get_dataframe()
    areas, roads = get_sorted_locations(df)
    return {"areas": areas, "roads": roads}


def get_roads_by_area_logic(area):
    """Return roads that appear in the given area (for filtered dropdown)."""
    df = get_dataframe()
    if df.empty or not area or not area.strip():
        return []
    area_df = df[df['Area Name'].str.contains(area.strip(), case=False, na=False)]
    if area_df.empty:
        return []
    roads = sorted(area_df['Road/Intersection Name'].dropna().unique().tolist())
    return roads

def get_route_logic(source, destination):
    df = get_dataframe()
    LATEST_DATE = get_latest_date()
    if df.empty or LATEST_DATE is None:
        return {
            "source": source,
            "destination": destination,
            "recommendation": "Traffic data not available for route planning.",
            "analyzed_alternatives_count": 0,
        }
    context_str, count = get_source_traffic_context(df, source, LATEST_DATE)
    
    prompt = build_route_prompt(source, destination, context_str)
    route_plan = query_ollama(prompt)
    if isinstance(route_plan, str) and route_plan.strip().startswith("Error:"):
        route_plan = (
            f"**Route**: {source} → {destination}\n\n"
            "Recommendation engine temporarily unavailable. "
            "Use current traffic context and prefer routes with lower congestion from the data."
        )

    return {
        "source": source,
        "destination": destination,
        "recommendation": route_plan,
        "analyzed_alternatives_count": count
    }
