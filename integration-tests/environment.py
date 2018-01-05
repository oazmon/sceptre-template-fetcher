import os
import uuid
import yaml

from sceptre_template_fetcher.cli import setup_logging


def before_all(context):
    if context.config.wip:
        setup_logging(True)
    context.uuid = uuid.uuid1().hex
    context.project_code = "sceptre-integration-tests-{0}".format(
        context.uuid
    )

    context.sceptre_dir = os.path.join(
        os.getcwd(), "integration-tests", "sceptre-project"
    )
    update_config(context)


def before_scenario(context, scenario):
    context.error = None
    context.response = None
    context.output = None


def update_config(context):
    config_path = os.path.join(
        context.sceptre_dir, "config", "config.yaml"
    )
    with open(config_path) as config_file:
        env_config = yaml.safe_load(config_file)

    env_config["project_code"] = context.project_code

    with open(config_path, 'w') as config_file:
        yaml.safe_dump(env_config, config_file, default_flow_style=False)


def after_all(context):
    update_config(context)
