import pytest
from tasks_3_and_4.air_traffic_control import air_traffic_control

# TODO - TASK 3
# Clause coverage. (7 points)
# Create a test suite that achieves clause coverage for a selection of 7 clauses of
# your choice. That is, for each clause c ensure there is a test that sets it to true
# and one that sets it to false. Why did you choose these 7 clauses? Does your
# test suite for clause coverage subsume predicate coverage?

# TEST CREATOR:  David Johnson

# NOTE: 7 clauses from 'air_traffic_control':
# A = runway_available  ==  runway_clear OR alternate_runway_available
# B = safe_speed  ==  plane_speed < 150
# C = emergency
# D = acceptable_traffic   ==  airport_traffic <= 5
# E = traffic_override  ==  priority_status AND airport_traffic <= 8
# F = safe_weather  ==  wind_speed <= 40 AND visibility >= 1000
# G = weather_override  ==  priority_status AND NOT safe_weather


# A = B = C = D = E = F = True
# G = False
def test_clause1():
    assert air_traffic_control(
        True,
        True,
        100,
        True,
        30,
        1100,
        4,
        True) == 'Landing Allowed'


# A = B = C = D = E = F = False
# G = True
def test_clause2():
    assert air_traffic_control(
        False,
        True,
        200,
        False,
        50,
        1100,
        10,
        True) == 'Landing Allowed'