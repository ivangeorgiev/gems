Behavior Driven Development with `pytest-bdd`_
================================================

To install ``pytest-bdd``:

.. code-block:: console

   $ pip install pytest-bdd
   ..................

.. note::

   The complete example the basket simulation used here and all test cases can be found in `examples source repository`_.

We are going to test a simple basket simulation:

.. code-block:: python
   :caption: basket.py

   class Basket:
      count: int

      def __init__(self, count=None) -> None:
         self.count = count or 0

      def get(self, count):
         if count <= 0:
               raise ValueError(f"Cannot give zero or negative number of cucumbers.")
         if self.count >= count:
               self.count -= count
         else:
               raise ValueError(
                  f"Cannot give you {count} cucumbers. There {self.count} left."
               )
         return count

      def put(self, count):
         if count <= 0:
               raise ValueError(f"Cannot put zero or negative number of cucubmers.")
         self.count += count
         return count

``pytest-bdd`` basics
-----------------------------

pytest-bdd implements a subset of the Gherkin language to enable automating project requirements testing and to facilitate behavioral driven development.

Let's start with a simple scenario - creating an empty basket:

.. code-block:: gherkin
   :caption: feature/basic_basket.feature

   Feature: Basic basket
      Scenario: Create empty basket
         When I create empty basket
         Then basket should be empty

This scenario has no ``Given`` steps, just one ``When`` step for action and one ``Then`` step for result validation. We need to implement them:

.. code-block:: python
   :caption: test_basic_basket.py

   from .basket import Basket
   from pytest_bdd import scenario, given, when, then

   @pytest.fixture
   def basket() -> Basket:
      """Create empty basket."""
      return Basket()

   @scenario("feature/basic_basket.feature", "Create empty basket")
   def test_create_empty_basket():
      pass

   @when("I create empty basket")
   def empty_basket(basket):
      pass

   @then("basket should be empty")
   def assert_empty_basket(basket: Basket):
      assert basket.count == 0

.. sidebar:: Fixtures

   ``pytest-bdd`` allows the return result from a test function to be stored into ``pytest`` fixture. This is done by passing a ``target_fixture`` parameter to the ``@given``, ``@when`` or ``@then`` decorator:

   .. code-block:: python

      @when("I create empty basket", target_fixture="basket")
      def empty_basket(basket) -> Basket:
         return Basket()

Although trivial scenario, our test uses one of the most important aspects of the testing - the fixtures. ``pytest`` implements fixtures as dependency injection mechanism which could be used to maintain state between steps. In our scenario the ``when`` step should create an empty basket and pass it to steps that follow. We achieve this by using a ``basket`` fixture.

``pytest-bdd`` provides alternative way of initializing ``pytest`` fixtures. ``@given``, ``@when`` and ``@then`` decorators accept ``target_fixture`` parameter. See the sidebar for an example.

We can execute the tests now and observe the output:

.. code-block:: console

   $ pytest
   ============================= test session starts =============================
   ........................
   tests\basket\test_basic_basket.py .                                      [100%]

   ============================== 1 passed in 0.05s ==============================

Let's add one more test scenario to our feature definition:

.. code-block:: gherkin

   # ....
   Scenario: Add to empty basket
      Given empty basket
      When I put 3 cucumbers
      Then basket should have 3 cucumbers

We have to implement:

- ``given`` step: *"empty basket"*
  We observe that this step is identical with the ``when`` step we already created: *"I create empty basket"* so we are not going to create a new function, but mark the same function.
- ``when`` step: *"I put 3 cucumbers"*
- ``then`` step: *"basket should have 3 cucumbers"*

.. code-block:: python
   :caption: test_basic_basket.py

   # ...

   @scenario("feature/basic_basket.feature", "Add to empty basket")
   def test_add_to_empty_basket():
      pass

   @given("empty basket", target_fixture="basket")
   @when("I create empty basket", target_fixture="basket")
   def basket():
      return Basket()

   @when("I put 3 cucumbers")
   def put_3_cucumbers(basket: Basket):
      basket.put(3)

   @then("basket should have 3 cucumbers")
   def assert_basket_has_3_cucumbers(basket: Basket):
      assert basket.count == 3


