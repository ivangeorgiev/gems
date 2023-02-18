## 1. Preparation

### 1.1. Create Log Analytics Workspace



### 1.2. Connect Azure Activity Log to Log Analytics Workspace



## 2. Generate some activity

### 2.1. Create Service Principal



### 2.2. Grant Service Principal Role



## 3. Query Log Analytics Workspace from Portal



## 4.  Query Log Analytics Workspace from PowerShell

### 4.1. Retrieve Access Token for Service Principal



### 4.2. Query



```powershell
$headers = @{
  "Authorization" = "Bearer $token"
  "Content-Type" = "application/json"
}

$body = @{
  query = "AzureActivity | top 50 by TimeGenerated desc"
  timespan = "PT12H"
}

$result = Invoke-WebRequest -UseBasicParsing -Method POST -Uri "https://westus2.api.loganalytics.io/v1/workspaces/$wsId/query" -Body ($body | ConvertTo-Json) -Headers $headers
$result.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```



