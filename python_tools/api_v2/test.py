# -*- coding: utf-8 -*-

from unittest import TestCase, main, TestSuite, TextTestRunner
from test_task import *


if __name__ == '__main__':
    main()  # run all unittest
    # suite = TestSuite()
    # suite.addTest(UserBaseTest('test_apply_format'))
    # suite.addTest(MyTest('test_method_b'))

    # suite =  unittest.TestLoader().loadTestsFromTestCase(MyTest)
    # TextTestRunner(verbosity=2).run(suite)