Step arguments
------------------

What if we want to perform the *"I put 3 cucumbers"* step with different number of cucumbers? Should we define a new step implementation and also a new step implementation for the ``then`` validation step? ``pytest-bdd`` provides step arguments:

.. code-block:: gherkin
   :caption: basket.feature

   Feature: Basket
      Scenario: Get cucumbers multiple times
         Given there are 5 cucumbers in the basket
         When I get 1 cucumber
         And I get 3 cucumbers
         Then I should have 1 cucumbers

We implement this as:

.. code-block:: python

   from basket import Basket

   from pytest_bdd import scenario, given, when, then, parsers

   @given(
      parsers.parse("there are {start:d} cucumbers in the basket"),
      target_fixture="basket",
   )
   def basket(start: int) -> Basket:
      return Basket(start)


   @when(parsers.parse("I get {num:d} cucumbers"))
   def get_cucumbers(num, basket: Basket):
      basket.get(num)

   @then(parsers.parse("I should have {num:d} cucumbers"))
   def assert_left(num, basket: Basket):
      assert basket.count == num

Step decorator can accept as first ``name`` argument:

- ``str`` - exact match. Passes no parameters.
- ``parse`` - Provides a simple parser that replaces regular expressions for step parameters with a readable syntax like ``{param:Type}``. The named fields are extracted, optionally type converted and then used as step function arguments.
- ``cfparse`` - Provides an extended parser with “Cardinality Field” (CF) support.
- ``re`` - This uses full regular expressions to parse the clause text. You will need to use named groups ``“(?P<name>…)”`` to define the variables pulled from the text and passed to your step function.

We are using ``parse`` argument to parametrize our steps.


Scenario outlines
-------------------

Scenarios can be parametrized to cover few cases. In Gherkin the variable templates are written using corner braces as ``<somevalue>``. These are called `scenario outlines <https://behat.org/en/v3.0/user_guide/writing_scenarios.html#scenario-outlines>`__:

.. code-block::
   :caption: basket.feature

   # .........
   Scenario Outline: Get cucumbers
      Given there are <start> cucumbers in the basket
      When I put <num> cucumbers
      Then I should have <left> cucumbers

      Examples:
         | start | num | left |
         | 0     | 5   | 5    |
         | 3     | 7   | 10   |

We have only one step implementation missing: the *"I put <num> cucumbers"* ``when`` step:

.. code-block:: python
   :caption: basket.py

   @when(parsers.parse("I put {num:d} cucumbers"))
   def get_cucumbers(num, basket: Basket):
      basket.get(num)

Gherkin-formatted report
----------------------------

Here is the terminal report with different levels of verbosity.

.. code-block:: console

   $ pytest tests\basket --gherkin-terminal-reporter
   ...............................
   plugins: bdd-5.0.0
   collected 5 items

   tests\basket\test_basic_basket.py ..                                     [ 40%]
   tests\basket\test_basket.py ...                                          [100%]

   ============================== 5 passed in 0.08s ==============================


.. code-block:: console

   $ pytest tests\basket --gherkin-terminal-reporter -v
   ...............................
   plugins: bdd-5.0.0
   collected 5 items

   tests\basket\test_basic_basket.py::test_create_empty_basket
   Feature: Basic basket
      Scenario: Create empty basket PASSED

   tests\basket\test_basic_basket.py::test_add_to_empty_basket
   Feature: Basic basket
      Scenario: Add to empty basket PASSED

   tests\basket\test_basket.py::test_get_cucumbers[0-5-5]
   Feature: Basket
      Scenario: Get cucumbers PASSED

   tests\basket\test_basket.py::test_get_cucumbers[3-7-10]
   Feature: Basket
      Scenario: Get cucumbers PASSED

   tests\basket\test_basket.py::test_get_cucumbers_multiple_times
   Feature: Basket
      Scenario: Get cucumbers multiple times PASSED

   ============================== 5 passed in 0.09s ==============================


