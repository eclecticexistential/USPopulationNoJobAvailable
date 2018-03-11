from stand_alone_jolts import get_jolts_stats


class JoltsData:
    def __init__(self, jolts=get_jolts_stats()):
        self.jolts = jolts

    def __iter__(self):
        for data in self.jolts:
            yield data

jolts_data = list(JoltsData())

print(jolts_data)