FizzBuzz Kata
==============

Write a Python function that given a positive integer number, returns a string "Fizz"
if the number is multiply of three, "Buzz" if the number is multiply of five, "FizzBuzz"
if the number is multiple of three and five, the number otherwise.


.. collapse:: Tests

   .. code-block:: python
      :linenos:

      import pytest
      from fizbuzz import fizbuzz3 as fizbuzz


      @pytest.mark.parametrize("num", (1, 2))
      def test_should_return_n_if_number_is_not_divisible_by_3_and_5(num):
         assert str(num) == fizbuzz(num)


      @pytest.mark.parametrize("num", (3, 6))
      def test_should_return_Fizz_if_number_is_divisible_by_3(num):
         assert "Fizz" == fizbuzz(num)

      @pytest.mark.parametrize("num", (5, 10))
      def test_should_return_Buzz_if_number_is_divisible_by_5(num):
         assert "Buzz" == fizbuzz(num)

      @pytest.mark.parametrize("num", (15, 30))
      def test_should_return_FizzBuzz_if_number_is_divisible_by_3_and_by_5(num):
         assert "FizzBuzz" == fizbuzz(num)


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
