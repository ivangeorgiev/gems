

## Query Log Analytics Workspace from Azure PowerShell with Service Principle

### What you need?

* You need to know:
  * Tenant ID
  * For the Application Registration (Service Principal):
    * Application ID
    * Application Secret
  * For the Log Analytics Workspace
    * Workspace Name
    * Resource Group Name
* Service Principle needs at least Reader role to Log Analytics Workspace

### Define Configuration as Constants

```powershell
```



### Connect Service Principle Account

First you need to sign-in the service principal.

```powershell
New-Variable -Name applicationId -Value "<application-id>" -Option Constant
New-Variable -Name applicationSecret -Value "<application-secret>" -Option Constant
New-Variable -Name tenantId -Value "<tenant-id>" -Option Constant
New-Variable -Name WorkspaceName -Value "<workspace-name>" -Option Constant
New-Variable -Name WorkspaceResourceGroupName -Value "<resource-group-name>" -Option Constant
```



```powershell
$password = (ConvertTo-SecureString -String $applicationSecret -AsPlainText -Force)
$credential = New-Object System.Management.Automation.PSCredential($applicationId, $password)

Connect-AzAccount -Credential $credential -TenantId $tenantId -ServicePrincipal
```



### Query Log Analytics Workspace

```powershell
$Workspace = Get-AzOperationalInsightsWorkspace -ResourceGroupName $WorkspaceResourceGroupName -Name $WorkspaceName

$kqlQuery = 'ADFPipelineRun | order by TimeGenerated desc'

$QueryResults = Invoke-AzOperationalInsightsQuery -Workspace $Workspace -Query $kqlQuery
```

Inspect the results:

```powershell
$QueryResults.Results | Select-Object -Property PipelineName, Status
```

Produces similar output:

```
PipelineName              Status    
------------              ------    
pl_orchestration_recipe_1 Succeeded 
pl_orchestration_recipe_1 Succeeded 
pl_orchestration_recipe_1 Succeeded 
pl_orchestration_recipe_1 InProgress
pl_orchestration_recipe_1 Queued    
...
```









* https://zimmergren.net/log-custom-application-security-events-log-analytics-ingested-in-azure-sentinel/
* 