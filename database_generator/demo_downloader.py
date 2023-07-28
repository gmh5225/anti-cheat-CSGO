import requests
import json
import re
import configparser


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


def read_json_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        # Extract the "match_id" from text file
        data = file.read()

        # Clean data
        pattern = r'"([a-zA-Z0-9-]+)"'
        data_clean = re.findall(pattern, data)
    return data_clean


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


def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
    print("File written: ", filename)


if __name__ == "__main__":
    # Replace 'YOUR_FACEIT_API_KEY' with your actual Faceit API key
    config = configparser.ConfigParser()
    config.read('config.ini')
    faceit_api_key = config.get('API_KEYS', 'api_key_1')

    # path to match_details text file
    input_path = "D:\\faceit_demos"

    # function to read match_ids from math_ids.txt
    data = read_json_file(input_path)
    dnum = 0
    for match_id in data:

        details = get_match_details(faceit_api_key, match_id)
        urls = details['demo_url']
        dnum += 1

        for url in urls:

            # Change this to your desired save path
            save_path = f"C:\\Users\\bhatn\\Desktop\\faceit_demos\\demo{dnum}.dem.gz"
            download_demo(url, save_path)
