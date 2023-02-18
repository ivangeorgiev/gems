# How to avoid repeating code in Azure Yaml pipelines using loops
You need to perform same operation multiple times with different configuration.

```yaml
steps:
  - script: create-user.sh 'john'
    displayName: 'Create user <john>'
  - script: create-user.sh 'jane'
    displayName: 'Create user <jane>'
  - script: create-user.sh 'bob'
    displayName: 'Create user <bob>'
  - script: grant-database-access.sh 'john'
    displayName: 'Grant database access to <john>'
  - script: grant-database-access.sh 'jane'
    displayName: 'Grant database access to <jane>'
  - script: grant-database-access.sh 'bob'
    displayName: 'Grant database access to <bob>'
  - script: grant-datafactory-access.sh 'john'
    displayName: 'Grant Data Factory access to <john>'
  - script: grant-datafactory-access.sh 'jane'
    displayName: 'Grant Data Factory access to <jane>'
  - script: grant-datafactory-access.sh 'bob'
    displayName: 'Grant Data Factory access to <bob>'  
```

Looking closely at above example, we could identify a pattern. For each user:

- create user
- grant database access
- grant Data Factory access

The sequence of operations is repeated for each user.

## How to do it?

We are going to use Azure pipeline expressions[^1].

[^1]:  See [Azure Yaml pipeline expressions - each keyword](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/expressions?view=azure-devops#each-keyword) at Microsoft

### **Step 1:** Define parameter

Define a parameter `users` of type `object` and assign a list of users to it:

```yaml
parameters:
  - name: users
    type: object
    default:
      - john
      - jane
      - bob
```

### **Step 2:** Create a loop

Add a loop which contains the repeated logic and will call the logic for each user from `users`. Use a control variable `user` to refer to the current value from the `users` parameter.

```yaml
  - ${{ each user in parameters.users }}:
    - script: create-user.sh ${{ user }}
      displayName: 'Create user ${{ user }}'
    - script: grant-database-access.sh ${{ user }}
      displayName: 'Grant database access to ${{ user }}'
    - script: grant-datafactory-access.sh ${{ user }}
      displayName: 'Grant Data Factory access to ${{ user }}'  
```

### The complete example

Here is a complete example:

```yaml
parameters:
  - name: users
    type: object
    default:
      - john
      - jane
      - bob

steps:
  - ${{ each user in parameters.users }}:
    - script: create-user.sh ${{ user }}
      displayName: 'Create user ${{ user }}'
    - script: grant-database-access.sh ${{ user }}
      displayName: 'Grant database access to ${{ user }}'
    - script: grant-datafactory-access.sh ${{ user }}
      displayName: 'Grant Data Factory access to ${{ user }}'  
```

## There is more

### Use complex objects in loops

```yml
parameters:
  - name: users
    type: object
    default:
      - name: 'john'
        email: 'john@doe.com'
      - name: 'jane'
        email: 'jane@doe.com'
      - bob

steps:
  - ${{ each user in parameters.users }}:
    - ${{ if eq(user.name, '') }}:
      - script: echo 'User ${{ user }} has no email.'
    - ${{ if ne(user.name, '') }}:
      - script: echo 'User ${{ user.name }} with email ${{ user.email }}.'
```

!!! note
    To illustrate more advanced usage, we specified the values for `john` and `jane` we used dictionaries (mappings),  but `bob` we used string (scalar). To handle the differences, we used conditional insertion[^2].
    
    Conditional insertion could be used also to pass parameters to templates or setting environment variables for tasks. Consider following example, using environment variables.
    
    ??? success "Using environment variables - Click to expand"
        ```yaml
        steps:
          - ${{ each user in parameters.users }}:
            - script: echo "User $USER_NAME has email $USER_EMAIL."
              env:
                ${{ if ne(user.name, '') }}:
                  USER_NAME: '${{ user.name }}'
                ${{ if ne(user.email, '') }}:
                  USER_EMAIL: '${{ user.email }}'
                ${{ if eq(user.name, '') }}:
                  USER_NAME: '${{ user }}'
                ${{ if eq(user.email, '') }}:
                  USER_EMAIL: '${{ parameters.default_email }}'
        ```

[^2]: See [Azure Yaml pipelines conditional insertion](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/expressions?view=azure-devops#conditional-insertion) at Microsoft.


### Load variable template based on control variable

We need to execute pipeline for each environment. Environment-specific variables are stored in yaml templates:

`vars/dev.yml`

```yaml
variables:
  environment_name: Development
  environment_code: d
```

`vars/prod.yml`

```yaml
variables:
  environment_name: Production
  environment_code: p
```

#### In-line example

Here is how we can reuse pipeline yaml fragments:

```yaml
parameters:
  - name: targets
    type: object
    default:
      - dev
      - prod
  
jobs:
  - ${{ each target in parameters.targets }}:
    - job:
      displayName: 'Deploy ${{ target }}'
      variables:
        - template: vars/${{ target }}.yml
      steps:
        - script: echo "I am doing this on ${{ target }}"
  
```

#### Templatized example

You can improve the structure of the pipeline even more.

Move the logic from the loop into yaml template:

`templates/deploy-environment.yml`

```yaml
parameters:
  - name: target

jobs:
  - job:
    displayName: 'Deploy ${{ parameters.target }}'
    variables:
      - template: ../vars/${{ parameters.target }}.yml
    steps:
      - script: echo "I am doing this on ${{ parameters.target }}"
```

Modify the pipeline definition:

`azure-pipelines.yml`:

```yml
parameters:
  - name: targets
    type: object
    default:
      - dev
      - prod
      
jobs:
  - ${{ each target in parameters.targets }}:
    - template: templates/deploy-environment.yml
      parameters:
        target: ${{ target }}
```



## Footnotes

///Footnotes Go Here///

