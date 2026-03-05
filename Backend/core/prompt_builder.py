
def build_diversion_prompt(closed_road, area, context_data, best_route_info):
    """Build the prompt string for the diversion recommendation."""
    
    recommended_str = best_route_info.get('road_name', 'None')
    cong = best_route_info.get('congestion_level', 'N/A')
    original_area = best_route_info.get('original_area', 'nearby area')
    avg_speed = best_route_info.get('avg_speed', 'N/A')
    
    prompt = f"""
You are an advanced Traffic Control AI.
Current Status: {closed_road} in {area} is CLOSED.

DATA CONTEXT:
{context_data}

DECISION:
Best available route: **{recommended_str}** (Congestion: {cong}%)

INSTRUCTIONS:
1. If the situation is critical (High congestion everywhere), start with "🚨 CRITICAL SITUATION".
2. If recommending a peripheral route (different area), explicitly state: "Avoid {area} entirely. Use peripheral route via {original_area}."
3. Provide a clear, strategic recommendation.
4. List the stats for the chosen route.
5. If staying home or traveling later is better (100% congestion everywhere), suggest a "Temporal Shift" strategy.

OUTPUT FORMAT:
- **Strategy**: [Main Headline Strategy]
- **Recommended Action**: [Specific Route instructions]
- **Metrics**: Congestion {cong}%, Speed {avg_speed} km/h
- **Reasoning**: [Why this is statistically better]
"""
    return prompt

def build_route_prompt(source, destination, context_data):
    """Build the prompt string for general route planning."""
    
    prompt = f"""
Route: {source} -> {destination}
Context: {context_data}
Suggest optimal path and estimated time.
"""
    return prompt
