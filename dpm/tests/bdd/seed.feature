# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

Feature: Loads properties when invoked
  Scenario: Seed test_service dynamic data into dev
    Given directory with seed data dpm/tests/resource/dynamic-properties-seed
    Given env prod
    Given seeding service test_service
#    When we run seeding