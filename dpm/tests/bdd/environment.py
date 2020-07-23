from dpm.tests.bdd.steps.properties_secrets_step import DocumentMock


def before_scenario(context, scenario):
    DocumentMock.properties = None