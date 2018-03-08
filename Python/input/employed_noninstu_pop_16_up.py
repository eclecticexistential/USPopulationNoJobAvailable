import csv
import re


def get_bls_data_2015():
    with open('../../Original_Datasets/'
              'https___www.bls.gov_news.release_archives_srgune_02282017.htm - Sheet1.csv', 'r') as csvfile2015:
        reader2015 = csv.reader(csvfile2015)
        counter = 8
        while counter > 0:
            next(reader2015)
            counter -= 1
        for row in reader2015:
            yield row


def get_bls_data_2016():
    with open('../../Original_Datasets/'
              'https___www.bls.gov_news.release_srgune.t01.htm - Sheet1.csv', 'r') as csvfile2016:
        reader2016 = csv.reader(csvfile2016)
        counter = 5
        while counter > 0:
            next(reader2016)
            counter -= 1
        for row in reader2016:
            yield row


def shape_bls_info(string):  # stats are in strings
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


def make_bls_info_readable(dataset):
    make_dict = []  # may make into a dict()
    array = []
    info = shape_bls_info(dataset)
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


def consolidate_data_by_year_and_region(year, dataset):
    closer = make_bls_info_readable(dataset)  # area, 2015POP, 2016POP, 2015CLF, 2016CLF, 2015Emp, 2016Unemp
    for group in closer:
        if group[0] in ['Northeast', 'Midwest', 'South', 'West']:
            if year == '2015' or year == '2016':
                yield group[0], group[1], group[3], group[5], group[7]
            elif year == '2017':
                yield group[0], group[2], group[4], group[6], group[8]


def identify_inst_pop(year, dataset):  # calculates number of institutionalized citizens to use later with census data
    data = list(consolidate_data_by_year_and_region(year, dataset))
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


def get_stats_by_year(year):
    if year == '2015':
        return identify_inst_pop('2015', get_bls_data_2015())
    elif year == '2016':
        return identify_inst_pop('2016', get_bls_data_2016())
