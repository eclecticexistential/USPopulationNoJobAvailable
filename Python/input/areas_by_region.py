import csv


def sep_state_region(region):
    with open('../../Original_Datasets/us census bureau regions and divisions.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        regions_by_state = []
        for row in reader:
            if row[2] == region and row[0] != 'District of Columbia':
                regions_by_state.append(row[0])
    return regions_by_state


def get_states_abb_into_region(region):  # added specifically for bokeh state sample data
    with open('../../Original_Datasets/us census bureau regions and divisions.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        regions_by_state_abb = []
        for row in reader:
            if row[2] == region and row[0] != 'District of Columbia':
                regions_by_state_abb.append(row[1])
    return regions_by_state_abb
