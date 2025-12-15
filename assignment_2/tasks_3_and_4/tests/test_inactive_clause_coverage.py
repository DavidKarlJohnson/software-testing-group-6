import pytest
from tasks_3_and_4.air_traffic_control import air_traffic_control

# TODO - TASK 4:
# Test suite for inactive clause coverage. (4 points)
# Identify 2 inactive clauses i.e. a clause c and a valuation f of the clauses in for
# a particular predicate such that if the truth value of c is changed while retain-
# ing the truth value of the other clauses, then the truth value of the predicate
# does not change. Create a test suite that achieves Restricted Inactive Clause
# Coverage for the two inactive clauses that you have identified.
# Why do your two test suites differ? Can you explain how your test suites
# achieve the targeted coverage?


"""
We've identified the following atomic clauses in the first elif-statement of the 'air_traffic_control' function:
1) airport_traffic  (part of derived condition: acceptable_traffic)
2) wind_speed       (part of derived condition: safe_weather)

We've created two different tests for each identified clause (resulting in four tests total):
    * One where the evaluation of the elif predicate is True.
    * One where the evaluation of the elif predicate is False.
For each of these two tests we flip the values of the identified atomic clauses from True to False in order to show that
they do not have any effect on the evaluation of the predicate, proving that they are indeed inactive. The DIFFERENCE
between the two types of tests is that one will take the first elif branch, which the other doesn't (which allows us to
prove inactivity of the identified atomic clauses).

If reason for picking the first elif-statement of the function, and not the if-statement is because the if-statement
doesn't allow all four requirements to achieve ICC:
1) Clause = True, Predicate = True
2) Clause = False, Predicate = True
3) Clause = True, Predicate = False
4) Clause = False, Predicate = False
"""

# Set atomic clause AIRPORT_TRAFFIC to True/False (affecting derived condition ACCEPTABLE_TRAFFIC),
# proving that the clause is inactive since the predicate (first elif-statement) doesn't change its evaluation (True)
def test_icc1_airporttraffic_pred_true(capsys):
    # airport_traffic = True, Predicate = True
    air_traffic_control(
        True,
        False,
        1,
        False,
        1000,
        1000,
        1,
        True)
    first_output = capsys.readouterr().out

    # airport_traffic = False, Predicate = True
    air_traffic_control(
        True,
        False,
        1,
        False,
        1000,
        1000,
        6,
        True)
    second_output = capsys.readouterr().out

    assert first_output != 'All conditions met for landing.\n\n'
    assert second_output != 'All conditions met for landing.\n\n'
    assert first_output == 'Debug Info:\nLanding allowed with priority overrides.\n\n'
    assert second_output == 'Debug Info:\nLanding allowed with priority overrides.\n\n'


# Set atomic clause AIRPORT_TRAFFIC to True/False (affecting derived condition ACCEPTABLE_TRAFFIC),
# proving that the clause is inactive since the predicate (first elif-statement) doesn't change its evaluation (False)
def test_icc2_airporttraffic_pred_false(capsys):
    # airport_traffic = True, Predicate = False
    air_traffic_control(
        True,
        False,
        1,
        False,
        1000,
        1000,
        1,
        False)
    first_output = capsys.readouterr().out

    # airport_traffic = False, Predicate = False
    air_traffic_control(
        True,
        False,
        1,
        False,
        1000,
        1000,
        6,
        False)
    second_output = capsys.readouterr().out

    assert first_output != 'All conditions met for landing.\n\n'
    assert second_output != 'All conditions met for landing.\n\n'
    assert first_output != 'Debug Info:\nLanding allowed with priority overrides.\n\n'
    assert second_output != 'Debug Info:\nLanding allowed with priority overrides.\n\n'


# Set atomic clause WIND_SPEED to True/False (affecting derived condition SAFE_WEATHER),
# proving that the clause is inactive since the predicate (first elif-statement) doesn't change its evaluation (True)
def test_icc3_windspeed_pred_true(capsys):
    # wind_speed = True, Predicate = True
    air_traffic_control(
        True,
        False,
        1,
        False,
        1,
        1000,
        6,
        True)
    first_output = capsys.readouterr().out

    # wind_speed = False, Predicate = True
    air_traffic_control(
        True,
        False,
        1,
        False,
        1000,
        1000,
        6,
        True)
    second_output = capsys.readouterr().out

    assert first_output != 'All conditions met for landing.\n\n'
    assert second_output != 'All conditions met for landing.\n\n'
    assert first_output == 'Debug Info:\nLanding allowed with priority overrides.\n\n'
    assert second_output == 'Debug Info:\nLanding allowed with priority overrides.\n\n'


# Set atomic clause WIND_SPEED to True/False (affecting derived condition SAFE_WEATHER),
# proving that the clause is inactive since the predicate (first elif-statement) doesn't change its evaluation (False)
def test_icc4_windspeed_pred_false(capsys):
    # wind_speed = True, Predicate = False
    air_traffic_control(
        True,
        False,
        1,
        False,
        1,
        1,
        1,
        False)
    first_output = capsys.readouterr().out

    # wind_speed = False, Predicate = False
    air_traffic_control(
        True,
        False,
        1,
        False,
        1000,
        1000,
        1,
        False)
    second_output = capsys.readouterr().out

    assert first_output != 'All conditions met for landing.\n\n'
    assert second_output != 'All conditions met for landing.\n\n'
    assert first_output != 'Debug Info:\nLanding allowed with priority overrides.\n\n'
    assert second_output != 'Debug Info:\nLanding allowed with priority overrides.\n\n'