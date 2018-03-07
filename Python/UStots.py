import sqlite3

from PopEmpJobs2016 import unaltered_bls_data, bls_with_census


def combine_years(fun, year1, year2):
    set_one = fun(year1, us=True)
    set_two = fun(year2, us=True)
    return [set_one, set_two]


db_conn = sqlite3.connect('USBLSStats.db')
censdb_conn = sqlite3.connect('USCensusStats.db')


def initialize_bls():
    db_conn.execute("DROP TABLE IF EXISTS USBLSStats")
    db_conn.commit()
    try:
        db_conn.execute(
            "CREATE TABLE USBLSStats(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Area TEXT NOT NULL, "
            "Year INTEGER NOT NULL, CLFTots INTEGER NOT NULL, UnemployedTots INTEGER NOT NULL,"
            "AvailableJobs INTEGER NOT NULL);")
        db_conn.commit()

        # print("BLS Table Created")

    except sqlite3.OperationalError:
        print("Table couldn't be Created")


def initialize_census():
    censdb_conn.execute("DROP TABLE IF EXISTS USCensusStats")
    censdb_conn.commit()
    try:
        censdb_conn.execute(
            "CREATE TABLE USCensusStats(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Area TEXT NOT NULL, "
            "Year INTEGER NOT NULL, CLFTots INTEGER NOT NULL, UnemployedTots INTEGER NOT NULL,"
            "AvailableJobs INTEGER NOT NULL);")
        censdb_conn.commit()

        # print("Census Table Created")

    except sqlite3.OperationalError:
        print("Table couldn't be Created")


def insert_into_db(data, bls=False, census=False):
    for stats in data:
        if bls:
            db_conn.execute("INSERT INTO USBLSStats (Area, Year, CLFTots, UnemployedTots,"
                            "AvailableJobs) VALUES ('" + str(stats[0]) + "', '"
                            + str(stats[1]) + "', '" + str(stats[2]) + "', '" + str(stats[3])
                            + "', '" + str(stats[4]) + "')")
        if census:
            censdb_conn.execute("INSERT INTO USCensusStats (Area, Year, CLFTots, UnemployedTots,"
                                "AvailableJobs) VALUES ('" + str(stats[0]) + "', '"
                                + str(stats[1]) + "', '" + str(stats[2]) + "', '" + str(stats[3])
                                + "', '" + str(stats[4]) + "')")


def make_bls_db():
    initialize_bls()
    insert_into_db(combine_years(unaltered_bls_data, '2015', '2016'), bls=True)


def make_census_db():
    initialize_census()
    insert_into_db(combine_years(bls_with_census, '2015', '2016'), census=True)


def get_us_stats(bls=False, census=False):
    bls_cursor = db_conn.cursor()
    cens_cursor = censdb_conn.cursor()
    try:
        if bls:
            make_bls_db()
            result = bls_cursor.execute("SELECT UnemployedTots, AvailableJobs FROM USBLSStats")
            return result
        if census:
            make_census_db()
            result = cens_cursor.execute("SELECT UnemployedTots, AvailableJobs FROM USCensusStats")
            return result

    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")

    except:
        print("Couldn't Retrieve Data From Database")

