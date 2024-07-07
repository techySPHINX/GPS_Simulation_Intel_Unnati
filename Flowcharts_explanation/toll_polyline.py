import requests
import json
import os

TOLLGURU_API_KEY = os.environ.get("TOLLGURU_API_KEY")
TOLLGURU_API_URL = "https://apis.tollguru.com/toll/v2"
POLYLINE_ENDPOINT = "complete-polyline-from-mapping-service"

polyline = "gib}FjbyeO...a@?c@?c@@g@"  
path = "43.64183,-79.38246|18.63085,-100.12845" 


def route_encoded_polyline():
    url = f"{TOLLGURU_API_URL}/{POLYLINE_ENDPOINT}"

    payload = json.dumps(
        {
            "source": "here",
            "polyline": polyline,  
            "height": 10,  
            "weight": 30000,  
            "vehicleType": "2AxlesTruck",  
            "departure_time": 1609507347,  
        }
    )
    headers = {"x-api-key": TOLLGURU_API_KEY, "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def route_path_lat_lng():
    url = f"{TOLLGURU_API_URL}/{POLYLINE_ENDPOINT}"

    payload = json.dumps(
        {
            "source": "here",
            "path": path,  
            "height": 10,  
            "weight": 30000,  
            "vehicleType": "2AxlesTruck",  
            "departure_time": 1609507347,  
        }
    )
    headers = {"x-api-key": TOLLGURU_API_KEY, "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


print(route_encoded_polyline().json())
print(route_path_lat_lng().json())
