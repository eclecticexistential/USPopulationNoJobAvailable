import sqlite3
import sys

sys.path.insert(0, '../input')

from CensusPopEstimateByAge import *
from employed_noninstu_pop_16_up import *


def unaltered_bls_data(year, us=False):
    area_av_job = get_stats_by_year(year)  # region, pop, CLF, emp, unemployed, institutionalized
    able_to_work_but_no_job = []
    clf_regions = 0
    unemp_regions = 0
    avjob_regions = 0
    us_tots = []
    for info in area_av_job:
        for intel in jolts_jobs_by_region(year):
            if info[0] == intel[0]:
                clf_regions += info[2]
                unemp_regions += info[4]
                avjob_regions += intel[1]
                can_work_minus_available_jobs = info[4] - intel[1]
                able_to_work_but_no_job.append([info[0], year, can_work_minus_available_jobs])
    if us:
        us_tots.extend(['United States', year, clf_regions, unemp_regions, avjob_regions])
        return us_tots
    else:
        return able_to_work_but_no_job


# CLF Unemployed JOLTS
def bls_with_census(year, us=False):
    ages_16_67 = get_total_census_pop(year)  # total population 16-67 in a region
    area_av_job = get_stats_by_year(year)  # region, pop, CLF, emp, unemployed, institutionalized
    clf_regions = 0
    unemp_regions = 0
    avjob_regions = 0
    us_tots= []
    census_data = []
    for info in area_av_job:
        for stats in ages_16_67:
            if info[0] == stats[0]:
                census_pop_minus_institutionalized = stats[1] - info[5]
                can_work_minus_employed = census_pop_minus_institutionalized - info[3]
                for intel in jolts_jobs_by_region(year):
                    if intel[0] == info[0]:
                        clf_regions += census_pop_minus_institutionalized
                        unemp_regions += can_work_minus_employed
                        avjob_regions += intel[1]
                        unemp_minus_jobs_available = can_work_minus_employed - intel[1]
                        census_data.append([info[0], year, unemp_minus_jobs_available])
    if us:
        us_tots.extend(['United States', year, clf_regions, unemp_regions, avjob_regions])
        return us_tots
    else:
        return census_data


def combine_year_sets(fun1, year1, year2):
    get_info1 = fun1(year1)
    get_info2 = fun1(year2)
    re_da = []
    for item in get_info1:
        for info in get_info2:
            if item[0] == info[0]:
                re_da.append([item[0], item[2], info[2]])
    return re_da


def combine_bls_census_into_one():
    unaltered = combine_year_sets(unaltered_bls_data, '2015', '2016')
    census = combine_year_sets(bls_with_census, '2015', '2016')
    er_ad = []
    for bls in unaltered:
        for cen in census:
            if bls[0] == cen[0]:
                er_ad.append([bls[0], bls[1], bls[2], cen[1], cen[2]])
    return er_ad


db_conn = sqlite3.connect('complete.db')


def initialize():
    db_conn.execute("DROP TABLE IF EXISTS Complete")
    db_conn.commit()
    try:
        db_conn.execute(
            "CREATE TABLE Complete(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Area TEXT NOT NULL, "
            "BLSNoJobAvail2015 INTEGER NOT NULL, BLSNoJobAvail2016 INTEGER NOT NULL, "
            "CensusNoJobAvail2015 INTEGER NOT NULL, CensusNoJobAvail2016 INTEGER NOT NULL);")
        db_conn.commit()

        # print("Table Created")

    except sqlite3.OperationalError:
        print("Table couldn't be Created")


def insert_into_db():
    for stats in combine_bls_census_into_one():
        db_conn.execute("INSERT INTO Complete (Area, BLSNoJobAvail2015, BLSNoJobAvail2016,"
                        "CensusNoJobAvail2015, CensusNoJobAvail2016) VALUES ('" + str(
                         stats[0]) + "', '" + str(stats[1]) + "', '" + str(stats[2])
                        + "', '" + str(stats[3]) + "', '" + str(stats[4]) + "')")


def make_db():
    initialize()
    insert_into_db()


def retrieve_stats(bls=False, census=False):
    make_db()
    the_cursor = db_conn.cursor()
    try:
        if bls:
            result = the_cursor.execute("SELECT Area, BLSNoJobAvail2015, BLSNoJobAvail2016 FROM Complete")
            return result
        if census:
            result = the_cursor.execute("SELECT Area, CensusNoJobAvail2015, CensusNoJobAvail2016 FROM Complete")
            return result

    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")

    except:
        print("Couldn't Retrieve Data From Database")

