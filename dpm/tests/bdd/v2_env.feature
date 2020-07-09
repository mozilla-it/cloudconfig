Feature: V2 Environment Fascade
    Background: run mocks
    Given mocks
    Given service_name is data-integrations
    And program_name is stripe
    And secrets_name data-integrations-secrets
    And project is mozilla-it
    And dpm_polling_interval is 5
    And secrets_polling_interval is 0

  Scenario: # Enter scenario name here
    # Enter steps here