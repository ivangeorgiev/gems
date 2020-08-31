---
tags: python, azure, azure active directory, jwt
creatrd: 2020-08-31
---

## Decode and Validate JWT Token from Azure Active Directory in Python

## Problem

You need to decode and validate JWT Token issued by Azure Active Directory.

Example scenario is where you have a Web Application which is using BFF (Backend for Frontend) API. Users are authenticated by the front-end application using Azure AD and the token is forwarded to the BFF API. The BFF API needs to validate the received token since the client is outside of its trust boundary.

## Solution

Use *pyjwt* and `cryptography` packages.

I have created a small package `aadtoken` to help with getting the Azure Active Directory public key and decode the token using, using `pyjwt` and `cryptography`. Further to decode the token use the `jwt.decode` function from the `pyjwat` package.

All the sources are available in [GitHub](https://github.com/ivangeorgiev/gems/tree/master/src/python-azure-ad-token-validate). Here I am providing only an example how to use the `aadtoken` helper package along with `jwt.decode`:

```python
import os
import sys
import jwt
from aadtoken import get_public_key

client_id = os.environ.get('CLIENT_ID', '<your-webapp-id-goes-here>')
tenant_id = os.environ.get('TENANT_ID', '<your-tenant-id-goes-here>')
if len(sys.argv) > 1:
    token = sys.argv[1]
else:
    token = os.environ.get('TOKEN', "<your-token-goes-here>")

issuer = 'https://sts.windows.net/{tenant_id}/'.format(tenant_id=tenant_id)


public_key = get_public_key(token)
decoded = jwt.decode(token,
                     public_key,
                     verify=True,
                     algorithms=['RS256'],
                     audience=[client_id],
                     issuer=issuer)
print(decoded)

```

You need to replace the placeholders with actual values.

Alternatively you could use environment variables to define the client id, the tenant id and the token.

The token id can also be passed as a command line argument:

```bash
python demo.py <your-token-goes-here>
```



## Discussion

This solution is based on the [Validating JSON web tokens (JWTs) from Azure AD, in Python](https://robertoprevato.github.io/Validating-JWT-Bearer-tokens-from-Azure-AD-in-Python/) publication by Roberto Prevato.

The solution defines a package which is responsible for discovering the Azure AD endpoints and getting the Azure Active Directory's public key.

Requests to Azure Active Directory discovery and keys endpoints are cached.

The most important function exported by the package is `get_public_key(<token>, [<tenant_id>])`.  For given token and tenant ID the function returns the Azure Active Directory public key. The key is used by the `jwt.decode` function from the *pyjwat* package to validate and decode the token.

