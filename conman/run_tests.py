import os
import sys
import unittest
from glob import glob

source_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(source_dir)
os.chdir(source_dir);

testfiles = os.path.join('conman', 'tests', 'test_*.py')
testmodules = [os.path.splitext(f)[0].replace(os.sep, ".") for f in glob(testfiles)]

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
