import sqlite3
import sys

sys.path.insert(0, '../input')
from CensusPopEstimateByAge import jolts_jobs_by_region


db_conn = sqlite3.connect('SAJolts.db')


def initialize():
    db_conn.execute("DROP TABLE IF EXISTS SAJolts")
    db_conn.commit()
    try:
        db_conn.execute(
            "CREATE TABLE SAJolts(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Year INTEGER NOT NULL, "
            "South TEXT NOT NULL, SouthJobs INTEGER NOT NULL, Northeast TEXT NOT NULL, NortheastJobs INTEGER NOT NULL, "
            "Midwest TEXT NOT NULL, MidwestJobs INTEGER NOT NULL, West TEXT NOT NULL, WestJobs INTEGER NOT NULL, "
            "UnitedStates TEXT NOT NULL, USJobs INTEGER NOT NULL);")
        db_conn.commit()

        # print("Table Created")

    except sqlite3.OperationalError:
        print("Table couldn't be Created")


def insert_into_db():  # stand alone JOLTS data
    for x in range(2001, 2017):
        data_set = jolts_jobs_by_region(str(x))
        area = 'United States'
        tots = data_set[0][1] + data_set[1][1] + data_set[2][1] + data_set[3][1]
        db_conn.execute("INSERT INTO SAJolts (Year, South, SouthJobs, Northeast, NortheastJobs, Midwest, MidwestJobs,"
                        "West, WestJobs, UnitedStates, USJobs) VALUES ('" + str(x) + "', '"
                        + str(data_set[0][0]) + "', '" + str(data_set[0][1]) + "', '" + str(data_set[1][0]) + "', '"
                        + str(data_set[1][1]) + "', '" + str(data_set[2][0]) + "', '" + str(data_set[2][1]) + "', '"
                        + str(data_set[3][0]) + "', '" + str(data_set[3][1]) + "', '" + area
                        + "', '" + str(tots) + "')")


def get_jolts_stats():
    initialize()
    insert_into_db()
    cursor = db_conn.cursor()
    try:
        result = cursor.execute("SELECT Year, South, SouthJobs, Northeast, NortheastJobs, Midwest, MidwestJobs,"
                                "West, WestJobs, UnitedStates, USJobs FROM SAJolts")
        return result

    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")

    except:
        print("Couldn't Retrieve Data From Database")

