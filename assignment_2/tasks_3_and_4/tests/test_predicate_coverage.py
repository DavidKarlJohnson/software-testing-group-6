import pytest
from tasks_3_and_4.air_traffic_control import air_traffic_control

# TODO - TASK 3:
# Predicate coverage. (3 points)
# Create a test suite that achieves predicate coverage. The set of predicates to be
# considered are those in the if conditions in the decision making process.

# TEST CREATOR:  David Johnson


# Test 1: Make the predicate in the if-condition of the
# function 'air_traffic_control' TRUE
def test_predicate_true(capsys):
    assert air_traffic_control(
        True,
       True,
       100,
       False,
       30,
       1001,
       4,
       False) == 'Landing Allowed'
    assert capsys.readouterr().out == 'Debug Info:\nAll conditions met for landing.\n\n'




# Test 2: Make the predicate in the if-condition of the
# function 'air_traffic_control' FALSE, by changing
# 'emergency' to True.
def test_predicate_false(capsys):
    assert air_traffic_control(
        True,
       True,
       100,
       True,
       30,
       1001,
       4,
       False)
    assert capsys.readouterr().out != 'Debug Info:\nAll conditions met for landing.\n\n'

