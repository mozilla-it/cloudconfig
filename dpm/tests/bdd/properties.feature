# Created by jspiropulo at 2/19/20
Feature: Get properties

#  Background:
#    Given mocks

#  Scenario: Get properties BING_DEFAULT_GROSS_REVENUE_DENOMINATOR by env and service
#    Given the env id is 224
#    And the service id is 568
#    And the program id is 788
#    And secret_name revenue-secrets
#    And project is dp2-stage
#    And I initialize the system
#    When we call BING_DEFAULT_GROSS_REVENUE_DENOMINATOR
#    Then we receive 0.895

#  Scenario: Get properties boxAppSettings by env and service
#    Given the env id is 224
#    And the service id is 568
#    And the program id is 788
#    And secret_name revenue-secrets
#    And project is dp2-stage
#    And I initialize the system
#    When we call boxAppSettings
#    Then dict we receive {"clientID": "mockedclientid", "clientSecret": "mockedclientSecret"}

#  Scenario: Get properties BOX_USER_ID by env and service
#    Given the env id is 224
#    And the service id is 568
#    And the program id is 788
#    And secret_name revenue-secrets
#    And project is dp2-stage
#    And I initialize the system
#    When we call BOX_USER_ID
#    Then we receive 9864028249
#
#  Scenario: Get properties PARTNER_MAPS_YANDEX by env and service
#    Given the env id is 224
#    And the service id is 568
#    And the program id is 788
#    And secret_name revenue-secrets
#    And project is dp2-stage
#    And I initialize the system
#    When we call PARTNER_MAPS_YANDEX
#    Then we receive Yandex
#
#  Scenario: Get properties BOX_USER_ID and PARTNER_MAPS_YANDEX we only initialize once
#    Given the env id is 224
#    And the service id is 568
#    And the program id is 788
#    And secret_name revenue-secrets
#    And project is dp2-stage
#    And I initialize the system
#    When we call PARTNER_MAPS_YANDEX
#    Then we receive Yandex
#    When we call BOX_USER_ID
#    Then we receive 9864028249

#  Scenario: keep running
#    Given the env id is 224
#    And the service id is 568
#    And secret_name revenue-secrets
#    And project is dp2-stage
#    And I initialize the system
#    Given keep running
