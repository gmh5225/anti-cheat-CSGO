import requests
import json
import os
import configparser


# Read the json file with hub details
def read_json_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        # Extract the "hub_id" from each JSON object and store it in a list
        for hub in file:
            data = json.loads(hub)
            hub_ids.append(data['hub_id'])
    return hub_ids


# Use the hub_id to find past matches
def get_hub_matches(api_key, hub_id_list):
    base_url = "https://open.faceit.com/data/v4/hubs/{hub_id}/matches?type=past&offset=0&limit=20"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    results = []

    for hub_id in hub_id_list:
        url = base_url.format(hub_id=hub_id)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results.append(response.json())
        else:
            print(
                f"Error for hub_id {hub_id}: {response.status_code} - {response.text}")
    return results


# Write match details to a json file
def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
    print("File written: ", filename)


if __name__ == "__main__":

    # use faceit open API key
    config =  configparser.ConfigParser()
    config.read('config.ini')
    faceit_api_key = config.get('API_KEYS', 'api_key_1')

    # PATH TO hub_details JSON FILE
    input_path = "C:\\Users\\bhatn\\Desktop\\anticheat\\hub_details.json"

    hub_ids = []
    hub_data = read_json_file(input_path)

    match_details = get_hub_matches(faceit_api_key, hub_data)

    if match_details:
        # Clean up the JSON response for better viewing
        formatted_json = json.dumps(match_details, indent=2)

        # Specify path of output json file
        output_path = r"C:\\Users\\bhatn\\Desktop\\anticheat"
        # Create the directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        # Write the match details to a json file
        json_filename = os.path.join(output_path, 'match_details.json')
        write_json_to_file(match_details, json_filename)
