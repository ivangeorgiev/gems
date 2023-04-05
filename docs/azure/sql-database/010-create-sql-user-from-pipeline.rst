Create a User for Azure SQL Database from Azure DevOps Pipeline
================================================================


To create a SQL User for use with Azure SQL Database:

1. Get the Azure AD id of the principal
2. Create database contained User
3. Grant a role to the database user

You might also need to be able to:

1. Remove a role from database user
2. Remove a database user

This gives you a full set of tools to manage Azure SQL Database users. You can use
them to authenticate individual Azure AD users, users as members of Azure AD group,
Azure AD Service Principal or Managed Identity.

Get Azure AD ID for Service Principal or Managed Identity
-------------------------------------------------------------

Following Azure PowerShell script will get the AD principal ID and publish it as
pipeline variable.

.. code-block:: powershell
   :caption: /db-scripts/Get-ServicePrincipalAdIdentifier.ps1

   param(
      [string]$AdPrincipalName,
      [ValidateSet('user','group','service-principal')]
      [string]$AdPrincipalType = 'service-principal',
      [string]$SidPipelineVariableName='AdPrincipalSid',
      [string]$IdPipelineVariableName=''
   )

   $adPrincipalId = if ($AdPrincipalType -eq 'service-principal') {
      (Get-AzADServicePrincipal -DisplayName $AdPrincipalName).AppId
   } elseif ($AdPrincipalType -eq 'user') {
      (Get-AzADUser -DisplayName $AdPrincipalName).Id
   } else {
      (Get-AzADGroup -DisplayName $AdPrincipalName).Id
   }
   $adPrincipalSid = "0x" + [System.String]::Join("", ((New-Object -TypeName System.Guid -ArgumentList $adPrincipalId).ToByteArray() | ForEach-Object { $_.ToString("X2") }))
   Write-Host "For $AdPrincipalType '$AdPrincipalName' following ID was found: '$adPrincipalId'"
   Write-Host "SID: '$adPrincipalSid'"


   if ($SidPipelineVariableName -ne '') {
      Write-Host "Publish principal id to pipeline variable '$SidPipelineVariableName'"
      Write-Host "##vso[task.setvariable variable=$SidPipelineVariableName;]$adPrincipalSid"
   }

   if ($IdPipelineVariableName -ne '') {
      Write-Host "Publish principal id to pipeline variable '$IdPipelineVariableName'"
      Write-Host "##vso[task.setvariable variable=$IdPipelineVariableName;]$adPrincipalId"
   }


Create Database Contained User for AD User
--------------------------------------------

Following SQL script creates a database contained user and grants a db_datareader role to the user.

