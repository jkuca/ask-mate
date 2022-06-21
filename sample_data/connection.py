import csv


def read_file(dierctory):
    _list = []
    try:
        with open(f'sample_data/{dierctory}', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                _list.append(row)
    except(ValueError):
        print(ValueError)

    return _list


def write_file(row, dierctory):
    with open(f'sample_data/{dierctory}', 'w', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

    if row in reader:
        for item in reader:
            if row['id'] == item['id']:
                item = row
            reader.writerow(item)
    else:
        reader.writerow(row)
