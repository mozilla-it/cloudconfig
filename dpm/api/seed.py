import json
import os
import glob

from .env import Env


class DynamicPropertiesSeeder:
    def __init__(self, env: str, dpm_service_name: str, seeds_path: str, dpm_program_name: str):
        self.env = env
        self.dpm_service_name = dpm_service_name
        self.seeds_path = seeds_path
        self.dpm_program_name = dpm_program_name

    def execute(self):
        for filename in glob.glob(f"{self.seeds_path}/{self.env}/*.json"):
            Env.initialize(dpm_service_name=self.dpm_service_name, dpm_program_name=self.dpm_program_name)
            content = json.loads(open(filename).read())
            keys = content.keys()
            for key in keys:
                Env.insert_property(key, content[key])
