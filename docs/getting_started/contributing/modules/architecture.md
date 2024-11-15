# Module Architecture

## Overview

Nautobot uses Django apps to break up each data domain within Nautobot. An example of this is **circuits**, **dcim**, **ipam**, **tenancy**, etc. Each application then implements endpoints that fit under the parent application.
An example of an endpoint is **devices** living under the **dcim** app and **ip addresses** living under the **ipam** app. This collection takes the same approach with organizing the module utils for each application and then the endpoints are implemented as the Ansible modules.

Let's take a look at the output of the `tree` command within the `plugins/` directory.

```bash
├── plugins
│   ... omitted
│   ├── module_utils
│   │   ├── circuits.py
│   │   ├── dcim.py
│   │   ├── extras.py
│   │   ├── ipam.py
│   │   ├── secrets.py
│   │   ├── tenancy.py
│   │   ├── utils.py
│   │   └── virtualization.py
│   └── modules
│       ... omitted
│       ├── device.py
│       ... omitted
│       └── vrf.py

128 directories, 357 files
```

As you can see, we have a handful of `module_utils` that correspond to each application in **Nautobot** as well as a `utils` module that provides a common interface for the collection.

Let's start by taking a look at the specifics of what each application module util is accomplishing.

## Module Util Apps (dcim, etc.)

These utility modules contain most of the logic when it comes to interacting with the Nautobot API. There is a lot of overlap between what the modules need to do to interact with the Nautobot API. Therefore, it's wise to try and reduce the boiler plate as much as possible. Within each application module, there is similar code for finding the object within Nautobot, but different options depending on some of the module arguments provided to the user and what fields are available on any given endpoint.

Let's take a look at some of the code within `dcim.py`.

```python
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotModule,
    ENDPOINT_NAME_MAPPING,
)

NB_CABLES = "cables"
NB_CONSOLE_PORTS = "console_ports"
NB_CONSOLE_PORT_TEMPLATES = "console_port_templates"
...
```

The top of the code is importing the `NautobotModule` class, `ENDPOINT_NAME_MAPPING`, and from `utils.py`.

After the imports, we define constants to define the endpoints that are supported as well as these being passed into the initialization of `NautobotModule`. We'll see these within the actual modules themselves when we take a look later.

Now let's take a look at the class definition.

```python
class NautobotDcimModule(NautobotModule):
    def __init__(self, module, endpoint):
        super().__init__(module, endpoint)

    def run(self):
    ...
```

We see that we're subclassing the `NautobotModule` here for `NautobotDcimModule` and then defining our own `__init__` method and then calling the `__init__` method of the parent class (`NautobotModule`). We'll
cover the parent `__init__` class in a below section.

!!! note
    This is not necessarily required, but provides flexibility in the future if we need to perform any operations prior to the parent `__init__`.

After that, we define the `run` method. This method has to be implemented in all module utils and is part of the parent class that raises the `NotImplementedError` exception if not defined on the child class. The `run` method contains all the logic for executing the module and we'll start to dissect it below.

```python
def run(self):
    ...
    # Used to dynamically set key when returning results
    endpoint_name = ENDPOINT_NAME_MAPPING[self.endpoint]

    self.result = {"changed": False}

    application = self._find_app(self.endpoint)
    nb_app = getattr(self.nb, application)
    nb_endpoint = getattr(nb_app, self.endpoint)
    user_query_params = self.module.params.get("query_params")
```

We take the value of the constant that was passed in and assigned to `self.endpoint` and grab the endpoint name that will be used within `self.result`. We'll see it being used shortly.

```python

ENDPOINT_NAME_MAPPING = {
    ...
    "devices": "device",
    ...
}
```

Now we move onto setting `application` and this is where we start to use methods that are available on the `NautobotModule` class. As you can see, we pass in the `self.endpoint` again to this method. Let's take a look at the method.

```python
# Used to map endpoints to applications dynamically
API_APPS_ENDPOINTS = dict(
    circuits=["circuits", "circuit_types", "circuit_terminations", "providers"],
    dcim=[
        ...
        "devices",
        ...
    ]
)
...
class NautobotModule(object):
    ...
    def _find_app(self, endpoint):
        """Dynamically finds application of endpoint passed in using the
        API_APPS_ENDPOINTS for mapping
        :returns nb_app (str): The application the endpoint lives under
        :params endpoint (str): The endpoint requiring resolution to application
        """
        for k, v in API_APPS_ENDPOINTS.items():
            if endpoint in v:
                nb_app = k
        return nb_app
```

This will determine which app the endpoint is part of dynamically and is reused throughout the collection.

We can see that **devices** is part of the **dcim** application. We then use that the set grab the **application** attribute from `pynautobot` and then follow that down to the endpoint level.

`nb_endpoint` is set to `self.nb.dcim.devices` which provides several methods to **get**, **filter**, etc. on the endpoint to figure out if the user defined object already exists within Nautobot.

After that, `user_query_params` is set and that will be either a list of user defined query params or `None`. This topic is covered more in :ref:`Using query_params Module Argument`.

Let's take a look at the next block of code.

```python
def run(self):
    ...
    data = self.data

    # Used for msg output
    if data.get("name"):
        name = data["name"]
    elif data.get("model"):
        name = data["model"]
    elif data.get("master"):
        name = self.module.params["data"]["master"]
    ...
```

