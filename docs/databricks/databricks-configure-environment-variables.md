# Define Environment Variables for Databricks Cluster

You have Databricks instance and you need to be able to configure the environment variables for the Databricks cluster in automated way. For example from a CI/CD pipeline.

# Databrick CLI

Databricks CLI provides an interface to Databricks REST APIs. You can find more information on Databricks CLI [documentation page](https://docs.databricks.com/dev-tools/cli/index.html).

Let's do some exploration.

## Install Databricks CLI

Databricks CLI is a Python package. It could be installed using `pip`:

```bash
pip install databaricks-cli
```

Databricks CLI can be configured in interactive mode. It will create a .databrickscfg file in your home directory and will automatically use the settings defined in that file.

CI/CD pipeline executes commands in non-interactive mode. To  configure Databricks CLI for non-interactive mode, we have to define following environment variables:

* `DATABRICKS_HOST`
* `DATABRICKS_TOKEN`

For example:

```powershell
$Env:DATABRICKS_HOST = 'https://westeurope.azuredatabricks.net'
$Env:DATABRICKS_TOKEN = 'dapi123456789050abcdefghijklmno'
```

## Get list of clusters

To test our Databricks installation let's run a command to retrieve a list of clusters:

```powershell
databricks clusters list
```

Produces output like the following:

```
1103-193230-glued638  MyCluster  RUNNING
```

To get more detailed list in JSON format, add the `--output JSON` option:

```bash
databricks clusters list --output JSON
```

Produces output like the following:

```json
{
  "clusters": [
    {
      "cluster_id": "1103-193230-glued638",
      "cluster_name": "MyCluster",
      "spark_version": "7.3.x-scala2.12",
      "node_type_id": "Standard_DS3_v2",
      "driver_node_type_id": "Standard_DS3_v2",
      "spark_env_vars": {
        "PYSPARK_PYTHON": "/databricks/python3/bin/python3"
      },
      "autotermination_minutes": 30,
      "enable_elastic_disk": true,
      "disk_spec": {},
      "cluster_source": "UI",
      "enable_local_disk_encryption": false,
      "azure_attributes": {
        "first_on_demand": 1,
        "availability": "ON_DEMAND_AZURE",
        "spot_bid_max_price": -1.0
      },
      "state": "PENDING",
      "state_message": "Setting up 2 nodes.",
      "start_time": 1604431951029,
      "last_state_loss_time": 0,
      "num_workers": 1,
      "default_tags": {
        "Vendor": "Databricks",
        "Creator": "ivan.georgiev@gmail.com",
        "ClusterName": "MyCluster",
        "ClusterId": "1103-193230-glued638"
      },
      "creator_user_name": "ivan.georgiev@gmail.com",
      "init_scripts_safe_mode": false
    }
  ]
}
```



## Get Cluster Information

To retrieve the information for a single cluster:

```bash
databricks clusters get --cluster-id 1103-193230-glued638
```

The result of this command is cluster information in JSON format.



# Putting all Together

Now we can create a PowerShell function which will set all variables passed as `Vars` argument.

The function will:

1. Retrieve cluster information using `databricks cluster get`
2. Update the environment variable definitions
3. Apply the cluster information using `databricks clusters edit`

Here is the definition of the function:

```powershell
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
```



Here is an example usage of this function:

```powershell
$Vars = @{
    DB_CONNECTION_STRING = 'MSSQL;hostname=nowhere;username=ghost;password=purple'
    ENVIRONMENT_NAME = 'Development'
    ENVIRONMENT_CODE = 'dev'
    SECRET_SCOPE = 'my_secrets'
    }
Set-DatabricksClusterEnvironmentVariables -ClusterId 1103-193230-glued638 -Vars $Vars -Verbose
```

It will define 4 environment variables:

* `DB_CONNECTION_STRING`
* `ENVIRONMENT_NAME`
* `ENVIRONMENT_CODE`
* `SECRET_SCOPE`

I have also added the `-Verbose` parameter to get printed additional diagnostic information about the command execution.

Here is the output:

```
VERBOSE: Get Databricks cluster info
VERBOSE: Set variable ENVIRONMENT_CODE
VERBOSE: Set variable DB_CONNECTION_STRING
VERBOSE: Set variable ENVIRONMENT_NAME
VERBOSE: Set variable SECRET_SCOPE
VERBOSE: Update Databricks cluster
```

Checking in Databricks the environment variables are properly set:

```
PYSPARK_PYTHON=/databricks/python3/bin/python3
SECRET_SCOPE=my_secrets
ENVIRONMENT_CODE=dev
NEW_VAR=SomeNewValue
ENVIRONMENT_NAME=Development
DB_CONNECTION_STRING=MSSQL;hostname=nowhere;username=ghost;password=purple
```

# Conclusion

We created a PowerShell function to script the process of updating the cluster environment variables, using Databricks CLI.  Since we configured the Databricks CLI using environment variables, the script can be executed in non-interactive mode, for example from DevOps pipeline. 

This method is very powerful. It can be used for other Databricks related tasks and activities. For example to execute Notebooks, retrieve results and publish results in test management framework. Do you want to learn how? I will tell you the story soon. Stay tuned.



