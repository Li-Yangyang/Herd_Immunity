import pytest
from simulation import Simulation
from person import Person
from virus import Virus

def test_init():
    simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)

    assert simulation.population_size is 100
    assert simulation.vacc_percentage is 0.2
    assert simulation.virus.name is "HIV"
    assert simulation.virus.mortality_rate is 0.8
    assert simulation.virus.repro_rate is 0.3
    assert simulation.total_infected is 1

def test_Person_creation():
    person1 = Person(1, False, None)
    assert person1._id is 1
    assert person1.is_vaccinated is False
    assert person1.is_alive is True
    assert person1.infected is None

    virus = Virus("HIV", 0.8, 0.3)
    person2 = Person(2, True, virus)
    assert person2._id is 2
    assert person2.is_vaccinated is True
    assert person1.is_alive is True
    assert person1.infected is None

def test_create_population():
    uninfected = []
    vaccinated = []
    unvaccinated = []


    simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)

    assert len(simulation.population) is 100

    for person in simulation.population:
        if person.infected is None:
            uninfected.append(person)
        if person.is_vaccinated is True:
            vaccinated.append(person)
        if person.is_vaccinated is False:
            unvaccinated.append(person)

    assert len(uninfected) is 99
    assert len(vaccinated) is not 0
    assert len(unvaccinated) is not 0

def test_should_continue_true():
    simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)

    assert simulation._simulation_should_continue() is True

def test_should_continue_deaths_false():
    simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)

    for person in simulation.population:
        person.is_alive == False
        simulation.total_dead.append(person)

    assert simulation._simulation_should_continue() is False

def test_should_continue_deaths_false():
    simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)

    for person in simulation.population:
        person.infected == simulation.virus
        simulation.current_infected += 1

    assert simulation._simulation_should_continue() is False

def test_should_continue_deaths_false():
    simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)

    # TESTING DEATHS
    for person in simulation.population:
        person.is_alive == False
        simulation.total_dead.append(person)
        print(person.is_alive)

    assert simulation._simulation_should_continue() is False

def test_time_step():
    simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)

    simulation.time_step()

    assert len(simulation.total_dead) is not 0

def test_infect_newly_infected():
    simulation = Simulation(100, 0.2, "HIV", 0.8, 0.3, 1)

    for person in simulation.population:
        if person.infected is None:
            simulation.newly_infected.append(person._id)

    simulation._infect_newly_infected()

    for person in simulation.population:
        assert person.infected is simulation.virus
        assert simulation.total_infected is 100
        assert simulation.current_infected is 100
