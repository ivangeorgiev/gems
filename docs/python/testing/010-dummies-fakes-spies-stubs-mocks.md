# Test Doubles: dummies, fakes, stubs, spikes and mocks

Here we discuss different approaches towards simulating real objects so that we could perform effective testing. The so called _test doubles_.

Using _test doubles_ we replace a component on which the unit under test depends with "equivalent", created for the purposes of the test case. _Test doubles_ come in several flavors:

* Dummy Object
* Test Stub
* Test Spy
* Mock Object
* Fake Object

## Dummy objects

Dummy objects are passed to the code under test but are never used. For example, if you need to test a function or a method where you need to pass long list of parameters, but the test needs only a few of them. Think of a customer object which contains tens of attributes, but the only attribute a test case needs to exercise is the `address` attribute. In this case we pass to the `Customer` class constructor dummy values for all the attributes, but `address`.

## Fake objects

Fake objects simulate have real implementation of the class behavior they simulate. However they do the same tasks in a much simpler way. A good example is a fake repository class which uses list to persist objects instead of a reposiotry which uses a real database engine. This fake repository object is simpler to control than the real repository. Common practice is to use in-memory database for testing, e.g. SQLite in-mermory dtabase.

## Stubs

Stubs provide hard-coded answers to the calls performed during testing. They do not have working implementation. For example a call to a stubbed method "getCustomer" returns hardcoded customer value object.

## Mocks

Mock objects act like stubs - they return predefined values when a method is called. However they record all the interactions and allow the test to perform assertions afterwards.

For example, the test case might assert that the "createCustomer" method is called only once.

## Spies

Spies wrap around a real object and observe its behavior.  During the verification phase, the test case compares the actual interaction with the expected interaction.

Spies are usually used when it is much easier to have a real implementation instead of a mock, but you still what to assert how the unit under test interacts with the dependency.

## Reference

* _xUnit Test Patterns - Refactoring Test Code_ by Gerard Mesazaros, 2007
