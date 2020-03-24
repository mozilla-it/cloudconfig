# How to install:

For pipenv:

```
[packages]
dynamic-property-management-module = { version = "*", git = "https://github.com/mozilla-it/dynamic-property-management-module.git", ref = "master"}
```

# Must be set:
These environmental variables must be set.
* GOOGLE_APPLICATION_CREDENTIALS
* GCP_PROJECT

# Example Usage:

```
**[Pulling Properties]**

Env.initialize(
               dpm_service_name = <service name/>, 
               dpm_program_name = <program_name/>,
               dpm_polling_interval = <dpm_polling_interval/>,
               secrets_name = <secrets_name/>, 
               secrets_polling_interval = <secrets_polling_interval/>,
               project = <project/>
              )
property_value = Env.get_property(<property_name/>)

**[Pulling Secrets]**

Env.initialize(
               dpm_service_name = <service name/>, 
               dpm_program_name = <program_name/>,
               dpm_polling_interval = <dpm_polling_interval/>,
               secrets_name = <secrets_name/>, 
               secrets_polling_interval = <secrets_polling_interval/>,
               project = <project/>
              )
secret_value = Env.get_secret(<secret_name/>)
```