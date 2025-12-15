import pytest
from tasks_3_and_4.air_traffic_control import air_traffic_control

# TODO - TASK 4:
# Active clauses. (3 points)
# Identify 3 active clauses i.e. a clause c and a valuation f of the clauses in that
# particular predicate such that if the truth value of c is changed while retaining
# the truth value of the other clauses, then the truth value of the predicate also
# changes.

"""
In the if-statement of the function we've got five clauses separated by AND. Imagine a situation where these clauses
are set in such a way that the if-branch is taken:

* runway_available = True
* safe_speed = True
* emergency = False
* safe_weather = True
* acceptable_traffic = True

Changing the variable 'plane_speed', so that the derived condition 'safe_speed' is changed to False will make the entire
predicate (the if-statement) False. Therefore, making it an active clause. 
Same thing with the 'emergency' variable (atomic), from False to True.
And also the variable 'airport_traffic', setting the derived condition 'acceptable_traffic' from True to False. 

SOLUTION:
We've identified the following three active clauses (note: atomic):
1) plane_speed
2) emergency
3) airport_traffic
"""