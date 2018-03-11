import csv
from JOLTS2016 import reduce_jolts_data_by_area
from areas_by_region import sep_state_region


def get_census_pop_by_area_age(area, year, age=16, retire=True):  # gets state population between 16-67
    with open('../../Original_Datasets/sc-est2016-agesex-civ.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        under_16 = 0
        for row in reader:
            if row[4] == area:
                if row[5] == '0':  # gets both male and female stats
                    if age != 999:
                        if int(row[6]) >= age:
                            if retire:
                                if year == '2016':
                                    if int(row[6]) <= 67:
                                        yield [row[4], int(row[6]), int(row[len(row)-1])]
                                elif year == '2015':
                                    if int(row[6]) <= 67:
                                        yield [row[4], int(row[6]), int(row[len(row)-2])]
                            else:
                                if year == '2016':
                                    if int(row[6]) != 999:
                                        yield [row[4], int(row[6]), int(row[len(row) - 1])]
                                elif year == '2015':
                                    if int(row[6]) != 999:
                                        yield [row[4], int(row[6]), int(row[len(row) - 2])]
                    elif age == 999:  # optional way to get all tots for an area 16-85...probably don't need
                        if year == '2016':
                            if int(row[6]) < 16:
                                under_16 += int(row[len(row) - 1])
                            if int(row[6]) == 999:
                                above_15 = int(row[len(row) - 1]) - under_16
                                yield [row[4], int(row[6]), above_15]
                        elif year == '2015':
                            if int(row[6]) < 16:
                                under_16 += int(row[len(row) - 2])
                            if int(row[6]) == 999:
                                above_15 = int(row[len(row)-2]) - under_16
                                yield [row[4], int(row[6]), above_15]


def put_census_pop_into_region(region, year, age, retire):
    states = sep_state_region(region)  # puts states into regions
    for state in states:
        yield get_census_pop_by_area_age(state, year, age, retire)  # --> [state, age, pop]


def add_census_pop_by_region(area, year, age=16, retire=True):
    run_tot_reg = 0
    areas_age = put_census_pop_into_region(area, year, age, retire)  # find people in a region between 16-67
    a_age_tots = []
    for pop in areas_age:
        for stat in pop:
            run_tot_reg += stat[2]  # adds up all pop by age in designated region, by state
    a_age_tots.extend([area, run_tot_reg])
    return a_age_tots


def get_total_census_pop(year, retire=True):  # gets population for each region adds to get US Pop tots
    areas = ['South', 'Northeast', 'Midwest', 'West']
    by_area = []
    tots = 0
    for area in areas:
        data = add_census_pop_by_region(area, year, retire)
        by_area.append(data)
        tots += data[1]
    by_area.append(['United States', tots])
    return by_area


def jolts_jobs_by_region(year):  # gets stats from JOLTS file
    areas = ['South', 'Northeast', 'Midwest', 'West']
    by_region = []
    for area in areas:
            by_region.append([area, reduce_jolts_data_by_area(area, year)])
    return by_region


def full_jolts_set_by_region():  # stand alone JOLTS data
    years_array = []
    for x in range(2001, 2017):
        data_set = jolts_jobs_by_region(str(x))
        tots = data_set[0][1] + data_set[1][1] + data_set[2][1] + data_set[3][1]
        group = [x]
        group.extend(data_set)
        group.append(['United States', tots])
        years_array.append(group)
    return years_array
