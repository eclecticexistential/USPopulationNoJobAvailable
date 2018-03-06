from PopEmpJobs2016 import retrieve_stats


class BLSData:
    def __init__(self, bls=retrieve_stats(bls=True)):
        self.bls = bls

    def __iter__(self):
        for stat in self.bls:
            yield stat

unaltered = list(BLSData())


class CensusData:
    def __init__(self, census_stats=retrieve_stats(census=True)):
        self.census = census_stats

    def __iter__(self):
        for data in self.census:
            yield data

census = list(CensusData())


