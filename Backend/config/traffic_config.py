
# Hardcoded Adjacency Map for Bangalore Context
# In a real app, this would be a geospatial query or a graph database.
ADJACENCY_MAP = {
    "Hebbal": ["Yeshwanthpur", "M.G. Road", "Indiranagar"],
    "Yeshwanthpur": ["Hebbal", "M.G. Road"],
    "M.G. Road": ["Indiranagar", "Hebbal", "Koramangala"],
    "Indiranagar": ["M.G. Road", "Whitefield", "Koramangala"],
    "Koramangala": ["Jayanagar", "Indiranagar", "M.G. Road", "Electronic City", "HSR Layout"], # HSR might not be in dataset
    "Jayanagar": ["Koramangala", "South End Circle", "M.G. Road"],
    "Whitefield": ["Indiranagar", "Marathahalli"],
    "Electronic City": ["Koramangala", "Silk Board"]
}
