import glob
import json
import os

import dpm.api.env as config


class DynamicPropertiesSeeder:
    def __init__(self, dpm_service_name: str, seeds_path: str, dpm_program_name: str):
        self.seeds_path = seeds_path
        config.Env.initialize(dpm_service_name=dpm_service_name, dpm_program_name=dpm_program_name)

    def execute(self):
        project_name = os.environ["PROJECT"]
        env = "dev"
        if "stage" in project_name:
            env = "stage"
        elif "prod" in project_name:
            env = "prod"

        for filename in glob.glob(f"{self.seeds_path}/{env}/*.json"):
            content = json.loads(open(filename).read())
            keys = content.keys()
            for key in keys:
                config.Env.insert_property(key, content[key])