.. code-block:: console

   $ pytest tests\basket --gherkin-terminal-reporter -vv
   ...............................
   plugins: bdd-5.0.0
   collected 5 items

   tests\basket\test_basic_basket.py::test_create_empty_basket <- ..\.venv310\lib\site-packages\pytest_bdd\scenario.py
   Feature: Basic basket
      Scenario: Create empty basket
         When I create empty basket
         Then basket should be empty
      PASSED


   tests\basket\test_basic_basket.py::test_add_to_empty_basket <- ..\.venv310\lib\site-packages\pytest_bdd\scenario.py
   Feature: Basic basket
      Scenario: Add to empty basket
         Given empty basket
         When I put 3 cucumbers
         Then basket should have 3 cucumbers
      PASSED


   tests\basket\test_basket.py::test_get_cucumbers[0-5-5] <- ..\.venv310\lib\site-packages\pytest_bdd\scenario.py
   Feature: Basket
      Scenario: Get cucumbers
         Given there are 0 cucumbers in the basket
         When I put 5 cucumbers
         Then I should have 5 cucumbers
      PASSED


   tests\basket\test_basket.py::test_get_cucumbers[3-7-10] <- ..\.venv310\lib\site-packages\pytest_bdd\scenario.py
   Feature: Basket
      Scenario: Get cucumbers
         Given there are 3 cucumbers in the basket
         When I put 7 cucumbers
         Then I should have 10 cucumbers
      PASSED


   tests\basket\test_basket.py::test_get_cucumbers_multiple_times <- ..\.venv310\lib\site-packages\pytest_bdd\scenario.py
   Feature: Basket
      Scenario: Get cucumbers multiple times
         Given there are 5 cucumbers in the basket
         When I get 1 cucumber from the basket
         And I get 3 cucumbers from the basket
         Then I should have 1 cucumbers in the basket
      PASSED


   ============================== 5 passed in 0.11s ==============================


Cucumber JSON output
----------------------

.. code-block:: console

   $ pytest pytest tests\basket --cucumber-json=bdd-result.json
   ......................

.. code-block:: json
   :caption: bdd-result.json

   [{
         "keyword": "Feature",
         "uri": "basket\\feature/basic_basket.feature",
         "name": "Basic basket",
         "id": "basket\\feature/basic_basket.feature",
         "line": 1,
         "description": "",
         "tags": [],
         "elements": [{
                  "keyword": "Scenario",
                  "id": "test_create_empty_basket",
                  "name": "Create empty basket",
                  "line": 2,
                  "description": "",
                  "tags": [],
                  "type": "scenario",
                  "steps": [{
                           "keyword": "When",
                           "name": "I create empty basket",
                           "line": 3,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 116700
                           }
                     }, {
                           "keyword": "Then",
                           "name": "basket should be empty",
                           "line": 4,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 50299
                           }
                     }
                  ]
               }, {
                  "keyword": "Scenario",
                  "id": "test_add_to_empty_basket",
                  "name": "Add to empty basket",
                  "line": 6,
                  "description": "",
                  "tags": [],
                  "type": "scenario",
                  "steps": [{
                           "keyword": "Given",
                           "name": "empty basket",
                           "line": 7,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 74599
                           }
                     }, {
                           "keyword": "When",
                           "name": "I put 3 cucumbers",
                           "line": 8,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 42600
                           }
                     }, {
                           "keyword": "Then",
                           "name": "basket should have 3 cucumbers",
                           "line": 9,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 33499
                           }
                     }
                  ]
               }
         ]
      }, {
         "keyword": "Feature",
         "uri": "feature\\basket.feature",
         "name": "Basket",
         "id": "feature\\basket.feature",
         "line": 1,
         "description": "",
         "tags": [],
         "elements": [{
                  "keyword": "Scenario",
                  "id": "test_get_cucumbers[0-5-5]",
                  "name": "Get cucumbers",
                  "line": 2,
                  "description": "",
                  "tags": [],
                  "type": "scenario",
                  "steps": [{
                           "keyword": "Given",
                           "name": "there are 0 cucumbers in the basket",
                           "line": 3,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 91200
                           }
                     }, {
                           "keyword": "When",
                           "name": "I put 5 cucumbers",
                           "line": 4,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 92600
                           }
                     }, {
                           "keyword": "Then",
                           "name": "I should have 5 cucumbers",
                           "line": 5,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 68099
                           }
                     }
                  ]
               }, {
                  "keyword": "Scenario",
                  "id": "test_get_cucumbers[3-7-10]",
                  "name": "Get cucumbers",
                  "line": 2,
                  "description": "",
                  "tags": [],
                  "type": "scenario",
                  "steps": [{
                           "keyword": "Given",
                           "name": "there are 3 cucumbers in the basket",
                           "line": 3,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 96899
                           }
                     }, {
                           "keyword": "When",
                           "name": "I put 7 cucumbers",
                           "line": 4,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 55499
                           }
                     }, {
                           "keyword": "Then",
                           "name": "I should have 10 cucumbers",
                           "line": 5,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 46000
                           }
                     }
                  ]
               }, {
                  "keyword": "Scenario",
                  "id": "test_get_cucumbers_multiple_times",
                  "name": "Get cucumbers multiple times",
                  "line": 12,
                  "description": "",
                  "tags": [],
                  "type": "scenario",
                  "steps": [{
                           "keyword": "Given",
                           "name": "there are 5 cucumbers in the basket",
                           "line": 13,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 107100
                           }
                     }, {
                           "keyword": "When",
                           "name": "I get 1 cucumber from the basket",
                           "line": 14,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 53600
                           }
                     }, {
                           "keyword": "And",
                           "name": "I get 3 cucumbers from the basket",
                           "line": 15,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 48300
                           }
                     }, {
                           "keyword": "Then",
                           "name": "I should have 1 cucumbers in the basket",
                           "line": 16,
                           "match": {
                              "location": ""
                           },
                           "result": {
                              "status": "passed",
                              "duration": 46500
                           }
                     }
                  ]
               }
         ]
      }
   ]


