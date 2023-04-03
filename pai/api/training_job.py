from typing import Any, Dict, List, Optional

from pai.api.base import PaginatedResult, WorkspaceScopedResourceAPI
from pai.libs.alibabacloud_paistudio20220112.models import (
    AlgorithmSpec,
    CreateTrainingJobRequest,
    CreateTrainingJobRequestComputeResource,
    CreateTrainingJobRequestHyperParameters,
    CreateTrainingJobRequestInputChannels,
    CreateTrainingJobRequestLabels,
    CreateTrainingJobRequestOutputChannels,
    CreateTrainingJobRequestScheduler,
    CreateTrainingJobResponseBody,
    GetTrainingJobResponseBody,
    ListTrainingJobLogsRequest,
    ListTrainingJobLogsResponseBody,
    ListTrainingJobsRequest,
)


class TrainingJobAPI(WorkspaceScopedResourceAPI):
    _list_method = "list_training_jobs_with_options"
    _create_method = "create_training_job_with_options"
    _get_method = "get_training_job_with_options"
    _list_logs_method = "list_training_job_logs_with_options"

    # _list_method = "list_training_jobs_with_options"

    def list(
        self,
        page_size: int = 20,
        page_number: int = 1,
        order: str = None,
        sort_by: str = None,
        status: str = None,
        training_job_name: str = None,
    ) -> PaginatedResult:
        request = ListTrainingJobsRequest(
            page_size=page_size,
            page_number=page_number,
            status=status,
            training_job_name=training_job_name,
            order=order,
            sort_by=sort_by,
        )
        res = self._do_request(
            method_=self._list_method,
            request=request,
        )

        return self.make_paginated_result(res)

    def get_api_object_by_resource_id(self, resource_id) -> Dict[str, Any]:
        res: GetTrainingJobResponseBody = self._do_request(
            method_=self._get_method,
            training_job_id=resource_id,
        )
        return res.to_map()

    def get(self, training_job_id) -> Dict[str, Any]:
        return self.get_api_object_by_resource_id(training_job_id)

    def create(
        self,
        instance_type,
        instance_count,
        job_name,
        hyperparameters: Optional[Dict[str, Any]] = None,
        input_channels: Optional[List[Dict[str, Any]]] = None,
        output_channels: Optional[List[Dict[str, Any]]] = None,
        labels: Optional[Dict[str, str]] = None,
        max_running_in_seconds: Optional[int] = None,
        description: Optional[str] = None,
        algorithm_name: Optional[str] = None,
        algorithm_version: Optional[str] = None,
        algorithm_provider: Optional[str] = None,
        algorithm_spec: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a TrainingJob."""
        input_channels = [
            CreateTrainingJobRequestInputChannels().from_map(ch)
            for ch in input_channels
        ]
        output_channels = [
            CreateTrainingJobRequestOutputChannels().from_map(ch)
            for ch in output_channels
        ]

        if algorithm_spec and (
            algorithm_name or algorithm_version or algorithm_provider
        ):
            raise ValueError(
                "Please provide algorithm_spec or a tuple of (algorithm_name, "
                "algorithm_version or algorithm_provider), but not both."
            )

        if algorithm_spec:
            algo_spec = AlgorithmSpec().from_map(algorithm_spec)
        else:
            algo_spec = None

        request = CreateTrainingJobRequest(
            algorithm_name=algorithm_name,
            algorithm_provider=algorithm_provider,
            algorithm_version=algorithm_version,
            compute_resource=CreateTrainingJobRequestComputeResource(
                ecs_count=instance_count,
                ecs_spec=instance_type,
            ),
            hyper_parameters=[
                CreateTrainingJobRequestHyperParameters(
                    name=name,
                    value=str(value),
                )
                for name, value in hyperparameters.items()
            ],
            input_channels=input_channels,
            labels=[
                CreateTrainingJobRequestLabels(key=key, value=value)
                for key, value in labels.items()
            ]
            if labels
            else None,
            output_channels=output_channels,
            scheduler=CreateTrainingJobRequestScheduler(
                max_running_time_in_seconds=max_running_in_seconds
            ),
            training_job_description=description,
            training_job_name=job_name,
            algorithm_spec=algo_spec,
        )

        resp: CreateTrainingJobResponseBody = self._do_request(
            method_=self._create_method, request=request
        )

        return resp.training_job_id

    def list_logs(
        self,
        training_job_id,
        worker_id=None,
        page_size=10,
        page_number=1,
        start_time=None,
        end_time=None,
    ) -> PaginatedResult:
        request = ListTrainingJobLogsRequest(
            page_size=page_size,
            page_number=page_number,
            start_time=start_time,
            end_time=end_time,
            worker_id=worker_id,
        )
        resp: ListTrainingJobLogsResponseBody = self._do_request(
            method_=self._list_logs_method,
            training_job_id=training_job_id,
            request=request,
        )
        return self.make_paginated_result(resp)
