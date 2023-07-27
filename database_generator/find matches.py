import requests
import json
import os
import configparser


def get_match_details(api_key):
    base_url = "https://open.faceit.com/data/v4/games/csgo/matchmakings?region=EU&offset=0&limit=20"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    url = f"{base_url}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
    print("File written: ", filename)


if __name__ == "__main__":
    # Faceit API key
    config = configparser.ConfigParser()
    config.read('config.ini')
    faceit_api_key = config.get('API_KEYS', 'api_key_1')

    match_details = get_match_details(faceit_api_key)
    if match_details:
        # Clean up the JSON response for better viewing
        formatted_json = json.dumps(match_details, indent=2)

        output_path = r"C:\\Users\\bhatn\\Desktop\\anticheat"
        # Create the directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        json_filename = os.path.join(output_path, 'match_details.json')
        write_json_to_file(match_details, json_filename)
