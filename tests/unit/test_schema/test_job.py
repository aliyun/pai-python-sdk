import json

from pai.schema import JobSchema
from tests.unit import BaseUnitTestCase

JOB_DATA = """{
    "GmtFinishTime": "2022-06-23T06:35:10Z",
    "JobMaxRunningTimeMinutes": 0,
    "ReasonMessage": "TFJob dlc1sm1ipuyurlsw successfully completed.",
    "Pods": [
        {
            "Status": "Succeeded",
            "GmtFinishTime": "2022-06-23T06:35:10Z",
            "HistoryPods": [],
            "GmtStartTime": "2022-06-23T06:35:07Z",
            "Type": "worker",
            "NodeName": "cn-hangzhou.10.224.36.33",
            "PodUid": "",
            "Ip": "10.224.36.33",
            "StatusDetail": {
                "Message": "",
                "ExitCode": "",
                "Reason": ""
            },
            "Duration": 135,
            "PodId": "dlc1sm1ipuyurlsw-worker-0",
            "GmtCreateTime": "2022-06-23T06:32:55Z"
        }
    ],
    "WorkspaceId": "28293",
    "JobSpecs": [
        {
            "PodCount": 1,
            "UseSpotInstance": false,
            "Type": "Worker",
            "EcsSpec": "ecs.c6.large",
            "Image": "registry.cn-hangzhou.aliyuncs.com/pai-dlc/xgboost-training:1.6.0-cpu-py36-ubuntu18.04"
        }
    ],
    "DataSources": [
        {
            "MountPath": "",
            "DataSourceId": "d-3tbyu0t6inlxdagnr0"
        },
        {
            "MountPath": "",
            "DataSourceId": "d-7ftcd1sp60ofneejrm"
        },
        {
            "MountPath": "",
            "DataSourceId": "d-dbkbq78v1ifxyxyc7d"
        }
    ],
    "GmtSubmittedTime": "2022-06-23T06:32:55Z",
    "DisplayName": "custom-job-None",
    "WorkspaceName": "lq_test_project",
    "JobId": "dlc1sm1ipuyurlsw",
    "Status": "Succeeded",
    "GmtRunningTime": "2022-06-23T06:35:08Z",
    "RequestId": "40D701F9-9A7A-5DE5-B78F-3DB640C39A98",
    "ClusterId": "",
    "Priority": 0,
    "Duration": 309,
    "CodeSource": {
        "MountPath": "",
        "CodeSourceId": ""
    },
    "ReasonCode": "JobSucceeded",
    "UserCommand": "mkdir -p /ml/code && cd /ml/code  && tar -xvzf /ml/mount/code/source.tar.gz -C /ml/code  && python xgb_train.py --n_estimators 1000 --objective multi:softmax --max_depth 5 --train_data /ml/input/data/train_data/train.csv",
    "JobType": "TFJob",
    "ResourceId": "",
    "UserId": "1157703270994901",
    "ThirdpartyLibDir": "",
    "GmtSuccessedTime": "2022-06-23T06:35:10Z",
    "GmtCreateTime": "2022-06-23T06:30:01Z"
}"""


class TestJobSchema(BaseUnitTestCase):
    def test_job_schema(self):
        schema = JobSchema()
        data = json.loads(JOB_DATA)
        job = schema.load(json.loads(JOB_DATA))
        self.assertEqual(job.id, data["JobId"])
        self.assertEqual(job.status, data["Status"])
        self.assertEqual(job.display_name, data["DisplayName"])
        result = schema.dump(job)
        output_keys = ["JobType", "WorkspaceId", "JobSpecs"]

        for key in output_keys:
            self.assertEqual(data[key], result[key])
