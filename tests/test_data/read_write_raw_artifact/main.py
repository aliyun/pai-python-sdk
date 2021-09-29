import os


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        subindent = " " * 4 * (level + 1)
        for f in files:
            print("{}{}".format(subindent, f))


def main():
    base_dir = "/work/"
    # print("list files")
    # list_files("/work")

    input_path = os.path.join(base_dir, "inputs", "artifacts", "input1", "value")

    print(input_path)
    input_value = open(input_path, "r").read()
    print("input value is")
    print(input_value)

    output_value = input_value + ":" + "End"
    output_path = os.path.join(base_dir, "outputs", "artifacts", "output1", "value")

    # exist_ok only work in Python3
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w+") as f:
        f.write(output_value)


if __name__ == "__main__":

    main()
