# coding: utf-8

from pai.pipeline.base import TemplateSpecBase


class ContainerTemplate(TemplateSpecBase):

    default_identifier = "container_template"

    def __init__(
        self,
        image_uri,
        command,
        image_registry_config=None,
        inputs=None,
        outputs=None,
        env=None,
        identifier=None,
        version=None,
        provider=None,
    ):
        self.image_uri = image_uri
        self.image_registry_config = image_registry_config
        self.command = command
        self.env = env

        super(ContainerTemplate, self).__init__(
            inputs=inputs,
            outputs=outputs,
            identifier=identifier,
            version=version,
            provider=provider,
        )

    def to_dict(self):
        d = super(ContainerTemplate, self).to_dict()
        d["spec"]["execution"] = {
            "image": self.image_uri,
            "command": self.command,
        }

        if self.image_registry_config:
            d["spec"]["execution"]["imageRegistryConfig"] = self.image_registry_config

        if self.env:
            d["spec"]["execution"]["env"] = self.env
        return d
