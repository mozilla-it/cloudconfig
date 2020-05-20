from dpm.api.env import Env


def before_scenario(context: object, scenario: object) -> object:
    Env._instance = None
    Env.InnerEnv._dpm_instance = None
    Env.InnerEnv._secret_instance = None
