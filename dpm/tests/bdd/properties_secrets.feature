# Created by jspiropulo at 3/19/20
Feature: Read properties from GCP secrets manager

  Background: run mocks
    Given mocks
    Given service_name is data-integrations
    And program_name is intacct
    And secrets_name data-integrations-secrets
    And project is imposing-union-227917
    And dpm_polling_interval is 5
    And secrets_polling_interval is 0

  Scenario: Get property "endpoint"
    Given this exists endpoint = {"value": "https://api.intacct.com"}
    When we read property endpoint
    Then we get val https://api.intacct.com

  Scenario: Get property "sender_id"
    Given this exists sender_id = {"value": "MOZ Corp2", "description": "The sender id we are using to communicate with Intacct"}
    When we read property sender_id
    Then we get val MOZ Corp2

  Scenario: Get property "user_agent"
    Given this exists user_agent = pyintacct-0.0.8
    When we read property user_agent
    Then we get val pyintacct-0.0.8

#  Scenario: Update property "user_agent"
#    Given this exists user_agent = pyintacct-0.0.8
#    When I update user_agent = pyintacct
#    When we read property user_agent
#    Then we get val pyintacct

  Scenario: Get secret "intacct_secret"
    Given this exists intacct_secret = GGJHGJHIUY
    When we read secret intacct_secret
    Then we get val GGJHGJHIUY

  Scenario: Get secret "json_secret"
    Given this exists json_secret = {"value": "GGJHGJHIUY"}
    When we read secret json_secret
    Then we get val {"value": "GGJHGJHIUY"}


#  Scenario: test
#    Given I start
#    Given I update USD with 1
#    Given test this
