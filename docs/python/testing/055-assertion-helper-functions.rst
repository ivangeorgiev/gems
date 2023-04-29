Assertion Helper Functions
============================

Here is a assertion helper function example. The `__tracebackhide__ = True` line
instructs pytest to not include traceback for the assertion helper function.

.. code-block:: python

   def assert_something():
      __tracebackhide__ = True
      pytest.fail("I like failing")

And a very simple test wchich uses our assertion helper function.

.. code-block:: python

   def test_me()
      assert_something()

Executing the test:

.. code-block::

   ~/DjangoPytest$ python -m pytest
   ================ test session starts ================
   platform linux -- Python 3.8.12, pytest-7.3.1, pluggy-0.13.1
   rootdir: /home/runner/DjangoPytest
   collected 1 item

   tests/test_me.py F                            [100%]

   ===================== FAILURES ======================
   ______________________ test_me ______________________

      def test_me():
   >       assert_something()
   E       Failed: I like failing

   tests/test_me.py:10: Failed
   ============== short test summary info ==============
   FAILED tests/test_me.py::test_me - Failed: I like failing
   ================= 1 failed in 0.11s =================

