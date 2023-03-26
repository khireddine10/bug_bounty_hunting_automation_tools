import json
import requests
import colorama

colorama.init()

def print_result(profile):
    print(f"\033[1m- {profile['firstName']} {profile['lastName']}\033[0m ({profile['publicIdentifier']})")

# load api key or client id
def load_config():
    with open("config.json") as f:
        config = json.load(f)
    return config

config = load_config()
api_key = config["api_key"]

print("\033[1mThis tool searches for profiles on LinkedIn with a certain skill at a specific company.\033[0m")

company = input("\033[1mEnter the name of the company: \033[0m")
skill = input("\033[1mEnter the name of the skill: \033[0m")

url = f"https://api.linkedin.com/v2/search?q=keywords({skill}) AND companyName({company})&sortBy=relevance&start=0&count=10"

headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

results = response.json()

print(results)

print("\n\033[1mDone!\033[0m")
