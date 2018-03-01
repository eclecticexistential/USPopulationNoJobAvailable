import csv
import re


def get_data():
    with open('Original_Datasets/'
              'https___www.bls.gov_news.release_archives_srgune_02282017.htm - Sheet1.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        counter = 7
        while counter > 0:
            next(reader)
            counter -= 1
        for row in reader:
            yield row


# print(list(get_data()))  ...do I need united states row?

def shape_info():  # stats are in strings
    string = get_data()
    conformed_data = []
    for line in string:
        for word in line:
            words = re.search(r'[\w+\s\w]+[\w+]+', word)
            nums = re.findall(r'[\d+,\d]+[\d+.]+', word)
            try:
                conformed_data.append(words.group())
            except AttributeError:
                continue
            str_hold = ""
            for key, num in enumerate(nums):
                for digit in num:
                    if len(num) <= 4:
                        try:
                            if int(num):
                                num += "000"
                                conformed_data.append(int(num))
                        except ValueError:
                            continue
                        break
                    elif len(num) > 4:
                        if digit != ",":
                            str_hold += digit
                        if len(str_hold) == len(num)-1:
                            str_hold += "000"
                            conformed_data.append(int(str_hold))
                            str_hold = ""
    return conformed_data


def make_readable():
    make_dict = []  # may make into a dict()
    array = []
    info = shape_info()
    for item in info:
        if type(item) == str:
            if len(array) != 0:
                make_dict.append(array)
                array = list()
                array.append(item)
            else:
                array.append(item)
        else:
            array.append(item)
    if len(array) != 0:
        make_dict.append(array)
        return make_dict


def consolidate(year):
    closer = make_readable()  # area, 2015POP, 2016POP, 2015CLF, 2016CLF, 2015Emp, 2016Unemp
    for group in closer:
        if group[0] in ['Northeast', 'Midwest', 'South', 'West']:
            if year == '2016':
                yield group[0], group[2], group[4], group[6], group[8]
            elif year == '2015':
                yield group[0], group[1], group[3], group[5], group[7]


def get_inst(year):  # calculates number of institutionalized citizens to use later with census data
    data = list(consolidate(year))
    reset = []
    send = []
    for item in data:
        for a in item:
            send.append(a)
        inst = int(item[1]) - int(item[2])
        send.append(inst)
        reset.append(send)
        send = []
    return reset
