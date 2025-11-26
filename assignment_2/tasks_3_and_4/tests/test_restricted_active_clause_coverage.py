import pytest
from tasks_3_and_4.air_traffic_control import air_traffic_control

# TODO - TASK 4:
# Test suite for Restricted Active Clause Coverage (RACC). (3 points)
# Create a test suite that achieves RACC restricted to the 3 active clauses you
# identified. That is, for each identified clause c, there is a test t1 which sets c to
# true and a test t2 which sets it to false, and further the value of the predicate is
# different between the two tests.