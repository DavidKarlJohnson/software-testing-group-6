import pytest
from tasks_3_and_4.air_traffic_control import air_traffic_control

# TODO - TASK 4:
# Test suite for Restricted Active Clause Coverage (RACC). (3 points)
# Create a test suite that achieves RACC restricted to the 3 active clauses you
# identified. That is, for each identified clause c, there is a test t1 which sets c to
# true and a test t2 which sets it to false, and further the value of the predicate is
# different between the two tests.


"""
Identified active clauses:
1) plane_speed
2) emergency
3) airport_traffic

Each active clause has two tests; one where the clause is True and one for False.
To check that the predicate (if-statement) evaluates to True or False, we check the string: 
'Debug Info:\nAll conditions met for landing.\n\n', which is a unique print-out to the if-statement. 
This way we can check if the two tests give different predicate values.
"""


# Active clause PLANE_SPEED set to True
# Predicate evaluates to True
def test_racc1_planespeed_true(capsys):
    assert air_traffic_control(
        True,
        False,
        1,
        False,
        1,
        1000,
        1,
        True)
    assert capsys.readouterr().out == 'Debug Info:\nAll conditions met for landing.\n\n'


# Active clause PLANE_SPEED set to False
# Predicate evaluates to False
def test_racc2_planespeed_false(capsys):
    assert air_traffic_control(
        True,
        False,
        1000,
        False,
        1,
        1000,
        1,
        True)
    assert capsys.readouterr().out != 'Debug Info:\nAll conditions met for landing.\n\n'


# Active clause EMERGENCY set to False
# Predicate evaluates to True
def test_racc3_emergency_false(capsys):
    assert air_traffic_control(
        True,
        False,
        1,
        False,
        1,
        1000,
        1,
        True)
    assert capsys.readouterr().out == 'Debug Info:\nAll conditions met for landing.\n\n'


# Active clause EMERGENCY set to True
# Predicate evaluates to False
def test_racc4_emergency_false(capsys):
    assert air_traffic_control(
        True,
        False,
        1,
        True,
        1,
        1000,
        1,
        True)
    assert capsys.readouterr().out != 'Debug Info:\nAll conditions met for landing.\n\n'


# Active clause AIRPORT_TRAFFIC set to True
# Predicate evaluates to True
def test_racc5_airporttraffic_true(capsys):
    assert air_traffic_control(
        True,
        False,
        1,
        False,
        1,
        1000,
        1,
        True)
    assert capsys.readouterr().out == 'Debug Info:\nAll conditions met for landing.\n\n'


# Active clause AIRPORT_TRAFFIC set to False
# Predicate evaluates to False
def test_racc6_airporttraffic_false(capsys):
    assert air_traffic_control(
        True,
        False,
        1,
        False,
        1,
        1000,
        1000,
        True)
    assert capsys.readouterr().out != 'Debug Info:\nAll conditions met for landing.\n\n'