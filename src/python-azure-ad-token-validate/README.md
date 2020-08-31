# Decode and Validate Azure Active Directory Token in Python

This repository contains the sources for the helper package `aadtoken` and demo script.

For examples and discussion, see the original article [Decode and Validate Azure Active Directory Token in Python](http://www.igeorgiev.eu/python/misc/python-azure-ad-token-decode-validate/).

## Installation

You need Python 3.7+ with `pip` installed.

To run the demo, you need to install the dependencies:

```bash
pip install -r requirements.txt
```



## Running the Demo

To start the demo, you need to define two environment variables:

```bash
export CLIENT_ID=<your-webapp-id-goes-here>
export TENANT_ID=<your-tenant-id-goes-here>
```

Than you can start the demo script:

```bash
python demo.py <your-token-goes-here>
```

