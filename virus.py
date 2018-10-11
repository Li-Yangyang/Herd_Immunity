class Virus(object):
    def __init__(self, name, mortality_rate, repro_rate):
        self.name = name
        self.mortality_rate = mortality_rate
        self.repro_rate = repro_rate

# PyTest style test function
def test_virus_instantiation():
    virus = Virus("HIV", 0.8, 0.3)

    assert virus.name == "HIV"
    assert virus.mortality_rate == 0.8
    assert virus.repro_rate == 0.3
