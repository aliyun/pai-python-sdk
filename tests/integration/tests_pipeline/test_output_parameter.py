import contextlib
import io

from pai.pipeline import Pipeline
from pai.pipeline.component import ContainerComponent
from pai.pipeline.types import PipelineParameter
from tests.integration import BaseIntegTestCase


class TestPipelineOutputParameter(BaseIntegTestCase):
    def test_output_parameters(self):
        python_image = self.get_python_image()

        acc = "0.97"
        output_param_name = "output_1"

        op = ContainerComponent(
            inputs=[PipelineParameter("foo"), PipelineParameter("bar")],
            outputs=[PipelineParameter("output_1")],
            image_uri=python_image,
            env={
                "PYTHONUNBUFFERED": "1",
            },
            command=[
                "bash",
                "-c",
                "echo foo={{inputs.parameters.foo}} bar=={{inputs.parameters.bar}} &&"
                " mkdir -p /pai/outputs/parameters/ "
                "&& echo %s > /pai/outputs/parameters/%s" % (acc, output_param_name),
            ],
        )
        step1 = op.as_step(
            name="step1",
            inputs={
                "foo": "FooExample",
                "bar": "BarExample",
            },
        )

        step2 = op.as_step(
            name="step2",
            inputs={"foo": step1.outputs["output_1"], "bar": "BarExample2"},
        )

        p = Pipeline(
            steps=[step1, step2],
        )
        run_output = io.StringIO()
        with contextlib.redirect_stdout(run_output):
            p.run(job_name="test_output_parameters")
        print(run_output.getvalue())
        self.assertTrue(f"foo={acc}" in run_output.getvalue())