Passing context across steps
-----------------------------------------

`Behave`_ framework uses generic catch-them-all context to maintain state across test steps. Many newcomers to the ``pytest`` and ``pytest-bdd`` world are wondering how to do the same with ``pytest-bdd``. Read further to find how.

.. warning:: Use context wisely and with caution

   Although passing context between steps is easy, genreally it should be considered code smell:

   - Increases coupling between steps
   - Makes dependencies implicit and obscure

   It is recommended to use explicit fixtures instead. Initialize necessary fixtures by ``given`` steps. Pass the fixtures further to other steps as explicit ``pytest`` fixtures.


``Pytest-bdd`` is a ``pytest`` plugin. This makes it possible to use ``pytest`` fixture to maintain state across test steps as context. Below is an example scenario and steps implementation which uses a dictionary as generic context to pass across steps.

.. code-block:: gherkin
   :caption: context.feature

   Feature: Context with pytest-bdd
      Scenario: Context is passed
         When I run a step which updates the context
         Then context is updated

.. code-block:: python
   :caption: test_context.py

   import pytest
   from pytest_bdd import scenarios, when, then

   scenarios("./context.feature")

   @pytest.fixture(scope="function")
   def ctx():
      yield {}

   @when("I run a step which updates the context")
   def when_update_context(ctx):
      ctx["updated"] = True

   @then("context is updated")
   def context_updated(ctx):
      assert "updated" in ctx
      assert ctx["updated"] is True

Further reading
----------------

- `Pytest-bdd documentation`_ is the ultimate reference when it comes to ``pytest-bdd``.
- Andrew Knight has created a great `Behavior Driven Python with pytest-bdd`_ course on Applitools's Test Automation University.

.. _`behave`: https://behave.readthedocs.io/en/stable/
.. _`Behavior Driven Python with pytest-bdd`: `pytest-bdd TAU course`_
.. _`examples source repository`: https://github.com/ivangeorgiev/python-refs/tree/main/src/python_refs/pytest_bdd
.. _`pytest-bdd`: `pytest-bdd source`_
.. _`pytest-bdd documentation`: https://pytest-bdd.readthedocs.io/en/latest/
.. _`pytest-bdd source`: https://github.com/pytest-dev/pytest-bdd
.. _`Test Automation University`: https://testautomationu.applitools.com/
.. _`pytest-bdd TAU course`: https://testautomationu.applitools.com/behavior-driven-python-with-pytest-bdd/
