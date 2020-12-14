from __future__ import print_function

import sys
import argparse
from utils import print_hello

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Program arguments parser")
    parser.add_argument("--foo", help="this is parameter foo", type=int)
    parser.add_argument("--bar", help="this is parameter bar", type=str)
    args, _ = parser.parse_known_args()

    print("Param Foo is", args.foo)
    print("Param Bar is", args.bar)

    print("This message is from stderr", file=sys.stderr)

    print_hello()
