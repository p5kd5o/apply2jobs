import io
import pathlib

import pydantic_yaml

import models.config


def load_config_data(data: str):
    return pydantic_yaml.parse_yaml_raw_as(models.config.Config, data)


def load_config_file(file: pathlib.Path | str | io.IOBase):
    return pydantic_yaml.parse_yaml_file_as(models.config.Config, file)
