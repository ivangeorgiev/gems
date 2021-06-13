function Set-DatabricksClusterEnvironmentVariables {
    [cmdletbinding()]
    param(
        [string]$ClusterId,
        [hashtable]$Vars
    )

    Write-Verbose "Get Databricks cluster info"
    $ClusterInfo = (databricks clusters get --cluster-id $ClusterId | ConvertFrom-Json)
    foreach ($VarName in $Vars.Keys) {
        Write-Verbose "Set variable $VarName"
        Add-Member -InputObject $ClusterInfo.spark_env_vars -Name $VarName -MemberType NoteProperty -Value $Vars[$VarName] -Force
    }

    $JsonFilePath = New-TemporaryFile

    $ClusterInfoJson = ($ClusterInfo | ConvertTo-Json -Depth 10)
    $Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False
    [System.IO.File]::WriteAllLines($JsonFilePath, $ClusterInfoJson, $Utf8NoBomEncoding)

    Write-Verbose "Update Databricks cluster"
    databricks clusters edit --json-file $JsonFilePath
    Remove-Item $JsonFilePath
}

$Vars = @{
    DB_CONNECTION_STRING = 'MSSQL;hostname=nowhere;username=ghost;password=purple'
    ENVIRONMENT_NAME = 'Development'
    ENVIRONMENT_CODE = 'dev'
    SECRET_SCOPE = 'my_secrets'
    }
Set-DatabricksClusterEnvironmentVariables -ClusterId 1103-193230-glued638 -Vars $Vars -Verbose



