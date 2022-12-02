from pai.pipeline.types.artifact import DataType


class ArchivedArtifact(object):
    """Archived artifact instance, hold the metadata, value and source of the artifact."""

    def __init__(self, metadata, value, name, producer_id, id):
        """ArchivedArtifact class constructor.

        Args:
            metadata (:class:`~.pai.pipeline.artifact.ArtifactMetadata`): Artifact metadata info.
            value (:class:`~.pai.pipeline.artifact.ArtifactValue`): Artifact value.
            name (str): name of artifact, actually, it is the name of artifact in manifest of
                source pipeline.
            producer_id (str): Producer of the artifact, identified by step name of pipeline.
            artifact_id (str): Unique artifact identifier in pipeline service.
        """
        self.name = name
        self.metadata = metadata
        self.value = value
        self.producer_id = producer_id
        self.id = id

    def __repr__(self):
        return "%s:Id=%s,Name=%s" % (
            type(self).__name__,
            self.id,
            self.name,
        )

    @classmethod
    def deserialize(cls, output):
        """Build new ArtifactInfo instance from Run output json.

        Output Example:

        {
          'Info': {
            'value': '{"location": {"table": "pai_temp_77c08aeb2e514c9d8649feba4a88ee77"}}',
            'metadata': {
              'path': '/tmp/outputs/artifacts/outputArtifact/data',
              'type': {
                'DataSet': {
                  'locationType': 'MaxComputeTable'
                }
              }
            }
          },
          'Name': 'outputArtifact',
          'Producer': 'flow-ec67rsug8kyly4049z',
          'CreateTime': 1595214018000,
          'Type': 'DataSet',
          'Id': 'artifact-e0xdqhsfhqctxkpyli'
        }

        Args:
            output (dict): Run output return by pipeline service.
        Returns:
            ArchivedArtifact: ArtifactInfo instance.
        """
        name = output["Name"]
        metadata = output["Info"]["metadata"]
        value = output["Info"]["value"]
        producer_id = output["Producer"]
        artifact_id = output["Id"]
        return ArchivedArtifact(
            metadata=metadata,
            value=value,
            name=name,
            producer_id=producer_id,
            id=artifact_id,
        )

    @property
    def is_model(self):
        return self.metadata.data_type == DataType.Model
