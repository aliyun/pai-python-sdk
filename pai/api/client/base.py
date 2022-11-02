from __future__ import absolute_import

import json
import logging
import os
import time
from functools import wraps
from typing import Optional

from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util import models as util_models
from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from Tea.exceptions import TeaException

DefaultPageSize = 50

DefaultGeneratorApiCallInterval = 0.5

logger = logging.getLogger(__name__)


def paginate_service_call(f):
    @wraps(f)
    def _(self, *args, **kwargs):
        request = f(self, *args, **kwargs)
        page_num = kwargs.pop("page_num", 1)
        page_size = kwargs.pop("page_size", DefaultPageSize)
        return self._call_paginate_service_with_exception(request, page_num, page_size)

    return _


class BaseClient(object):
    _ENV_SERVICE_ENDPOINT_KEY = None

    def __init__(self, acs_client, endpoint=None):
        self._acs_client = acs_client

        if endpoint:
            self._endpoint = endpoint
        elif (
            self._ENV_SERVICE_ENDPOINT_KEY is not None
            and self._ENV_SERVICE_ENDPOINT_KEY in os.environ
        ):
            self._endpoint = os.environ[self._ENV_SERVICE_ENDPOINT_KEY]
        else:
            self._endpoint = None

    def _call_service_with_exception(self, request):
        from pai.exception import ServiceCallException

        logger.debug(
            "Request:%s, path_params:%s, uri_params:%s, query_params:%s, body_params:%s",
            type(request),
            request.get_path_params(),
            request.get_uri_params(),
            request.get_query_params(),
            request.get_body_params(),
        )
        try:
            raw_resp = self._acs_client.do_action_with_exception(request)
            logger.debug("Response:%s", raw_resp)
            resp = self._response_to_dict(raw_resp)
        except (ClientException, ServerException) as e:
            raise ServiceCallException(e.__str__())
        return resp

    def _call_paginate_service_with_exception(
        self, request, page_num=1, page_size=DefaultPageSize
    ):
        is_end = False
        while not is_end:
            request.set_PageNumber(page_num)
            request.set_PageSize(page_size)
            logger.debug(
                "Paginate Request:%s:page_size:%s, page_number:%s",
                type(self).__name__,
                page_size,
                page_num,
            )
            resp = self._call_service_with_exception(request)
            total_count = resp["TotalCount"]
            for resource in resp["Data"]:
                yield resource
            if page_num * page_size >= total_count:
                is_end = True
            page_num += 1

    @property
    def region_id(self):
        return self._acs_client.get_region_id()

    def _get_product(self):
        pass

    @classmethod
    def _response_to_dict(cls, response):
        if not response:
            return dict()

        return json.loads(response, encoding="utf-8")

    def _construct_request(self, request_cls):
        req = request_cls()
        req.set_accept_format("json")

        if req.get_method() in ["POST", "PUT"]:
            req.set_content_type("application/json")

        if self._get_endpoint():
            req.set_endpoint(self._get_endpoint())

        if self._get_product():
            req.set_product(self._get_product())

        req.set_protocol_type("https")
        return req


class BaseTeaClient(object):
    _ENV_SERVICE_ENDPOINT_KEY = None
    _PRODUCT_NAME = None

    _inner_region_id = "center"

    def __init__(
        self,
        access_key_id: str,
        access_key_secret: str,
        region_id: Optional[str] = None,
        endpoint: None = None,
        **kwargs,
    ) -> None:
        if endpoint is None:
            endpoint = type(self)._get_endpoint(region_id=region_id)

        self.region_id = region_id
        self.endpoint = endpoint
        self._access_key_id = access_key_id
        self._access_key_secret = access_key_secret

    def build_client_config(self, **kwargs) -> Config:
        return Config(
            access_key_id=self._access_key_id,
            access_key_secret=self._access_key_secret,
            region_id=self.region_id,
            endpoint=self.endpoint,
            signature_algorithm="v2",
            user_agent=self._generate_user_agent(),
            **kwargs,
        )

    @classmethod
    def _generate_user_agent(cls) -> str:
        import pai

        return "AlibabaPAISDK/{}".format(pai.__version__)

    @classmethod
    def _get_runtime(cls):
        return util_models.RuntimeOptions()

    @classmethod
    def _get_headers(cls):
        return {}

    @classmethod
    def _construct_endpoint_by_region(cls, region_id: str) -> str:
        """Construct Product endpoint with given region_id"""
        if region_id == cls._inner_region_id:
            return "{}inner-share.aliyuncs.com".format(cls._PRODUCT_NAME.lower())
        return "{}.{}.aliyuncs.com".format(cls._PRODUCT_NAME.lower(), region_id)

    @classmethod
    def _get_endpoint(cls, region_id: str) -> str:
        """Get service endpoint."""
        if cls._ENV_SERVICE_ENDPOINT_KEY and os.environ.get(
            cls._ENV_SERVICE_ENDPOINT_KEY
        ):
            return os.environ.get(cls._ENV_SERVICE_ENDPOINT_KEY)
        if not region_id or not cls._PRODUCT_NAME:
            raise ValueError(
                "Please provide region_id and product_name to build service endpoint: region_id=%s, product_name=%s"
                % (region_id, cls._PRODUCT_NAME)
            )
        return cls._construct_endpoint_by_region(region_id)

    def _call_service_with_exception(self, client_method, **kwargs):
        from pai.exception import ServiceCallException

        try:
            resp = client_method(**kwargs)
        except TeaException as e:
            raise ServiceCallException(e.__str__())
        return resp.body

    @staticmethod
    def to_generator(method):
        def f(**kwargs):
            page_size = kwargs.pop("page_size", None) or 100
            page_number = kwargs.pop("page_number", None) or 1

            while True:
                entities, _ = method(
                    page_size=page_size, page_number=page_number, **kwargs
                )
                if not entities:
                    return
                for entity in entities:
                    yield entity
                page_number += 1
                time.sleep(DefaultGeneratorApiCallInterval)

        return f
