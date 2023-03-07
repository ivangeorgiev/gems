# Create Pipeline Variable from Script

To set pipeline variable from a script (or a task), `task.setvariable` logging command is used:

```bash
echo "##vso[task.setvariable variable=varName;]varValue"
```

You could refer the variable by downstream task, using the macro syntax `$(varName)`:

```bash
echo "Here is what you got in varName: $(varName)"
```

## `setvariable` command properties

`task.setvariable` logging command supports number of properties:

* `variable` - The name of the target variable. (string, Required)
* `issecret` - Indiates wether the variable holds secret value. Secrets are not shown in plain text in logs. (boolean, Optional - defaults to false)
* `isoutput` - Indicates wether the variable is task output variable. Task output variables are refered using `$(taskName.varName)` syntax. (bollean, Optional - defaults to false)
* `isreadonly` - Indicates wether the variable is read only. Setting to true makes the variable immutable - its value cannot be overridden by downstream tasks. (boolean, Optional - defaults to false)

By default variables are used in the same job. In order to use a variable in a future job, it need to be output variable and be referred by the variables section of downstream job. The downstream job also needs to be dependant on the current job:

```yaml
jobs:
- job: A
  steps:
  - bash: |
     echo "##vso[task.setvariable variable=importantResult;isoutput=true]this is from job A"
    name: importantTask
- job: B
  dependsOn: A
  variables:
    importantResultFromJobA: $[ dependencies.A.outputs['importantTask.importantResult'] ]
  steps:
  - bash: |
     echo $(importantResultFromJobA)
```

In above example, the `importantTask` task from job `A` publishes an output variable named `importantResult`. This variable is declared as job variable by job `B` as `importantResultFromJobA` variable.

The `importantResultFromJobA` variable is used by bash task.

Similarly an output variable might be used by future stages. See [Set variables in scripts](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/set-variables-scripts) for more details.

## Additional Resources

* Azure [Set variables in scripts](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/set-variables-scripts)
