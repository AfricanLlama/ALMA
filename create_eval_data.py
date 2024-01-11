## Script to create evaluation data in proper format using existing test data in json format
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data_path')
parser.add_argument('target')
args = parser.parse_args()

# Change these variables to set which test data you want to copy into new format
data_path = args.data_path
target = args.target

test_data = f"{data_path}test.{target}-en.json"
with open(test_data, "r") as f:
    test_list = json.load(f)

eng_path = f"{data_path}test.{target}-en.en"
target_path = f"{data_path}test.{target}-en.{target}"

with open(eng_path, "w") as f:
    for d in test_list:
        f.write(d["translation"]['en'] + "\n")

with open(target_path, "w") as f:
    for d in test_list:
        f.write(d["translation"][target] + "\n")

print("Done!")