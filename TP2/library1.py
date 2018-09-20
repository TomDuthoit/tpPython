""" explore https://docs.python.org/3.6/library/collections.abc.html#collections.abc.Mapping """
# ----------------------------
# Part 1 - import library
# 			and constant value
# -----------------------
# system library
import sys
import logging

try:
    import pytest
except ImportError:
    print("Install pytest with pip command ....")

import numbers
NUMERICS = numbers.Number

from typing import Container, Sized, Reversible, Iterable, Collection, Mapping
from typing import Sequence, List, Tuple , Dict, Set


# constants
STR_FMT = '%(asctime)s - %(levelname)s : %(message)s'
DATE_FMT = '%d/%m/%Y %H:%M:%S'


# ----------------------------
# Part 2 - all functions
#
# -----------------------
def is_container(coll: Container) -> bool :
	""" Not very usefull but readable .... """	
	return isinstance(collection, Container)


NUMERICS = (int, bool, float)
def min_value(logger: logging.Logger, liste: Sequence):
    """ min numeric value """

    num_min = None
    for value in liste:
        if isinstance(value, NUMERICS):
            if num_min is None or value < num_min:
                num_min = value

    return num_min


def min_value2(logger: logging.Logger, liste: Sequence):
    """ min numeric value """
    try:
        return min(filter(lambda x: isinstance(x, NUMERICS), liste))

    except Exception as e:
        log.debug("Here I am with '{}'".format(e))
        return None

try:
    # voir https://docs.pytest.org/en/latest/parametrize.html
    @pytest.mark.parametrize("log", [logging.getLogger()])
    def test_min_values(log: logging.Logger ) ->  None:
        """ call from pytest for instance"""

        lists = ([], ["tt",(1,0)], [-5, "ee", True, -5.0001])
        val_res = zip(lists ,(None, None, -5.0001))
        try:
            for val, res in val_res:
                assert min_value(log, val) == res
                assert min_value2(log, val) == res
        except Exception as e:
            log.info("Tests Error {}".format(e))
        else:
            log.info("Tests Ok ......")
except ImportError:
    print("Install pytest with pip command ....")

def test_min_values2(log: logging.Logger = logging.getLogger()) ->  None:
    """ call from pytest for instance"""

    lists = ([], ["tt",(1,0)], [-5, "ee", True, -5.0001])
    val_res = zip(lists ,(None, None, -5.0001))
    try:
        for val, res in val_res:
            assert min_value(log, val) == res
            assert min_value2(log, val) == res
    except Exception as e:
        log.info("Tests Error {}".format(e))
    else:
        log.info("Tests Ok ......")


# -----------------------
# Part 3 - main entry
# -----------------------
if __name__ == "__main__":
    """version
    """
    logging.basicConfig(level=logging.INFO, format=STR_FMT, datefmt=DATE_FMT)
    log = logging.getLogger()
    log.info(sys.version)
    lists = ([], ["tt",(1,0)], [-5, "ee", True, -5.0001])
	
    if False:
        for li in lists:
            log.info("val min of '%s' is '%s'", str(li), str(min_value(log, li)))
            log.info("val min of '%s' is '%s'", str(li), str(min_value2(log, li)))
    else:
        test_min_values(log)
