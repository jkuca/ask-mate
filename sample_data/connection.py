import csv
import shutil
from tempfile import NamedTemporaryFile


def read_file(directory):
    _list = []
    try:
        with open(f'sample_data/{directory}', newline='', encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                _list.append(row)
    except(ValueError):
        print(ValueError)

    return _list


def read_header(directory):
    with open(f'sample_data/{directory}', newline='', encoding="utf-8-sig") as csvfile:
        header = csv.DictReader(csvfile).fieldnames

    return header


def write_file(row, directory):
    header = read_header(directory)
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(f'sample_data/{directory}', 'r+', newline='', encoding="utf-8-sig") as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(
            tempfile, fieldnames=header)
        for item in reader:
            if row['id'] == item['id']:
                print('im in')
                item['id'] = row['id']
                item['message'] = row['message']
            writer.writerow(item)

    shutil.move(tempfile.name, f'sample_data/{directory}')


def delete_row(row, directory):
    header = read_header(directory)
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(f'sample_data/{directory}', 'r', newline='', encoding="utf-8-sig") as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(
            tempfile, fieldnames=header)

        for item in reader:
            if row['id'] != item['id']:
                writer.writerow(item)

    shutil.move(tempfile.name, f'sample_data/{directory}')


write_file({'id': '3', 'submission_time': 123123124, 'view_number': 1, 'vote_number': 1, 'title': 'dasda', 'message': 'asdasda', 'image': None
            }, 'question.csv')
