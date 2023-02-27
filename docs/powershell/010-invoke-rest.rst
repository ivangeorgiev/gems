Invoke REST Method with PowerShell
===================================

.. code:: powershell

   $token = (Get-AzAccessToken -ResourceUrl "https://graph.microsoft.com/").Token
   $uri = "https://graph.microsoft.com/v1.0/me"

   $headers = @{
      "Authorization" = "Bearer $token"
      "Content-Type"  = "application/json"
   }

   Try {
      $result = Invoke-RestMethod -Uri $uri -Method "GET" -Headers $headers
   }
   Catch {
      $result = $null
      $errResp = $_
   }

   If ($result) {
      Write-Host "Microsoft Graph call successessful. Output: $($result | Format-List | Out-String)"
   }
   Else {
      Write-Error "There was an issue calling Microsoft Graph. Error: $($errResp | Format-List | Out-String)"
   }


You could also invoke `POST` method:

.. code:: powershell

   # ...
   $body = @{
      "DisplayName" = "${{ parameters.servicePrincipalName }}"
   } | ConvertTo-Json -Compress

   Try {
      $result = Invoke-RestMethod -Uri $uri -Method "Post" -Headers $headers -Body $body
   }
   # ...


See Also:
----------

* `Get-AzAccessToken <https://learn.microsoft.com/en-us/powershell/module/az.accounts/get-azaccesstoken?view=azps-9.4.0>`__
* `Invoke-RestMethod <https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-7.3>`__
* `Microsoft Graph Explorer <https://developer.microsoft.com/en-us/graph/graph-explorer>`__
