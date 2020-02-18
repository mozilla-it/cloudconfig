from behave import then

from dpm.api.config.env_config import Env


class EnvStep:
    @then("values are")
    def values_are_step_impl(self):
        for row in self.table:
            key_ = row["key"]
            value_ = row["value"]
            value = Env.get_config(key_)
            assert value == value_

    @then("values are for {tag}")
    def values_for_tag_step_impl(self, tag):
        for row in self.table:
            key_ = row["key"]
            value_ = row["value"]
            sf = Env.get_config(tag)
            assert sf[key_] == value_