We then assign the data instance to `data` that will be used throughout the end of the `run` method. Next wee need to assign the name variable for future use when attempting to obtain the object from Nautobot and this can live under several different fields which is the logic you see above.

Now we move onto some more data manipulation to prepare the payload for Nautobot.

```python
def run(self):
    ...
    # Make color params lowercase
    if data.get("color"):
        data["color"] = data["color"].lower()
```

We make sure that **color** is lowercase if provided.

Here is some more endpoint specific logic that we aren't going to cover, but provides a good example of what some modules may implement when the normal flow does not work for the endpoint.

```python
def run(self):
    ...
    if self.endpoint == "cables":
        cables = [
            cable
            for cable in nb_endpoint.all()
            if cable.termination_a_type == data["termination_a_type"]
            and cable.termination_a_id == data["termination_a_id"]
            and cable.termination_b_type == data["termination_b_type"]
            and cable.termination_b_id == data["termination_b_id"]
        ]
        if len(cables) == 0:
            self.nb_object = None
        elif len(cables) == 1:
            self.nb_object = cables[0]
        else:
            self._handle_errors(msg="More than one result returned for %s" % (name))
    else:
        object_query_params = self._build_query_params(
            endpoint_name, data, user_query_params
        )
        self.nb_object = self._nb_endpoint_get(
            nb_endpoint, object_query_params, name
        )
```

The code after `else:` is what we're interested in and how most modules will determine if the object currently exists within Nautobot or not. The query parameters are dynamically built by providing the `endpoint_name`, `data` passed in by the user, and the `user_query_params` if provided by the user. Once the query parameters are built, we then attempt to fetch the object from Nautobot.

```python
def run(self):
    ...
    if self.state == "present":
        self._ensure_object_exists(nb_endpoint, endpoint_name, name, data)

    elif self.state == "absent":
        self._ensure_object_absent(endpoint_name, name)

    try:
        serialized_object = self.nb_object.serialize()
    except AttributeError:
        serialized_object = self.nb_object

    self.result.update({endpoint_name: serialized_object})

    self.module.exit_json(**self.result)
```

Depending on the state that the user defined, it will use helper functions to complete the intended state of the object. If those don't fail the module, it will then attempt to serialize the object before updating the `self.result` object and then exiting the module.

Most of the app module utils will have the same pattern, but can either have more or less code within it depending on the complexity of the endpoints implemented.

## NautobotModule (__init__)

The `NautobotModule` is the cornerstone of this collection and contains most of the methods required to build a module, but we're going to focus on what happens within the `__init__` method.

```python
class NautobotModule(object):
    """
    Initialize connection to Nautobot, sets AnsibleModule passed in to
    self.module to be used throughout the class
    :params module (obj): Ansible Module object
    :params endpoint (str): Used to tell class which endpoint the logic needs to follow
    :params nb_client (obj): pynautobot.api object passed in (not required)
    """

    def __init__(self, module, endpoint, nb_client=None):
        self.module = module
        self.state = self.module.params["state"]
        self.check_mode = self.module.check_mode
        self.endpoint = endpoint
        query_params = self.module.params.get("query_params")

        if not HAS_PYNAUTOBOT:
            self.module.fail_json(
                msg=missing_required_lib("pynautobot"), exception=PYNAUTOBOT_IMP_ERR
            )
```

The `__init__` method requires an `~ansible.module_utils.basic.AnsibleModule` instance and the endpoint name to be provided with a `~pynautobot.api` client being optional.

We set several instance attributes that are used within other methods throughout the life of the instance. After that, we check to make sure the user has `pynautobot` installed and fail if not.

```python
class NautobotModule(object):
    ...
    # These should not be required after making connection to Nautobot
    url = self.module.params["url"]
    token = self.module.params["token"]
    ssl_verify = self.module.params["validate_certs"]

    # Attempt to initiate connection to Nautobot
    if nb_client is None:
        self.nb = self._connect_api(url, token, ssl_verify)
    else:
        self.nb = nb_client
        self.version = self.nb.version
```

Next we set variables to be used to instantiate the `pynautobot` client if one was not passed in. After instantiated, it will set the Nautobot version that helps determine how specific portions of the code should act depending on the Nautobot version.

```python
class NautobotModule(object):
    ...
    # These methods will normalize the regular data
    cleaned_data = self._remove_arg_spec_default(module.params["data"])
    norm_data = self._normalize_data(cleaned_data)
    choices_data = self._change_choices_id(self.endpoint, norm_data)
    data = self._find_ids(choices_data, query_params)
    self.data = self._convert_identical_keys(data)
```

The next few lines manipulate the data and prepare it for sending to Nautobot.

- Removes argument spec defaults that Ansible sets if an option is not specified (`None`)
- Normalizes data depending on the type of search it will use for the field
- Changes choice for any fields that have choices provided by Nautobot (e.g. status, type, etc.)
- Find IDs of any child objects that need exist in Nautobot before creating parent object (e.g. Device role)
- Converts any fields that are namespaced to prevent conflicts when searching for them (e.g. device_role, ipam_role, rack_group, etc.)

If all those pass, it sets the manipulated data to `self.data` that is used in the module util apps.
