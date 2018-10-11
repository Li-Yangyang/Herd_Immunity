import random
from virus import Virus

class Person(object):
    def __init__(self, _id, is_vaccinated, infected=None):
        # TODO:  Finish this method.  Follow the instructions in the class documentation
        # to set the corret values for the following attributes.
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.is_alive = True
        self.infected = infected


    def did_survive_infection(self):
        if self.infected is not None:

            survive_val = random.random()
            # print(survive_val, '#################################')

            if survive_val < self.infected.mortality_rate:
                self.is_alive = False
                return False
            elif survive_val > self.infected.mortality_rate:
                self.is_vaccinated = True
                self.infected = None
                return True

        else:
            return True

if __name__ == "__main__":
    virus = Virus("HIV", 0.8, 0.3)

    person1 = Person(1, False, None)
    print(person1._id, person1.is_alive, person1.is_vaccinated, person1.infected, "-- initiated person 1!")
    survived1 = person1.did_survive_infection()
    print("survived1 value =", survived1)


    person2 = Person(1, False, virus)
    print(person2._id, person2.is_alive, person2.is_vaccinated, person2.infected, "-- initiated person 2!")
    survived2 = person2.did_survive_infection()
    print("survived2 value =", survived2)

#pytest
def test_did_survive_infection():
    virus = Virus("HIV", 0.8, 0.3)

    person1 = Person(1, False, None)
    print(person1._id, person1.is_alive, person1.is_vaccinated, person1.infected, "-- initiated person 1!")

    person2 = Person(2, False, virus)
    print(person2._id, person2.is_alive, person2.is_vaccinated, person2.infected, "-- initiated person 2!")

    survived1 = person1.did_survive_infection()
    print("survived value =", survived1)

    if survived1:
        assert person1.is_alive is True
        assert person1.is_vaccinated is False
        assert person1.infected is None
    else:
        assert person1.is_alive is False

    survived2 = person2.did_survive_infection()
    print("survived value =", survived2)

    if survived2:
        assert person2.is_alive is True
        assert person2.is_vaccinated is True
        assert person2.infected is None
    else:
        assert person2.is_alive is False
