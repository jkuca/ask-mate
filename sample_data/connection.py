import csv
from email import header
import shutil
from tempfile import NamedTemporaryFile


def read_file(directory):
    file = []
    with open(f'sample_data/{directory}', newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            file.append(row)

    return file


def read_header(directory):
    with open(f'sample_data/{directory}', newline='', encoding="utf-8-sig") as csvfile:
        header = csv.DictReader(csvfile).fieldnames
    return header


def get_default_row(directory):
    header


def update_file(row, directory):
    header = read_header(directory)
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(f'sample_data/{directory}', 'r', newline='', encoding="utf-8-sig") as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(
            tempfile, fieldnames=header)
        for item in reader:
            if row['id'] == item['id']:
                item.update(row)
            writer.writerow(item)

    shutil.move(tempfile.name, f'sample_data/{directory}')


def add_new_row(row, directory):
    header = read_header(directory)
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(f'sample_data/{directory}', 'r+', newline='', encoding="utf-8-sig") as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(
            tempfile, fieldnames=header)
        for item in reader:
            writer.writerow(item)
        writer.writerow(row)

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
