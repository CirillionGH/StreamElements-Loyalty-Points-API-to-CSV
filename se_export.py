import csv
import requests

# --- CONFIGURATION ---
# We put your ID inside quotes here so Python knows it is text, not a number!
CHANNEL_ID = "CHANNEL_ID" <-- Paste your CHANNEL ID inside these quotes
JWT_TOKEN = "JWTTOKEN"  # <-- Paste your secret JWT token inside these quotes
OUTPUT_FILENAME = "streamelements_loyalty.csv"
# ---------------------

# Leave this line completely alone! It will automatically grab your CHANNEL_ID from above.
BASE_URL = f"https://api.streamelements.com/kappa/v2/points/{CHANNEL_ID}/top"
headers = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Accept": "application/json"
}

limit = 100
offset = 0
all_exported_users = []

print("🚀 Connecting to StreamElements API...")

while True:
    print(f"Fetching records {offset} through {offset + limit}...")
    params = {"limit": limit, "offset": offset}
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        if response.status_code != 200:
            print(f"❌ Error fetching data: {response.status_code} - {response.text}")
            break
            
        data = response.json()
        
        if isinstance(data, list):
            page_users = data
        elif isinstance(data, dict) and "users" in data:
            page_users = data["users"]
        else:
            page_users = []
            
        if not page_users:
            print("🏁 No more users found. Wrapping up data formatting...")
            break
            
        for user in page_users:
            username = user.get("username")
            points = user.get("points")
            
            if username and points is not None:
                all_exported_users.append({"Username": username, "Points": points})
                
        if len(page_users) < limit:
            break
            
        offset += limit
        
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
        break

if all_exported_users:
    with open(OUTPUT_FILENAME, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Username", "Points"])
        writer.writeheader()
        writer.writerows(all_exported_users)
    print(f"✅ Success! Exported {len(all_exported_users)} users straight to '{OUTPUT_FILENAME}'.")
else:
    print("⚠️ Process finished, but no data could be compiled.")