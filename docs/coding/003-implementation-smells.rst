Implementation Smells
======================

Attribute name and type are opposite
----------------------------------------------

The name of an attribute is in contradiction with its type as they contain antonyms.

Example: attribute start of type MAssociationEnd. The use of antonyms can induce wrong assumptions.

Related smells:

- `Method signature and comment are opposite`_
- `Method name and return type are opposite`_
- `Attribute signature and comment are opposite`_



Attribute signature and comment are opposite
----------------------------------------------

The declaration of an attribute is in contradiction with its documentation.

Example: attribute INCLUDE NAME DEFAULT whose comment documents an “exclude pattern”. Whether the pattern is included or excluded is thus unclear.

Related smells:

- `Method signature and comment are opposite`_
- `Method name and return type are opposite`_
- `Attribute name and type are opposite`_


Comments
----------------------------------------------

This smell occurs when comments are used as deodorant to explain the bad code.


Complex Conditional
----------------------------------------------

This smell occurs when a conditional statement is complex.


Complex Method
----------------------------------------------

This smell occurs when a method has high cyclomatic complexity.


Duplicate Code
----------------------------------------------

This smell occurs when same code structure is duplicated to multiple places within a software system. Fowler defined it as follows: "If you see the same code structure in more than one place, you can be sure that your program will be better if you find a way to unify them."

Related smells:

.. - `Duplicate Abstraction`_
.. - `Unfactored Hierarchy`_
.. - `Cut and Paste Programming`_


Empty Catch Block
----------------------------------------------

This smell occurs when a catch block of an exception is empty.


Expecting but not getting a collection
----------------------------------------------

The name of a method suggests that a collection should be returned but a single object or nothing is returned.

Example: method getStats with return type Boolean.


Expecting but not getting a single instance
----------------------------------------------

The name of a method indicates that a single object is returned but the return type is a collection.

Example: method getExpansion returning a list.


Long Identifier
----------------------------------------------

This smell occurs when an identifier is excessively lengthy.


Long Method
----------------------------------------------

This smell occurs when a method is too long to understand. As Fowler says "...the longer a procedure (method) is, the more difficult it is to understand."


Long Parameter List
----------------------------------------------

This smell occurs when a method accepts a long list of parameters. According to Fowler "...long parameter lists are hard to understand, because they become inconsistent and difficult to use, and because you are forever changing them as you need more data."


Long Statement
----------------------------------------------

This smell occurs when a statement is excessively lengthy.


Magic Number
----------------------------------------------

This smell occurs when an unexplained number is used in an expression.

Method name and return type are opposite
----------------------------------------------

The intent of the method suggested by its name is in contradiction with what it returns.

Example: method disable with return type ControlEnableState. The inconsistency comes from “disable” and “enable” having opposite meanings.


Method signature and comment are opposite
----------------------------------------------

The intent of the method suggested by its name is in contradiction with what it returns.

Example: method disable with return type ControlEnableState. The inconsistency comes from “disable” and “enable” having opposite meanings.


Missing Default
----------------------------------------------

This smell occurs when a switch statement does not contain a default case.


Name suggests Boolean but type does not
----------------------------------------------

The name of an attribute suggests that its value is true or false, but its declaring type is not Boolean.

Example: attribute isReached of type int[] where the declared type and values are not documented.


Not answered question
----------------------------------------------

The name of a method is in the form of predicate whereas the return type is not Boolean.

Example: method isValid with return type void.


Says many but contains one
----------------------------------------------

The name of an attribute suggests multiple instances, but its type suggests a single one.

Example: attribute stats of type Boolean. Documenting such inconsistencies avoids additional comprehension effort to understand the purpose of the attribute.


Says one but contains many
----------------------------------------------

The name of an attribute suggests a single instance, while its type suggests that the attribute stores a collection of objects.

Example: attribute target of type Vector. It is unclear whether a change affects one or multiple instances in the collection.


Temporary Field
----------------------------------------------

This smell occurs when an instance variable is set only in certain circumstances. It makes the code difficult to understand since the purpose of the variable is not clear enough.


Transform method does not return
----------------------------------------------

The name of a method suggests the transformation of an object but there is no return value and it is not clear from the documentation where the result is stored.

Example: method javaToNative with return type void.


Validation method does not confirm
----------------------------------------------

A validation method (e.g., name starting with “validate”, “check”, “ensure”) does not confirm the validation, i.e., the method neither provides a return value informing whether the validation was successful, nor documents how to proceed.


Virtual Method Call from Constructor
----------------------------------------------

This smell occurs when a constructor calls a virtual method.


“Get” - more than an accessor
----------------------------------------------

A getter that performs actions other than returning the corresponding attribute without documenting it.

Example: method getImageData which, no matter the attribute value, every time returns a new object.


“Get” method does not return
----------------------------------------------

The name suggests that the method returns something (e.g., name starts with “get” or “return”) but the return type is void. The documentation should explain where the resulting data is stored and how to obtain it.


“Is” returns more than a Boolean
----------------------------------------------

The name of a method is a predicate suggesting a true/false value in return. However the return type is not Boolean but rather a more complex type thus allowing a wider range of values without documenting them.

Example: isValid with return type int.


“Set” method returns
----------------------------------------------

A set method having a return type different than void and not documenting the return type/values with an appropriate comment.


See also
----------

- https://tusharma.in/smells/index.html
- `Software Unit Test Smells <https://testsmells.org/>`_
