import json
import os
from itertools import islice

from odps import ODPS
from odps.accounts import StsAccount


def get_input_table_meta(channel_name: str):
    """获取输入表元信息"""
    meta_path = os.path.join(
        os.environ.get("PAI_INPUT_{}".format(channel_name.upper())), "meta.json"
    )
    with open(meta_path, "r") as f:
        metadata = json.load(f)

    endpoint = metadata.get("endpoint")
    odps_table_uri = metadata.get("path")
    project_name, _, table_name = odps_table_uri[7:].split("/")
    return endpoint, project_name, table_name


def get_credential():
    """获取ODPS访问凭证"""
    odps_credential_path = os.environ.get("PAI_ODPS_CREDENTIAL")
    with open(odps_credential_path, "r") as f:
        data = json.load(f)
    return data["AccessKeyId"], data["AccessKeySecret"], data["SecurityToken"]


def read_table():
    """读取输入表数据"""
    access_key_id, access_key_secret, security_token = get_credential()
    endpoint, project_name, table_name = get_input_table_meta("train")

    account = StsAccount(
        access_id=access_key_id,
        secret_access_key=access_key_secret,
        sts_token=security_token,
    )
    o = ODPS(account=account, project=project_name, endpoint=endpoint)

    # 读取输入表数据
    for record in islice(o.read_table(table_name), 20):
        print(record)


if __name__ == "__main__":
    read_table()
