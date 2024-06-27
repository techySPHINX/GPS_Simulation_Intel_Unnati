import folium
import requests
import datetime
from branca.element import JavascriptLink
import os
import geocoder

MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAP_API")


def get_location_coordinates(location_name):

    try:

        g = geocoder.osm(location_name)

        if g.ok:
            return g.lat, g.lng
        else:
            print(
                f"Error fetching coordinates for {location_name}: {g.reason}")
            return None

    except Exception as e:
        print(f"An error occurred while fetching coordinates: {e}")
        return None


INDIA_CENTRE_LAT_LNG = get_location_coordinates("India (approximate center)")

if INDIA_CENTRE_LAT_LNG:
    india_center_lat, india_center_lng = INDIA_CENTRE_LAT_LNG
    print(
        f"India's approximate center coordinates: ({india_center_lat:.4f}, {india_center_lng:.4f})")
else:
    print("Error: Could not retrieve India's center coordinates.")


HIGH_ACCURACY = True
MAX_CACHE_AGE_MILLISECOND = 30000
MAX_NEW_POSITION_MILLISECOND = 5000

is_start = None
path = None
accumulated_distance = 0
current_marker = None

log_console = None
distance_box = None


def create_map():
    global map

    map = folium.Map(location=INDIA_CENTRE_LAT_LNG, zoom_start=13,
                     tiles="https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
                     attr='Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                     max_zoom=18,
                     id="mapbox/streets-v11",
                     tile_size=512,
                     zoom_offset=-1,
                     access_token=MAPBOX_ACCESS_TOKEN
                     )


has_geolocation_support = False


def start_tracking():
    global is_start, path, accumulated_distance, current_marker

    if not has_geolocation_support:
        log_console.text = "Geolocation is not supported by your browser"
        return

    log_console.text = "Locating..."
    distance_box.text = "0.000"
    is_start = True

    def success(position):
        global accumulated_distance, current_marker, path

        latitude = position.coords.latitude
        longitude = position.coords.longitude
        timestamp = datetime.datetime.now().isoformat()

        print(f"1. Detected at {timestamp}")

        if path is None:
            path = folium.PolyLine(
                locations=[[latitude, longitude]], color="#fbc531")
            map.add_child(path)
            map.move_to(location=[latitude, longitude], zoom_start=15)
        else:
            path.add_point([latitude, longitude])

        if current_marker is None:
            current_marker = folium.Marker(
                [latitude, longitude], popup="<b>Start at {}</b>".format(timestamp))
            map.add_child(current_marker)
        else:
            current_marker.location = [latitude, longitude]
            current_marker.popup = f"Current at {timestamp}"

        update_distance(latitude, longitude)

    def error(err):
        print(f"Unable to retrieve your location! {err.code} - {err.message}")


def update_distance(latitude, longitude):
    global accumulated_distance

    if path is None or not is_start:
        return

    if len(path.locations) >= 3:
        last_latlng = path.locations[-2]
        current_latlng = path.locations[-1]
        delta = calculate_distance(
            last_latlng[0], last_latlng[1], current_latlng[0], current_latlng[1])
        accumulated_distance += delta

        formatted_distance = round(accumulated_distance, 3).toLocaleString(
            "en-US", minimum_fraction_digits=3)
        distance_box.text = formatted_distance
        print(f"3. Updated path with {
            delta} km | accumulatedDistance={formatted_distance}")


def calculate_distance(lat1, lon1, lat2, lon2):

    url = f"https: // maps.googleapis.com/maps/api/distancematrix/json?units = kilometers & origins = {
        lat1}, {lon1} & destinations = {lat2}, {lon2} & key = {GOOGLE_MAPS_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        try:

            distance = data["rows"][0]["elements"][0]["distance"]["value"] / 1000
            return distance
        except (IndexError, KeyError):
            print("Error: Unable to extract distance from response data.")
            return 0

    else:
        print(f"Error: API request failed with status code {
              response.status_code}")
        return 0
