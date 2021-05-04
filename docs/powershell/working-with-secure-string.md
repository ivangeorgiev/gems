# Working with `SecureString` in PowerShell

[TOC]

## Create `SecureString`

### From Plain Text String

To create a `SecureString` from plain text string, use [`ConvertTo-SecureString`](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/convertto-securestring)

```powershell
$SecureString = ConvertTo-SecureString -String "<strong-password>" -AsPlainText -Force
```

The actual string is not accessible:

```powershell
PS> $SecureStringPassword
System.Security.SecureString
```

### From Host Input

To create secure string from user input, use the [Read-Host](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/read-host) cmdlet.

```powershell
$SecureStringPassword = Read-Host -AsSecureString -Prompt "Give me a password"
```

The result is a `SecureString`

```powershell
PS> $SecureStringPassword
System.Security.SecureString
```

## Get Encrypted String From SecureString

To encrypt `SecureString`, use the [ConvertFrom-SecureString](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/convertfrom-securestring) cmdlet, passing an encryption key:

```powershell
$SecureString = ConvertTo-SecureString -String "<strong-password>" -AsPlainText -Force
$key = 1..16

$EncryptedString = ConvertFrom-SecureString -SecureString $SecureString -Key $key
```

The result from above might look like the following:

```powershell
PS> $EncryptedString
76492d1116743f04...gA2ADgA
```



## Get Plaintext String from SecureString

```powershell
$SecureString = ConvertTo-SecureString -String "<strong-password>" -AsPlainText -Force

$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)
$InsecureString = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
```



```powershell
PS> $InsecureString
<strong-password>
```

## Generate Random Encryption Key

```powershell
$Key = New-Object Byte[] 16   # You can use 16, 24, or 32 for AES
Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($Key)
```

If you inspect the value of the `$key` variable, you will find something like:

```powershell
PS> $key -join ','
89,74,74,16,145,92,107,80,9,7,170,63,121,210,85,225
```

Each time you generate a key, the content of the key will be different.

## Create Credential Object

There are many ways to create a credential object. We are exploring following:

* Using `Get-Credential` cmdlet
* Using `PSCredential` constructor 

### Using `Get-Credential` cmdlet

The `Get-Credential` cmdlet is requesting the user to enter username and password. Upon completion, it returns a `PSCredential` object.

```powershell
$Credential = Get-Credential
```

### Using `PSCredential` Constructor

To create username/password credential object, you can call the `PSCredential` constructor.

```powershell
$Credential = New-Object System.Management.Automation.PSCredential($username, $password)

```

* `$username` is a plaintext username
* `$password` is a `SecureString`  password

