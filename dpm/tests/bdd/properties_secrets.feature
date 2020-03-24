# Created by jspiropulo at 3/19/20
Feature: Read properties from GCP secrets manager

  Background: run mocks
    Given mocks

  Scenario: Get property "value"
    Given this exists value = 1
    Given service_name is data-integrations
    And program_name is intacct
    And secrets_name data-integrations-secrets
    And project is imposing-union-227917
    And dpm_polling_interval is 5
    And secrets_polling_interval is 0
    When we read property value
    Then we get val 1

  Scenario: Get secret "batman"
    Given this exists batman = 2
    Given service_name is data-integrations
    And program_name is intacct
    And secrets_name data-integrations-secrets
    And project is imposing-union-227917
    And dpm_polling_interval is 5
    And secrets_polling_interval is 0
    When we read secret batman
    Then we get val 2


#  Scenario: test
#    Given test this poll properties 1 and poll secrets 1