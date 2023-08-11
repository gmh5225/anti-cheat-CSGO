import requests
import json
import re
import configparser
import os

# Function to download the demo (.dem) file


def download_demo(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Demo downloaded successfully to: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the demo: {e}")

# Function to read the match_id from the text file


def read_json_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        # Extract the "match_id" from text file
        data = file.read()

        # Clean data
        pattern = r'"([a-zA-Z0-9-]+)"'
        data_clean = re.findall(pattern, data)
    return data_clean

# Function to get the match details


def get_match_details(api_key, match_id):
    base_url = "https://open.faceit.com/data/v4/matches/"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    url = f"{base_url}{match_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to write the match details to a json file


def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
    print("File written: ", filename)


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Replace with your actual Faceit API key from https://developers.faceit.com/
    faceit_api_key = config.get('API_KEYS', 'api_key_1')

    # path to match_details text file
    downloader_input = config.get('PATHS', 'downloader_input')

    # path to save the demo files
    save_path_base = config.get('PATHS', 'save_path')

    # Read match_ids from match_ids.txt
    data = read_json_file(downloader_input)
    dnum = 0
    for match_id in data:

        # Retrive match details for each match_id
        details = get_match_details(faceit_api_key, match_id)
        urls = details['demo_url']
        dnum += 1
        if dnum == 2:
            break
        # Retrive a demo file for each url in match_details
        for url in urls:

            # Change this to your desired save path
            save_path = os.path.join(save_path_base, f"demo{dnum}.dem.gz")
            download_demo(url, save_path)
