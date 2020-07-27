from dynaconf import Dynaconf
from os import environ

environ["MERGE_ENABLED_FOR_DYNACONF"] = "true"

settings = Dynaconf(
    envvar_prefix="VCR",
    environments=False,
    settings_files=[
        "defaults.toml",  # Defaults
        ".secrets.toml",
        "config.toml",
        "/config/config.toml",  # Specific to docker
        "/config/.secrets.toml",  # Specific to docker, for secrets storage
    ],
)
