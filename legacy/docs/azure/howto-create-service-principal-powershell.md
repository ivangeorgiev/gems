# Create an Azure Service Principal with Azure PowerShell



## Create Service Principal

```powershell
$servicePrincipalName = "app-01-sp"
$servicePrincipal = New-AzADServicePrincipal -DisplayName $servicePrincipalName
```

The returned object we stored in `$servicePrincipal`  has a member `Secret` which contains a `SecureString` with a generated password. To get the secret in plain text, you can use following code:

```powershell
$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($servicePrincipal.Secret)
$plainSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
```

This secret is shown only once. If you loose the secret, you can [reset the service principal credentials](#reset-credentials).

To create service principal with a custom password:

```powershell
Import-Module -Name Az.Resources # Imports the PSADPasswordCredential object
$credentials = New-Object Microsoft.Azure.Commands.ActiveDirectory.PSADPasswordCredential -Property @{StartDate=Get-Date; EndDate=(Get-Date).AddYears(1); Password="<Choose a strong password>"}
$sp = New-AzAdServicePrincipal -DisplayName $servicePrincipalName -PasswordCredential $credentials
```



## Reset credentials

You can create new service principal credential using `New-AzADSpCredential`, but before that the existing credential need to be removed first:

```powershell
Remove-AzADSpCredential -DisplayName $servicePrincipalName -Force
$newCredential = New-AzADSpCredential -ServicePrincipalName "http://$servicePrincipalName"
```

To convert the secret into plain text, you can use the following code:

```powershell
$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($newCredential.Secret)
$plainSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
```

You can limit the validity of the created credential:

```powershell
$newCredential = New-AzADSpCredential -ServicePrincipalName "http://$servicePrincipalName" -StartDate (Get-Date) -EndDate (Get-Date).AddYears(1)
```

The created credential will be valid for 1 year.



## Sign-in with Service Principal

To sign in with service principal, you need the application id and the secret for the service principal.

```powershell
$credentials = Get-Credential
Connect-AzAccount -ServicePrincipal -Credential $credentials -Tenant $tenantId
```



## Get Access Token for Service Principal

For this you need: the tenant id, the application ID, and the secret of the service principal. You also need the tenant id.

```powershell
$body = @{
    client_id = "<application-id>"
    client_secret = "<application-secret>"
    scope = "https://westus2.api.loganalytics.io/.default"
    grant_type = "client_credentials"
}

(Invoke-RestMethod -Method POST -Uri "https://login.microsoftonline.com/$tenantId/oauth2/v2.0/token" -Body $body).access_token

```



