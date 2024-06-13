#  Copyright 2023 Alibaba, Inc. or its affiliates.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from marshmallow import fields, post_load

from .base import BaseAPIResourceSchema, ListOfKVField


class HyperparameterField(fields.Field):
    """Convert between hyperparameters in Dict to hyperparameters in API Object."""

    def _serialize(self, value, attr, obj, **kwargs):
        res = []
        if not value:
            return res
        for k, v in value.items():
            res.append(
                {
                    "Name": k,
                    "Value": v,
                }
            )
        return res

    def _deserialize(self, value, attr, data, **kwargs):
        res = dict()
        if not value:
            return res
        for item in value:
            res[item["Name"]] = item["Value"]
        return res


class TrainingJobMetricSchema(BaseAPIResourceSchema):
    name = fields.Str()
    timestamp = fields.Str()
    value = fields.Float()


class TrainingJobSchedulerSchema(BaseAPIResourceSchema):
    max_running_time_in_seconds = fields.Int()


class TrainingJobChannelSchema(BaseAPIResourceSchema):
    dataset_id = fields.Str()
    input_uri = fields.Str()
    name = fields.Str()


class TrainingJobStatusTransitionSchema(BaseAPIResourceSchema):
    end_time = fields.Str()
    reason_code = fields.Str()
    reason_message = fields.Str()
    start_time = fields.DateTime()
    status = fields.Str()


class TrainingJobSchema(BaseAPIResourceSchema):
    FieldNameMapping = {
        "GmtCreateTime": "create_time",
        "GmtModifiedTime": "modified_time",
        "TrainingJobDescription": "description",
    }

    algorithm_name = fields.Str()
    algorithm_provider = fields.Str()
    algorithm_version = fields.Str()

    hyperparameters = HyperparameterField()
    input_channels = fields.List(fields.Dict)
    output_channels = fields.List(fields.Dict)
    labels = ListOfKVField()
    description = fields.Str()
    training_job_name = fields.Str()
    scheduler = fields.Dict()
    compute_resource = fields.Dict()
    workspace_id = fields.Str()
    experiment_config = fields.Dict()

    # load only fields
    latest_metrics = fields.List(fields.Dict)
    algorithm_id = fields.Str(load_only=True)
    create_time = fields.DateTime(load_only=True)
    modified_time = fields.DateTime(load_only=True)
    reason_code = fields.Str()
    reason_message = fields.Str()
    status = fields.Str()
    status_transitions = fields.List(fields.Dict)
    training_job_id = fields.Str()
    training_job_url = fields.Str()

    @post_load
    def _make(self, data, **kwargs):
        from ..job._training_job import TrainingJob

        data["instance_count"] = data.get("compute_resource", {}).get("EcsCount")
        data["instance_type"] = data.get("compute_resource", {}).get("EcsType")
        data["max_running_time_in_seconds"] = data.get("scheduler", {}).get(
            "MaxRunningTimeInSeconds"
        )

        return self.make_or_reload(TrainingJob, data)
