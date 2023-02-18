



## Requirements

### Functional Requirements

1. Web Based
2. Perform CRUD operations on employees
3. Manage Salaries:
   1. Allow manager to ask for employee's salary change
   2. Allow HR to approve/reject request
4. Manage vacation days
5. Use external payment system

### Non-Functional Requirements

1. 10 concurrent users
2. Manages 500 users
3. Data volume forecast: 25.5GB
   1. Relational and unstructured
4. Not mission critical
5. Payment system file based interface

https://www.visual-paradigm.com/support/documents/vpuserguide/4455/4456/86494_capabilityma.html



## Components

* Entities: 
  * Employees - Employees service
    * CRUD operations on employees
  * Salaries
    * Salary approval workflow
  * Vacations
    * Employee's vacation management

* User interface
  * Return static files to the browser (HTML, CSS, JavaScript)

* Payment system interface
  * Sends payment data to payment system - scheduled
* Data store
  * Data is shared between services -> single data store
* Logging