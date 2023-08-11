from awpy import DemoParser
import pandas as pd
import os
import json
import configparser

# Set the parse_rate equal to the tick rate at which you would like to parse the frames of the demo.
# This parameter only matters if parse_frames=True ()
# For reference, MM demos are usually 64 ticks, and pro/FACEIT demos are usually 128 ticks.


def write_to_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)


# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

csv_dir = config.get('Paths', 'csv_dir')
json_dir = config.get('Paths', 'json_dir')
in_path = config.get('Paths', 'in_path')


# Create output directories if they don't exist
os.makedirs(csv_dir, exist_ok=True)
os.makedirs(json_dir, exist_ok=True)

demo_files = [f for f in os.listdir(in_path) if f.endswith(".dem")]

for dnum, demo_filename in enumerate(demo_files, start=1):
    file_loc = os.path.join(in_path, demo_filename)
    demo_parser = DemoParser(
        demofile=file_loc, demo_id=f"match{dnum}", parse_rate=128)
    print(f"Parsing demo {demo_filename} (match{dnum})")

    # Parse the demofile, output results to dictionary with df name as key
    data = demo_parser.parse()

    # Parse the data into dataframes using
    df = demo_parser.parse(return_type="df")
    output_json_filename = os.path.join(json_dir, f"data_{dnum}.json")
    write_to_json(data["gameRounds"], output_json_filename)

    # Convert data to Pandas DataFrame
    df = pd.DataFrame(data["gameRounds"])
    csv_filename = os.path.join(csv_dir, f"data_{dnum}.csv")
    df.to_csv(csv_filename, index=False)

    print(
        f"Processed demo {demo_filename} (match{dnum}) and saved data to {output_json_filename} and {csv_filename}")
    if dnum == 1:
        break

print("Parsing complete!")