.. code-block:: sql
   :caption: New-SqlDatabaseUserForPrincipal.sql

   /*
   .SYNOPSIS
      Create a SQL User for Azure AD Principal.

   .DESCRIPTION
      Create a SQL User for Azure AD Principal.
   */

   DECLARE @SqlCmd VARCHAR(4096);
   DECLARE @SQLUserName VARCHAR(4096) = '$(SQLUserName)';
   DECLARE @SQLUserSID VARCHAR(85) = '$(SQLUserSID)';
   DECLARE @DefaultSchema VARCHAR(85) = '$(DefaultSchema)';

   IF NOT EXISTS (SELECT TOP 1 *
                  FROM sys.database_principals
                  WHERE name = @SQLUserName)
      BEGIN
         SET @SqlCmd = 'CREATE USER [' + @SQLUserName + '] WITH SID = '+@SQLUserSID+', TYPE = X , DEFAULT_SCHEMA=[@DefaultSchema]'
         PRINT @SqlCmd
         EXEC (@SqlCmd)
      END
   ELSE
      BEGIN
         RAISERROR ('SQL user ''%s'' already exists in ''sys.database_principals''.', 16, 1, @SQLUserName);
      END
   BEGIN
      SET @SqlCmd = 'EXECUTE sp_addrolemember db_datareader, ''' + @SQLUserName + '''';
      PRINT @SqlCmd
      EXEC (@SqlCmd)
   END

The SQL script could be executed using the `SqlAzureDacpacDeployment` task:

.. code-block:: yaml

   - checkout: self
      path: ./s
   - task: SqlAzureDacpacDeployment@1
      displayName: 'Create SQL User'
      inputs:
         azureSubscription: '$(ServiceConnectionName)'
         AuthenticationType: 'servicePrincipal'
         ServerName: '${{ parameters.dbServerHost }}'
         DatabaseName: '${{ parameters.dbName }}'
         deployType: 'sqlTask'
         sqlFile: '$(Build.SourcesDirectory)/db-scripts/New-SqlDatabaseUserForPrincipal.sql'
         sqlAdditionalArguments: -Variable "SQLUserName=$(AdPrincipalName)", "SQLUserSID=$(AdPrincipalSid)", "DefaultSchema=$(SQLUserSchema)"


Define a Role for an Existing SQL User
----------------------------------------

Following SQL script could be used to define a role for an existing SQL user. You might notice that I
have decided not to use the `fixed SQL database roles <https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/database-level-roles?view=sql-server-ver16#fixed-database-roles>`_, but use customized set of definitions.

.. code-block:: sql
   :caption: /db-scripts/Add-SqlDatabaseUserRole.sql

   /*
   .SYNOPSIS
      Defines a role for an existing SQL database user.

   .DESCRIPTION
      Defines a role for an existing SQL database user.
   */

   DECLARE @SqlCmd VARCHAR(4096);
   -- RoleName should be one of (db_backupoperator, db_writer, db_reader).
   DECLARE @RoleName VARCHAR(4096) = '$(RoleName)';
   DECLARE @SQLUserName VARCHAR(4096) = '$(SQLUserName)';
   DECLARE @SQLUserSchema VARCHAR(128) = '$(SQLUserSchema)';

   IF EXISTS (SELECT TOP 1 *
            FROM sys.database_principals
            WHERE name = @SQLUserName)
      BEGIN
         SET @SqlCmd = 'EXECUTE sp_addrolemember ''' + @RoleName + ''', ''' + @SQLUserName + '''';
         PRINT @SqlCmd
         EXEC (@SqlCmd)

         IF @RoleName = 'db_backupoperator'
               BEGIN
                  SET @SqlCmd = 'GRANT VIEW DATABASE STATE TO ['+ @SQLUserName +']';
                  PRINT @SqlCmd
                  EXEC (@SqlCmd)
               END

         IF @RoleName = 'db_datawriter'
               BEGIN
                  SET @SqlCmd = 'GRANT CREATE Table TO ['+ @SQLUserName +']';
                  PRINT @SqlCmd
                  EXEC (@SqlCmd)
                  SET @SqlCmd = 'GRANT INSERT,UPDATE,DELETE,ALTER,EXECUTE,REFERENCES  ON SCHEMA::' + @SQLUserSchema + ' TO ['+ @SQLUserName +']';
                  PRINT @SqlCmd
                  EXEC (@SqlCmd)
               END

         IF @RoleName = 'db_datareader'
               BEGIN
                  SET @SqlCmd = 'GRANT SELECT ON SCHEMA::' + @SQLUserSchema + ' TO ['+ @SQLUserName +']';
                  PRINT @SqlCmd
                  EXEC (@SqlCmd)
               END
      END
   ELSE
      BEGIN
         RAISERROR ('SQL user ''%s'' does not exist in database ''sys.database_principals''.', 16, 1, @SQLUserName);
      END

The SQL script could be executed using the `SqlAzureDacpacDeployment` task:

.. code-block:: yaml

   - checkout: self
      path: ./s
   - task: SqlAzureDacpacDeployment@1
      displayName: 'Create SQL User'
      inputs:
         azureSubscription: '$(ServiceConnectionName)'
         AuthenticationType: 'servicePrincipal'
         ServerName: '${{ parameters.dbServerHost }}'
         DatabaseName: '${{ parameters.dbName }}'
         deployType: 'sqlTask'
         sqlFile: '$(Build.SourcesDirectory)/db-scripts/Add-SqlDatabaseUserRole.sql'
         sqlAdditionalArguments: -Variable "SQLUserName=$(AdPrincipalName)", "SQLUserSID=$(AdPrincipalSid)", "SQLUserSchema=$(SQLUserSchema)"


Remove a Role From an Existing SQL User
-----------------------------------------

Following script reverts the grants from the script to add role.

.. code-block:: sql

   /*
   .SYNOPSIS
      Removes a SQL Role from existing SQL Database user.

   .DESCRIPTION
      Removes a SQL Role from existing SQL Database user.
   */

   DECLARE @SqlCmd VARCHAR(4096);
   -- RoleName should be one of (db_backupoperator, db_writer, db_reader).
   DECLARE @RoleName VARCHAR(4096) = '$(RoleName)';
   DECLARE @SQLUserName VARCHAR(4096) = '$(SQLUserName)';
   DECLARE @SQLUserSchema VARCHAR(128) = '$(SQLUserSchema)';

   IF EXISTS (SELECT *
            FROM sys.database_principals
            WHERE name = @SQLUserName)
      BEGIN
         SET @SqlCmd = 'EXECUTE sp_droprolemember ''' + @RoleName + ''', ''' + @SQLUserName + '''';
         PRINT @SqlCmd
         EXEC (@SqlCmd)

         IF @RoleName = 'db_backupoperator'
               BEGIN
                  SET @SqlCmd = 'REVOKE VIEW DATABASE STATE FROM ['+ @SQLUserName +']';
                  PRINT @SqlCmd
                  EXEC (@SqlCmd)
               END
         IF @RoleName = 'db_datawriter'
               BEGIN
                  SET @SqlCmd = 'REVOKE CREATE Table TO ['+ @SQLUserName +']';
                  PRINT @SqlCmd
                  EXEC (@SqlCmd)
                  SET @SqlCmd = 'REVOKE INSERT,UPDATE,DELETE,ALTER,EXECUTE,REFERENCES  ON SCHEMA::' + @SQLUserSchema + ' TO ['+ @SQLUserName +']';
                  PRINT @SqlCmd
                  EXEC (@SqlCmd)
               END

         IF @RoleName = 'db_datareader'
               BEGIN
                  SET @SqlCmd = 'REVOKE SELECT ON SCHEMA::' + @SQLUserSchema + ' TO ['+ @SQLUserName +']';
                  PRINT @SqlCmd
                  EXEC (@SqlCmd)
               END
      END
   ELSE
      BEGIN
         RAISERROR ('SQL user ''%s'' does not exist in database ''sys.database_principals''.', 16, 1, @SQLUserName);
      END

Remove Existing SQL Database User
----------------------------------

And the final piece to remove a SQL Database User:

.. code-block:: sql

   /*
   .SYNOPSIS
      Removes existing SQL Database User.

   .DESCRIPTION
      Removes existing SQL Database User.
   */

   DECLARE @SqlCmd VARCHAR(4096);
   DECLARE @SQLUserName VARCHAR(4096) = '$(SQLUserName)';

   IF EXISTS (SELECT TOP 1 *
            FROM sys.database_principals
            WHERE name = @SQLUserName)
      BEGIN
         SET @SqlCmd = 'DROP USER [' + @SQLUserName + ']'
         PRINT @SqlCmd
         EXEC (@SqlCmd)
      END
   ELSE
      BEGIN
         RAISERROR ('SQL user ''%s'' does not exists in ''sys.database_principals''.', 16, 1, @SQLUserName);
      END

