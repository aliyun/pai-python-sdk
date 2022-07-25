from pai.core.session import (
    Session,
    setup_default_session,
)
from tests.unit import BaseUnitTestCase


class TestSession(BaseUnitTestCase):
    def test_context_session(self):
        sess = setup_default_session(
            access_key_id="akId", access_key_secret="akSecret", region_id="cn-hanghai"
        )
        assert sess is Session.current()

        default_sess = setup_default_session(
            access_key_id="defaultAkId",
            access_key_secret="defaultAkSecret",
            region_id="cn-shanghai",
        )
        assert default_sess is Session.current()

        with Session(
            access_key_id="akIdExample",
            access_key_secret="akSecretExample",
            region_id="cn-hangzhou",
        ) as s:
            assert s is Session.current()
            with Session(
                access_key_id="foo", access_key_secret="bar", region_id="cn-shanghai"
            ) as inner:
                assert inner is Session.current()

            assert s is Session.current()

        assert default_sess is Session.current()
