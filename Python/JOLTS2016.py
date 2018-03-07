import csv


def pull_jolts_data(year):
    new_info = []
    with open('../Original_Datasets/JOTLS 2000-2017 Open Jobs - Sheet1.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            for item in row:
                if item[:4] == 'JTS0' and item[11:14] == 'JOL':
                    if item[25:29] == year:
                        new_info.append([item[:14], item[25:29], item[56:60]])
    return new_info


def clean_jolts_data(year):  # gets data by year
    info = pull_jolts_data(year)
    counter = 0
    digit = 0
    new = []
    for value in info:
        value[2] += "000"
        digit += int(value[2])
        counter += 1
        if counter == 11:
            new.append([value[0], value[1], round(digit/12)])
            digit = 0
            counter = 0
    return new


def reduce_jolts_data_by_area(area, year):  # use built-in coding to find seasonally adjusted stats by area
    get_set = clean_jolts_data(year)
    search = "JTS000000"
    if area == 'South':
        search += 'SOJOL'
    elif area == 'Northeast':
        search += 'NEJOL'
    elif area == 'West':
        search += 'WEJOL'
    elif area == 'Midwest':
        search += 'MWJOL'
    else:
        search += '00JOL'
    for a in get_set:
        if a[0] == search:
            return a[2]
