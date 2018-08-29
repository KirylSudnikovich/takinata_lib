import unittest


def run_tests():
    testmodules = [
        'lib.tests.project',
        'lib.tests.category',
        'lib.tests.task',
        'lib.tests.user'
    ]

    suite = unittest.TestSuite()

    for t in testmodules:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName(t))

    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    run_tests()
