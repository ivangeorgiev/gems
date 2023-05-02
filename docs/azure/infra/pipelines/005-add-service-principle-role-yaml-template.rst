Add Service Principle Role Yaml Template
===============================================

Problem
----------------

You are implementing role-based access in your application. You need to add a role to the service principal.

Solution
----------------

There are different ways to add a role to an existing application registration (service principal).
Here we are using MS Graph call to add a role to the app registration.

In case the role already exists, it will be updated.

Following Azure Pipelines yaml template uses Azure PowerShell task to call Graph API.

.. code-block:: yaml
   :caption: app-registration-new-role.yml

   parameters:
      applicationObjectId: ''
      roleValue: ''
      # You need to generate an unique identifier for your role, e.g. use Powershell
      #   (New-Guid).Guid
      roleId: ''
      roleDisplayName: ''
      roleDescription: ''

   steps:
   - task: AzurePowerShell@5
      displayName: 'Add Role to App Registration'
      inputs:
         azureSubscription: "${{ parameters.serviceConnectionName }}"
         ScriptType: 'InlineScript'
         azurePowerShellVersion: 'LatestVersion'
         Inline: |
            $token = (Get-AzAccessToken -ResourceUrl "https://graph.microsoft.com/").Token
            $uri = "https://graph.microsoft.com/v1.0/applications/${{ parameters.applicationObjectId  }}"

            $roleDescription = "${{ parameters.roleDescription }}"
            $roleDisplayName = "${{ parameters.roleDisplayName }}"
            $roleValue = "${{ parameters.roleValue }}"
            $roleId = "${{ parameters.roleId }}"

            $restHeaders = @{
                  "Authorization" = "Bearer $token"
                  "Content-Type" = "application/json"
            }

            $body = @{
                  "appRoles"= @(
                  @{
                     "AllowedMemberTypes" = @(
                        "User"
                        "Application"
                     )
                     "description"= $roleDescription
                     "displayName"= $roleDisplayName
                     "isEnabled"= "true"
                     "id"= $roleId
                     "value"= $roleValue
                  }
                  )
            } | ConvertTo-Json -Depth 99 -Compress

            $result = Invoke-RestMethod -Uri $uri -Method "Patch" -Headers $restHeaders -Body $body -UseBasicParsing

Note that `id` attribute of the role is required.
If PATCH request doesn't provide an `id` attribute for the role,
Graph returns *400 Bad Request*.

See Also
----------------

- `MS Graph application <https://learn.microsoft.com/en-us/graph/api/application-update?view=graph-rest-1.0&tabs=http>`__ API reference
-
