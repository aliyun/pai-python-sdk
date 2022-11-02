import contextlib
import io

from pai.operator import ContainerOperator
from pai.operator.types import PipelineParameter
from pai.pipeline import Pipeline
from tests.integration import BaseIntegTestCase


class TestConditionPipeline(BaseIntegTestCase):
    def test_condition_output(self):
        acc = "0.97"
        output_param_name = "outputparam"
        op = ContainerOperator(
            inputs=[
                PipelineParameter("foo", default="valueFoo"),
                PipelineParameter("bar", default="valueBar"),
            ],
            outputs=[PipelineParameter(name=output_param_name)],
            image_uri="python:3",
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
        step1 = op.as_step(name="step1")

        step2 = op.as_condition_step(
            name="step2",
            condition=step1.outputs[0] > 0.8,
            inputs={"foo": "GreatThanStep"},
        )
        step3 = op.as_condition_step(
            name="step3",
            condition=step1.outputs[0] <= 0.8,
            inputs={"foo": "LeqThanStep"},
        )

        step4 = op.as_step(name="step4", inputs={"foo": step1.outputs[0]})

        p = Pipeline(steps=[step3, step2, step1, step4])
        run_output = io.StringIO()
        with contextlib.redirect_stdout(run_output):
            p.run(job_name="test_condition_pipeline")
        self.assertTrue("foo=GreatThanStep" in run_output.getvalue())
