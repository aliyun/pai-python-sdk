import pai_running
from pai_running.context import Context


def main():

    context = Context()
    print(pai_running.__version__)
    print("input_artifact raw_value")
    print(context.input_artifacts[0].raw_value)
    print(context.input_artifacts["input1"].raw_value)

    context.output_artifacts["output1"].write_output("value")


if __name__ == "__main__":
    main()
