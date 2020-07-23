# Created by jspiropulo at 4/23/20
Feature: Seeds properties when initialized

  Background: run mocks
    Given mocks
    Given service_name is test_service
    And program_name is intacct
    And secrets_name data-integrations-secrets
    And project is imposing-union-227917


  Scenario: Seed test_service dynamic data into dev
    Given directory with seed data dpm/tests/resource/dynamic-properties-seed
    Given we initialize the seeder
    When we run seeding