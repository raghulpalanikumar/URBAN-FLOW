
print("Starting script...")
import sys
import os
print("Imports sys/os done")

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())
print(f"CWD: {os.getcwd()}")
print(f"PATH modified")

try:
    print("Trying to import traffic_service...")
    from services.traffic_service import get_diversion_logic
    print("Imported traffic_service successfully.")
except Exception as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test_scenario():
    print("Testing 'Hebbal Flyover' in 'Hebbal' (Simulating restricted condition)...")
    
    try:
        result = get_diversion_logic("Hebbal Flyover", "Hebbal")
        
        print("\n--- RESULTS ---")
        if "error" in result:
            print(f"Error: {result['error']}")
            return

        print(f"Correction Notice: {result.get('correction_notice')}")
        print(f"Analyzed Alternatives: {result.get('analyzed_alternatives_count')}")
        
        details = result.get('diversion_details', {})
        print(f"Best Route Selected: {details.get('road_name')}")
        print(f"Congestion: {details.get('congestion_level')}%")
        print(f"Is Peripheral: {details.get('is_peripheral', False)}")
        
        print("\n--- LLM PROMPT GENERATED (Verification) ---")
        # Note: We can't see the exact prompt variable here, but the result contains the 'recommendation'
        # which flows from the prompt.
        rec = result.get('recommendation', '')
        print((rec[:200] + "...") if rec else "No recommendation")
        
        print("\n--- TOP ALTERNATIVES FOUND ---")
        for alt in result.get('all_alternatives', [])[:3]:
            print(f"- {alt['name']}: {alt['congestion']}%")

    except Exception as e:
        print(f"Test Execution Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scenario()
