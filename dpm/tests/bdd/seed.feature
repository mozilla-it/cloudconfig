# Created by jspiropulo at 4/23/20
Feature: Loads properties when invoked

  Scenario: Seed test_service dynamic data into dev
    Given directory with seed data dpm/tests/resource/dynamic-properties-seed
    Given env prod
    Given seeding service test_service
#    When we run seeding