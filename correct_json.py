import json
import argparse

def change_label(file_path, old, new):
    with open(file_path, 'r') as f:
        data = json.load(f)

    for i in range(len(data)):
        old_data = data[i]['translation'][old]
        del data[i]['translation'][old]
        data[i]['translation'][new] = old_data

    with open(file_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

def make_list(file_path):
    with open(file_path) as f:
        lines = f.read().splitlines()

    if (lines[0][0] == "["):
        return
    
    num = len(lines)
    with open(file_path, "w") as f:
        f.write("[")
        for i in range(num - 1):
            f.write(lines[i] + ",\n")
        f.write(lines[num - 1])
        f.write("]")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('file_path', type=str, help='File path')
    parser.add_argument('old_label', type=str, help='Old label')
    parser.add_argument('new_label', type=str, help='New label')

    args = parser.parse_args()
    ### If label arg is given, we change the label, else we turn the non-list json into a list
    if (args.old_label):
        change_label(args.file_path, args.old_label, args.new_label)
    else:
        make_list(args.file_path)



