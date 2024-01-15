import math
def fact(n):
    if n < 2:
        return 1
    if n > 10:
        return math.inf
    else:
        return n * fact(n-1)   


from hypothesis import settings, Verbosity
from hypothesis import given, strategies as st
@settings(verbosity=Verbosity.verbose)
@given(n=st.integers(min_value=1, max_value=15))
def test_fact_spec(n):
#    print("The test number is: {}".format(n))
    assert fact(n) == n * fact(n - 1)
