from pai.pipeline import Pipeline
from pai.pipeline.component import ContainerComponent
from pai.pipeline.types import PipelineParameter
from tests.integration import BaseIntegTestCase


class TestUnRegisteredComponent(BaseIntegTestCase):
    def test_pipeline(self):
        python_image = self.get_python_image()

        op1 = ContainerComponent(
            inputs=[PipelineParameter("foo"), PipelineParameter("bar")],
            outputs=[],
            image_uri=python_image,
            command=[
                "python",
                "-u",
                "-c",
                "print('{{inputs.parameters.foo}} {{inputs.parameters.bar}}')",
            ],
        )

        def build_pipeline():
            x = PipelineParameter("foo")
            y = PipelineParameter("bar")
            step1 = op1.as_step(
                inputs={
                    "foo": x,
                    "bar": y,
                },
                name="step1",
            )

            step2 = op1.as_step(
                inputs={
                    "foo": "hello",
                    "bar": "world",
                }
            )

            step2.after(step1)

            return Pipeline(steps=[step1, step2])

        p = build_pipeline()
        p.run(
            job_name="test_container_op_pipeline",
            arguments={
                "foo": "Hello",
                "bar": "World",
            },
        )
