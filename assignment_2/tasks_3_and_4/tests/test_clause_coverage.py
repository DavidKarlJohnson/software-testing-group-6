import pytest
from tasks_3_and_4.air_traffic_control import air_traffic_control

# TODO - TASK 3
# Clause coverage. (7 points)
# Create a test suite that achieves clause coverage for a selection of 7 clauses of
# your choice. That is, for each clause c ensure there is a test that sets it to true
# and one that sets it to false. Why did you choose these 7 clauses? Does your
# test suite for clause coverage subsume predicate coverage?

# TEST CREATOR:  David Johnson

"""
# NOTE: 7 clauses (atomic) from 'air_traffic_control':
1: runway_clear
2: alternate_runway_available
3: plane_speed
4: emergency
5: wind_speed
6: visibility
7: airport_traffic

The 7 clauses were selected since they all exists within the if-statement of the 'air_traffic_control'
function (mostly as derived conditions). First, I create an initial test (test_clause1), which will make the if-
statement pass. Subsequent tests are meant to ensure that the if-statement doesn't pass by "flipping" the
argument values and testing for the absence of the printout "All conditions met for landing.", which
is exclusive to the if-statement. "Flipping" all the 7 arguments will ensure that they've all been either
True and False at some point, ensuring clause coverage.
"""


# Make the if-statement True
def test_clause1(capsys):
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


# Set RUNWAY_CLEAR to False
# Will make RUNWAY_AVAILABLE False, and if-statement False
def test_clause2(capsys):
    air_traffic_control(
    False,
    False,
    1,
    False,
    1,
    1000,
    1,
    True)
    assert capsys.readouterr().out != 'Debug Info:\nAll conditions met for landing.\n\n'


# Set ALTERNATE_RUNWAY_AVAILABLE to True, and RUNWAY_CLEAR to FALSE
# Will make RUNWAY_AVAILABLE True, and if-statement True
def test_clause3(capsys):
    assert air_traffic_control(
        False,
        True,
        1,
        False,
        1,
        1000,
        1,
        True)
    assert capsys.readouterr().out == 'Debug Info:\nAll conditions met for landing.\n\n'


# Set PLANE_SPEED to 1000
# Will make SAFE_SPEED False, and if-statement False
def test_clause4(capsys):
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


# Set EMERGENCY to True
# Will make if-statement False
def test_clause5(capsys):
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


# Set WIND_SPEED to 1000
# Will make SAFE_WEATHER False, and if-statement False
def test_clause6(capsys):
    assert air_traffic_control(
        True,
        False,
        1,
        False,
        1000,
        1000,
        1,
        True)
    assert capsys.readouterr().out != 'Debug Info:\nAll conditions met for landing.\n\n'


# Set VISIBILITY to 1
# Will make SAFE_WEATHER False, and if-statement False
def test_clause7(capsys):
    assert air_traffic_control(
        True,
        False,
        1,
        False,
        1,
        1,
        1,
        True)
    assert capsys.readouterr().out != 'Debug Info:\nAll conditions met for landing.\n\n'


# Set AIRPORT_TRAFFIC to 1000
# Will make ACCEPTABLE_TRAFFIC False, and if-statement False
def test_clause8(capsys):
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