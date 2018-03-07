from UStots import get_us_stats


class USBLSStats:
    def __init__(self, bls=get_us_stats(bls=True)):
        self.bls = bls

    def __iter__(self):
        for data in self.bls:
            yield data

us_bls = list(USBLSStats())

class USCensusStats:
    def __init__(self, census_stats=get_us_stats(census=True)):
        self.census = census_stats

    def __iter__(self):
        for data in self.census:
            yield data

us_census = list(USCensusStats())