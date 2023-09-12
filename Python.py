import requests

url = "https://cedt-gct-bitbucket.nam.nsroot.net/bitbucket/rest/api/1.0/dashboard/pull-requests"
all_items = []

while url:
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get("values", [])
        all_items.extend(items)
        
        # Check if there's a link to the next page in the response headers
        next_url = data.get("next")
        
        if next_url:
            url = next_url
        else:
            url = None  # No more pages, exit the loop
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        break

# Now, all_items contains all the items from all pages
