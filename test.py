import csv

with open("sample_data/question.csv", "r", newline="") as file:
    read = file.readlines()
    header = [element for i, element in enumerate(read) if i == 0]
    print(header)
