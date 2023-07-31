import os
import requests

# Set your Kentik API credentials
email = os.getenv('mail')
token = os.getenv('password')

# Define the API URL
url = "https://api.kentik.com/api/v5/query/topXdata"

# Define the headers for the API request
headers = {
    'X-CH-Auth-Email': email,
    'X-CH-Auth-API-Token': token,
    'Content-Type': 'application/json'
}

# Define the SQL query
data = {
    "query": {
        "queryString": "SELECT src_as, sum(flow_octets) as volume FROM all_devices WHERE src_as != 0 GROUP BY src_as ORDER BY volume DESC LIMIT 10",
        "queryTitle": "Top 10 Source ASNs",
        "queryType": "topXdata"
    }
}

# Make the API request
response = requests.post(url, headers=headers, json=data)

# If the request was successful, print the results
if response.status_code == 200:
    results = response.json()
    for row in results['results']:
        print(f"ASN: {row['src_as']}, Volume: {row['volume']}")
else:
    print(f"API request failed with status code {response.status_code}")
