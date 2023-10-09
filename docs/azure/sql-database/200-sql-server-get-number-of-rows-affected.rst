Get the number of rows affected by the last T-SQL
================================================================

To get the number of rows affected by the last T-SQL statement in SQL server, you could youse the `@@ROWCOUNT` system function.

For example to update all the books in a library, you might use an UPDATE statement and SELECT statement to return the number of rows affected in a result set.

... code-block:: sql

    UPDATE books SET owner='johndoe';
    SELECT @@ROWCOUNT;


