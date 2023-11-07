Get a Microsoft Entra ID (Azure AD) access token for Databricks
==========================================================================

You can use different methods to obtain Microsoft Entra ID (Azure AD) token for Databricks:

- `curl` command
- HTTP requests through some HTTP library or application, e.g. Python's `requests` or Postman
- Azure CLI
- Microsoft Identity Client Library

There is also a choice should you use Service Principal or system assigned or customer assigned Managed Identity.

Service Principal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following snippet illustrates how to obrain a Databrics access token for Azure Service Principal using curl:

.. code-block:: bash

    # Following environment variables should be defined
    # - CLIENT_ID
    # - CLIENT_SECRET
    # - TENANT_ID

    curl -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
        https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token \
        -d 'grant_type=client_credentials' \
        -d 'scope=2ff814a6-3304-4ab8-85cb-cd0e6f879c1d%2F.default' \
        -d "client_id=$CLIENT_ID" \
        -d "client_secret=$CLIENT_SECRET"

produces following response

.. code-block:: json

    {"token_type":"Bearer","expires_in":3599,"ext_expires_in":3599,"access_token":"eyJ0e...fg"}


Managed Identity from App Service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Following snippet illustrates how to obtain a Databricks acess token from Microsoft Entra ID (Azure AD) using curl on App Service.

.. code-block:: bash

    resource="2ff814a6-3304-4ab8-85cb-cd0e6f879c1d%2F.default"
    endpoint=$IDENTITY_ENDPOINT
    header="X-Identity-Header: $IDENTITY_HEADER"
    apiVersion="2019-08-01"

    url="$endpoint?api-version=$apiVersion&resource=$resource"

    curl "$url" -H "$header"

produces following response

.. code-block:: json

    {"access_token":"eyJ0e...WBQ","expires_on":"1699439633","resource":"2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default","token_type":"Bearer","client_id":"00000000-0000-0000-0000-000000000000"}

Links
~~~~~~

- `Authentication for Azure Databricks automation <https://learn.microsoft.com/en-us/azure/databricks/dev-tools/auth>`__
- `Get a Microsoft Entra ID access token with the Microsoft identity platform REST API <https://learn.microsoft.com/en-us/azure/databricks/dev-tools/service-prin-aad-token#--get-a-microsoft-entra-id-access-token-with-the-microsoft-identity-platform-rest-api>`__
- App Service Managed Identity `REST endpoint reference <https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Chttp#rest-endpoint-reference>`__ from *How to use managed identities for App Service and Azure Functions*
