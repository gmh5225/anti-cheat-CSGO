import json
import os
import configparser

# Write match ids to a txt file


def write_ids_to_file(ids, filename):
    with open(filename, 'w') as file:
        json.dump(ids, file)
    print("File written: ", filename)

# Read the json file with match details


def read_json_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        # Extract the "match_id" from each JSON object and store it in a list
        data = json.load(file)
    return data


if __name__ == "__main__":

    match_ids = []

    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    config = configparser.ConfigParser()
    config.read('config.ini')
    input_path = config.get('PATHS', 'match_ids_input')
    data = read_json_file(input_path)

    for i in range(0, len(data)):
        for matches in data[i]['items']:
            if matches['status'] == 'FINISHED':
                match_ids.append(matches['match_id'])

    output_dir = config.get('PATHS', 'match_ids_output')
    output_file = os.path.join(output_dir, 'match_ids.txt')

    write_ids_to_file(match_ids, output_file)
