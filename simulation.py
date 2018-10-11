import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus

class Simulation(object):

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        self.population_size = population_size
        self.population = []
        self.total_infected = initial_infected
        self.current_infected = initial_infected
        self.vacc_percentage = vacc_percentage
        self.virus = Virus(virus_name, mortality_rate, basic_repro_num)
        self.total_dead = []
        self.newly_infected = []

        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(population_size, vacc_percentage, virus_name, mortality_rate,
                           basic_repro_num)

        self._create_population(initial_infected)

    def _create_population(self, initial_infected):
        infected_count = 0
        person_id = 0


        while len(self.population) != self.population_size:

            if infected_count !=  initial_infected:

                new_infected = Person(person_id, False, self.virus)
                self.population.append(new_infected)
                infected_count += 1
                # print('infected')
            else:
                vacc_chance = random.random()

                if vacc_chance < self.vacc_percentage:
                    # print('vacc')
                    new_vaccinated = Person(person_id, True, None)
                    self.population.append(new_vaccinated)

                elif vacc_chance > self.vacc_percentage:
                    # print('not vacc')
                    new_unvaccinated = Person(person_id, False, None)
                    self.population.append(new_unvaccinated)

            person_id += 1



    def _simulation_should_continue(self):
        print("Dead: {}\nInfected: {}\nsCopulation: {}".format(len(self.total_dead), self.current_infected, len(self.population)))
        # if self.total_infected == self.population_size or self.current_infected == 0:
        if int(len(self.total_dead)) + int(self.current_infected) >= int(len(self.population)) or self.current_infected == 0 or self.current_infected > len(self.population):
            return False
        else:
            return True

    def run(self):
        time_step_counter = 0

        should_continue = self._simulation_should_continue()

        while should_continue:
            self.time_step()
            self.logger.log_time_step(time_step_counter)
            time_step_counter += 1

            self._infect_newly_infected()
            self.newly_infected = []
            print(len(self.newly_infected))

            should_continue = self._simulation_should_continue()
            print('NEXT TIME STEP')


        print('The simulation has ended after {} turns.'.format(time_step_counter))

    def time_step(self):
        for person1 in self.population:
            if person1.infected is not None:
                if person1.is_alive:
                    if person1.did_survive_infection():
                        # print("survived")
                        interactions = 0

                        while interactions < 100:
                            # print("selecting person")
                            rand = random.randint(0, len(self.population) - 1)
                            person2 = self.population[rand]
                            # print('person2 {} of {} people - {}'.format(person2._id, len(self.population), rand))
                            # print(interactions)

                            if person2.is_alive:
                                simulation.interaction(person1, person2)
                                interactions += 1
                            else:
                                # print('not alive')
                                continue

                        # print('person {} had 100 interactions'.format(person1._id))

                    else:
                        self.total_dead.append(person1)
                        self.current_infected -= 1
                        # print("PERSON {} DIED".format(person1._id))
            else:
                # print('no infection')
                continue

    def interaction(self, person1, person2):
        assert person1.is_alive == True
        assert person2.is_alive == True

        if person2.is_vaccinated:
            # print('nothing')
            self.logger.log_interaction(person1, person2, False, True, False)
        elif person2.infected is not None:
            # print('person {} already infected'.format(person2._id))
            self.logger.log_interaction(person1, person2, False, False, True)
        else:
            randnum = random.random()
            if randnum < self.virus.repro_rate:
                self.newly_infected.append(person2._id)
                self.logger.log_interaction(person1, person2, True, False, False)
            else:
                # print("not infected")
                pass

    def _infect_newly_infected(self):
        print('INFECTING {} PEOPLE'.format(len(self.newly_infected)))
        for id in self.newly_infected:
            for person in self.population:
                if person._id == id:
                    person.infected = self.virus
                    self.total_infected += 1
                    self.current_infected += 1


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected)
    simulation.run()

#pytest
# def test_simulation():
#     simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)
#     print(simulation.population)
