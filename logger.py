from person import Person
from virus import Virus

class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        file = open(self.file_name, "w")
        file.write("Simulation Variables: {}\t{}\t{}\t{}\t{}\n".format(pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num))

        file.close()

    def log_interaction(self, person1, person2, did_infect=None,
                        person2_vacc=None, person2_sick=None):
        file = open(self.file_name, "a")

        if did_infect is True:
            file.write("P{} infects P{}.\n".format(person1._id, person2._id))

        elif did_infect is False:
            if person2_vacc is True:
                file.write("P{} did not infect P{} because P{} is vaccinated.\n".format(person1._id, person2._id, person2._id))
            elif person2_sick is True:
                file.write("P{} did not infect P{} because P{} is already sick.\n".format(person1._id, person2._id, person2._id))

        file.close()

    def log_infection_survival(self, person, did_die_from_infection):
        file = open(self.file_name, "a")

        if did_die_from_infection:
            file.write("P{} died from interaction\n".format(person._id, did_die_from_infection))

        else:
            file.write("P{} did not die from interaction\n".format(person._id, did_die_from_infection))

        file.close()

    def log_time_step(self, time_step_number):
        file = open(self.file_name, "a")
        file.write("Time step {} ended, beginning {}\n".format(time_step_number, (time_step_number + 1)))

        file.close()

#testing
def test_write_metadata():
    virus = Virus("HIV", 0.8, 0.3)
    logger = Logger('log.txt')

    logger.write_metadata(10, 0.1, virus.name, virus.mortality_rate, virus.repro_rate)
    logger.log_interaction(Person(1, False, virus), Person(2, False, None), True, False, True)
    logger.log_infection_survival(Person(3, False, virus), True)
    logger.log_time_step(10)
    f = open(logger.file_name, 'r')
