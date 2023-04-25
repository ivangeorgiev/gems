Get Access Token for Managed Identity from Azure AppService
==========================================================================

Highlights:

- Environment variable `IDENTITY_ENDPOINT` contains the endpoitn url to request token from
- Environment variable `IDENTITY_HEADER` contains the value to pass with `X-IDENTITY-HEADER` headers
- Query params:
  - `resource`, e.g. `https://vault.azure.net`
  - `api-version`, e.g. `2019-08-01`

Here is sample code in Python which acquires access token and uses it to get secret from Key Vault.

.. code-block:: python

   import requests
   from os import environ

   key_vault_name = "<key-vault-name-here>"
   secret_name = "<secret-name-here>"

   token_params = {"resource": "https://vault.azure.net", "api-version": "2019-08-01"}
   token_response = requests.get(
      environ["IDENTITY_ENDPOINT"],
      params=token_params,
      headers={"X-IDENTITY-HEADER": environ["IDENTITY_HEADER"]},
   )
   token = token_response.json()["access_token"]
   token

   secret_params= {"api-version': '7.4'}
   secret_response = requests.get(
      f"https://{key_vault_name}.vault.azure.net:443/secrets/{secret_name}/",
      params=secret_params,
      headers={"Authorization": f"Bearer {token}"},
   )
   secret_response
   secret_response.json()['value']


The same code to get access token for Managed Identity from App Service as `GitHub gist <https://gist.github.com/ivangeorgiev/7d536fafc7dca0c5bf45b35d20039fa0>`__:

The Key Vault `api-varsion` query parameter shown in documentation is `7.4`, but I found that `2016-10-01` also works.

.. raw:: html

   <script src="https://gist.github.com/ivangeorgiev/7d536fafc7dca0c5bf45b35d20039fa0.js?file=get_access_token.py"></script>


See Also
-------------

- `Get Secret<https://learn.microsoft.com/en-us/rest/api/keyvault/secrets/get-secret/get-secret?tabs=HTTP>`__ Key Vault documentation
- `Connect to Azure services in app code <https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Cpowershell>`__
