import json
from algoliasearch.search_client import SearchClient

# Connect and authenticate with your Algolia app
client = SearchClient.create("SK1QL8DGIA", "2f1a762808fec3bad0a5b67ee019a461")
print(type(client.list_indices()))
with open("sample.json", "w") as outfile:
    outfile.write(json.dumps(client.list_indices(), indent=4))