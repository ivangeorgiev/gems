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
      :linenos:

      def fizbuzz1(n):
         if n % 3 == 0 and n % 5 == 0:
            return "FizzBuzz"
         if n % 3 == 0:
            return "Fizz"
         if n % 5 == 0:
            return "Buzz"
         return str(n)

.. collapse:: Solution 2

   .. code-block:: python
      :linenos:

      def fizbuzz2(n):
         divisors = ( (15, "FizzBuzz"), (3, "Fizz"), (5, "Buzz") )
         for divisor, result in divisors:
            if n % divisor == 0:
                  return result
         return str(n)

.. collapse:: Solution 3

   .. code-block:: python
      :linenos:

      from functools import reduce

      def fizbuzz3(n):
         divisors = ( (3, "Fizz"), (5, "Buzz") )
         result = ""
         for divisor, word in divisors:
            if n % divisor == 0:
                  result = result + word
         if result == "":
            result = str(n)
         return result


.. collapse:: Solution 4

   .. code-block:: python
      :linenos:

      def fizbuzz4(n):
         divisors = ( (3, "Fizz"), (5, "Buzz") )
         result = "".join(word for divisor, word in divisors if n % divisor == 0)
         return result or str(n)
