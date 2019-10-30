import csv



def get_csv_data(filename):
    list_of_data = []
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file)
        for item in reader:
            list_of_data.append(dict(item))
    return list_of_data


