import requests

def get_nationality(name):
    url = f"https://api.nationalize.io/?name={name}"
    response = requests.get(url)
    data = response.json()
    return data

name = "viktoria"
result = get_nationality(name)
print(f"results '{name}':")
for item in result['country']:
    print(f"Country: {item['country_id']}, Probability : {item['probability']}")
