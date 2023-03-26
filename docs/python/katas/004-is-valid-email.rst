Is Valid Email Kata
=====================

Write a Python function that returns `True` or `False` to indicate whether the passed value
is a valid email address or not.


.. collapse:: Tests

   .. code-block:: python
      :caption: tests/test_is_email.py
      :linenos:

        import unittest
        import parameterized

        from ..validators import is_email

        class TestIsEmailFunction(unittest.TestCase):
            @parameterized.parameterized.expand([
                ('value is simple email address', 'example@example.com'),
                ('domian is a subdomain', 'example@subdomain.domain.com'),
                ('domain contains dashes', 'example@example-domain.com'),
                ('username contains digits', 'example123@example.com'),
            ])
            def test_should_return_true_when(self, name, value):
                self.assertTrue(is_email(value))

            @parameterized.parameterized.expand([
                ('domain is empty', 'example@'),
                ('host is empty', 'example@.com'),
                ('at character is missing', 'example.com'),
                ('domain ends with period', 'example@com.'),
                ('domain starts with period', 'example@.domain.com'),
                ('username is empty', '@domain.com'),
            ])
            def test_should_return_false_when(self, name, value):
                self.assertFalse(is_email(value))


.. collapse:: Solution 1

   .. code-block:: python
      :caption: validator.py
      :linenos:

      import re

      def is_email(value):
         pattern = r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$'

         regex = re.compile(pattern)
         match = regex.search(value)

         return bool(match)
