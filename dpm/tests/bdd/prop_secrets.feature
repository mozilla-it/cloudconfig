# Created by jspiropulo at 3/19/20
Feature: Read properties from GCP secrets manager

  Scenario: Get properties dict "destination"
    Given service_name is data-integrations
    And program_name is intacct
    When we read dict property destination
    Then we get dict intacct.open_po_{}

  Scenario: Get properties val "destination"
    Given service_name is data-integrations
    And program_name is intacct
    When we read val property destination
    Then we get val intacct.open_po_{}


  Scenario: test
    Given test this