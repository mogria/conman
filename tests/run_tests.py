import os
import unittest
from glob import glob

test_dir = os.path.dirname(os.path.realpath(__file__)) # tests/ directory
os.chdir(test_dir);
testmodules = ["tests." + os.path.splitext(f)[0] for f in glob("test_*.py")]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner(buffer=True).run(suite)
