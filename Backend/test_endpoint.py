
import requests
import json

def test_diversion():
    url = "http://localhost:5000/get_diversion"
    payload = {
        "area": "Indiranagar",
        "closed_road": "100 Feet Road"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Exception:", e)

if __name__ == "__main__":
    test_diversion()
