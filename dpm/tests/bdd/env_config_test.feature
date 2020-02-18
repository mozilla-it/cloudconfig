Feature: dynamic config for different environments

  Scenario: Pass the DEV profile and initialize dev
    Given this secrets integrations/tests/resources/secrets/props.json
    Then values are
      | key                | value                       |
      | gpg_public_key_url | http://someurl.com          |
    Then values are for salesforce
      | key                | value                       |
      | sftp_host          | http://sfsftp.fake.host.com |
      | sftp_username      | sfusername                  |
      | sftp_password      | sfpassword                  |
