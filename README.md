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
**[Initialization should only happen once. The polling 
values will determine if additional polls will be performed.]**
Env.initialize(
               dpm_service_name = <service name/>, 
               dpm_program_name = <program_name/>,
               dpm_polling_interval = <dpm_polling_interval/>,
               secrets_name = <secrets_name/>, 
               secrets_polling_interval = <secrets_polling_interval/>,
               project = <project/>
              )

**[Pulling Properties]**
property_value = Env.get_property(<property_name/>)

**[Pulling Secrets]**
secret_value = Env.get_secret(<secret_name/>)
```

```
>>> from dpm.api import Env
>>> Env.initialize("LOOK AT THE EXAMPLE ABOVE")
>>> Env.get_property("property_key")
'property_value'
>>> Env.get_secret("secret_key")
'secret_value'
```

# Managing Properties and Secrets:
In order to create/delete/update/read properties or secrets go here:
https://github.com/mozilla-it/cloudsecrets

You'll have to follow the instructions on how to install and use the CLI tool.