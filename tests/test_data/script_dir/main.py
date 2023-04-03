from __future__ import print_function

import argparse
import os
import sys
import time

from utils import print_hello

if __name__ == "__main__":

    for key, value in os.environ.items():
        print("Environment: Key={} Value={}".format(key, value))

    parser = argparse.ArgumentParser(description="Program arguments parser")
    parser.add_argument("--foo", help="this is parameter foo", type=str)
    parser.add_argument("--bar", help="this is parameter bar", type=str)
    parser.add_argument("--output_path", help="Job Output Path", type=str)
    args, _ = parser.parse_known_args()

    print("Param Foo is", args.foo)
    print("Param Bar is", args.bar)

    print("This message is from stderr", file=sys.stderr)

    print_hello()

    if args.output_path:
        with open(os.path.join(args.output_path, "output.txt"), "w") as f:
            f.write("ExampleOutput")

    time.sleep(10)
