import csv
import os
import json
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Dict


class Env:
    local_config: dict = {}

    config = "config"

    @staticmethod
    def get_box_key():
        return os.environ["BOX_KEY"]

    @staticmethod
    def __get_common():
        env = Environment(
            loader=PackageLoader("integrations", Env.config),
            autoescape=select_autoescape(["json"]),
        )
        env.filters["jsonify"] = json.dumps
        commmon_path = "env_template.json"
        common_template = env.get_template(commmon_path)

        with open(os.environ["SECRETS"], "r") as cf:
            render = common_template.render(page=json.load(cf))
            return json.loads(render)

    @staticmethod
    def get_config(key: str):
        if not Env.local_config:
            Env.local_config = Env.__get_common()

        return Env.local_config[key]

    @staticmethod
    def update_config(key: str, value: str):
        Env.local_config.update({key: value})

    @staticmethod
    def get_anaplan_key():
        priv_key_file = os.environ.get("ANAPLAN2_PRIVATE_PEM")
        with open(priv_key_file, "r") as my_cert_file:
            my_cert_text = my_cert_file.read()
        return my_cert_text

    @staticmethod
    def get_anaplan_cert():
        pub_cert_key = os.environ.get("ANAPLAN2_PUBLIC_PEM")
        with open(pub_cert_key, "r") as my_cert_file:
            my_cert_text = my_cert_file.read()
        return my_cert_text

    @staticmethod
    def get_workday_basic_auth():
        # Dict with keys: ["USERNAME", "PASSWORD"
        workday_creds = os.environ.get("WORKDAY_CREDS")
        with open(workday_creds, "r") as cred_file:
            cred_file_read = cred_file.read()
            workday_json = json.loads(cred_file_read)
        return workday_json

    @staticmethod
    def get_finance_mapping_workday_to_anaplan():
        mapping = os.environ.get("MAPPING")
        reader = csv.DictReader(open(mapping))
        column_mappings: Dict = {}
        for line in reader:
            column_mappings = line
        return column_mappings
