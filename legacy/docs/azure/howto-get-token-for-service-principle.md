[TOC]

## Problem

When you are creating a background application before your application can consume services, it needs to authenticate. 

To authenticate, applications use service principals and OAuth token provided by Azure Active Directory.

## What You Need

Here is what you need:

| Entity         | Description                                                  |
| -------------- | ------------------------------------------------------------ |
| Application Id | Service principal application ID                             |
| Client Secret  | Service principal secret                                     |
| Tenant Id      | Azure Active Directory ID where the service principal is registered |
| Resource Url   | The URL of the resource for which the token is being requested |

## Find Tenant ID

You could find the tenant ID from Azure Portal.

You could also find the Tenant ID using Azure PowerShell:

```powershell
$tenantId = (Get-AzContext).Tenant.Id
```



## Find Application Id and Application Secret

You can take the Application Id from the Overview of the service principal in Azure Active Directory blade in Azure Portal. 

You can also create an application secret.



## Request Access Token using REST API

Here is an example how to get access token for the Log Analytics API using PowerShell and HTTP request:

```powershell
$body = @{
    client_id = "<application-id>"
    client_secret = "<application-secret>"
    scope = "https://westus2.api.loganalytics.io/.default"
    grant_type = "client_credentials"
}

$response = (Invoke-RestMethod -Method POST -Uri "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token" -Body $body)
$token = $response.access_token
```





