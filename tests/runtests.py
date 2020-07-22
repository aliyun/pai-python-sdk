import fnmatch
import os
import unittest


def main():
    matches = []
    folder = os.path.dirname(__file__)
    print('folder:', folder)
    for root, dirnames, filenames in os.walk(folder):
        for filename in fnmatch.filter(filenames, 'test*.py'):
            full_path = os.path.join(root, filename)
            matches.append(os.path.join("test", full_path[len(folder) + 1:-3]).replace('/', '.'))

    test_suite = unittest.TestSuite()

    for name in matches:
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromName(name))
        print(name)

    unittest.TextTestRunner().run(test_suite)


if __name__ == "__main__":
    main()
