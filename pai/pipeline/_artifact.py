from pai.pipeline.pipeline_variable import PipelineVariable


class PipelineArtifact(PipelineVariable):
    variable_category = "artifacts"

    def __init__(self, name, typ, desc=None, kind='input', value=None, from_=None, required=None, parent=None):
        super(PipelineArtifact, self).__init__(name=name, typ=typ, desc=desc, kind=kind, value=value, from_=from_,
                                               required=required, parent=parent)

    # todo: value format of artifact is not set down.
    def validate_value(self, val):
        return True


def _create_artifact(name, typ, kind, desc=None, required=None, value=None, from_=None, parent=None):
    return PipelineArtifact(name=name, typ=typ, kind=kind, desc=desc, required=required, value=value,
                            parent=parent, from_=from_)
