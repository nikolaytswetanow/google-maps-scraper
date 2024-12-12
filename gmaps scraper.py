import googlemaps
from googlemaps.exceptions import ApiError

import requests
import pandas as pd
import time
import os

# API Keys
GOOGLE_MAPS_API_KEY = "AIzaSyDDU2mmKesQ4k75rwLWpwehw5Vc-9MdQnU"
HUNTER_API_KEY = "b66127011119d8facb8fe759868bb31064372b97"

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Search parameters
location = input("Coordinates: ")
radius = input("Radius in meters: ")
keyword = input("Keywords: ")
os.system("cls")

# Fetch places from Google Maps
try:
    results = gmaps.places_nearby(location=location, radius=radius, keyword=keyword)
except ApiError as e:
    # Custom error handling
    print(f"\033[31mThis IP Address is NOT authorized.\033[0m")

except Exception as e:
    # Catch-all for other exceptions
    print(f"An unexpected error occurred: {e}")

# Data collection
data = []

for place in results.get("results", []):
    place_id = place["place_id"]
    details = gmaps.place(place_id=place_id)  # Fetch detailed info for each place

    # Extract Google Maps details
    name = place.get("name", "Not Found")
    formatted_phone_number = details["result"].get("formatted_phone_number", "Not Found")
    website = details["result"].get("website", "Not Found")

    # If a website is available, query Hunter.io for emails and social media
    emails = []

    if website != "No website found":
        domain = website
        hunter_url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
        response = requests.get(hunter_url)
        hunter_data = response.json()

        if "data" in hunter_data and "emails" in hunter_data["data"]:
            for email_entry in hunter_data["data"]["emails"]:
                emails.append(email_entry.get("value"))

    # Append to data list
    data.append({
        "Name": name,
        "Emails": ", ".join(emails) if emails else "No emails found",
        "Website": website,
        "Phone Number": formatted_phone_number,
    })

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_file = "results.xlsx"
df.to_excel(output_file, index=False)

print(f"\033[92mSuccessfully saved to '{output_file}'.")
time.sleep(3)