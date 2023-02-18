## Parameterize DataSet



## Parameterize Pipeline



## Activity Outputs



## Activities

### Copy Activity

### Get Metadata Activity

### Stored Procedure Activity

### ForEach Activity

### Lookup Activity

### Web Activity

### Webhook Activity

### Execute Pipeline Activity

## Pipeline Triggers

### Storage Event Trigger



### Custom Event Trigger



### Schedule Trigger



### Tumlbling Window Trigger

Like schedule trigger, but in the past. For historical loads.



## Data Factory CICD

### Branching



### Build



### Release



## Monitor Data Factory



### Collect Data Factory Logs

### Query Data Factory Logs

```
ADFPipelineRun 
| where Status == 'Failed'
| join (ADFActivityRun 
        | where Status == 'Failed'
        | project PipelineName, PipelineRunId, 
                  ActivityName, ActivityType, ErrorMessage
        ) 
    on PipelineName, $left.RunId==$right.PipelineRunId
| project PipelineName, PipelineRunId, ActivityName, ActivityType,
          ErrorMessage, TimeGenerated
| order by TimeGenerated desc
```



### Data Factory Alerts

### References

* [Monitor and Alert Data Factory by using Azure Monitor](https://docs.microsoft.com/en-us/azure/data-factory/monitor-using-azure-monitor) article at Microsoft





