import json


# Write match ids to a json file
def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
    print("File written: ", filename)

# Read the json file with match details


def read_json_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        # Extract the "match_id" from each JSON object and store it in a list
        data = json.load(file)
    return data


if __name__ == "__main__":

    match_ids = []
    input_path = "C:\\Users\\bhatn\\Desktop\\anticheat\\database_generator\\match_details.json"
    data = read_json_file(input_path)

    for i in range(0, len(data)):
        for matches in data[i]['items']:
            if matches['status'] == 'FINISHED':
                match_ids.append(matches['match_id'])

write_json_to_file(match_ids, 'match_ids.json')
