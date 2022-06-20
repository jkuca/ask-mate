import csv

with open("sample_data/question.csv", "r", newline="") as file:
    data = {}
    header = [file.readline()]
    read = file.readlines()
    for key in header:
        for value in read:
            subdata = {}
            subdata.setdefault(key, value)
    print(data)
