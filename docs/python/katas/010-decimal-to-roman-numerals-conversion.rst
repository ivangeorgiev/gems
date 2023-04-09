Decimal to Roman Numeral Conversion
===================================

Roman Numerals
--------------

Roman numerals are a numeral system that originated in ancient Rome and were used throughout the Roman Empire. They consist of a combination of letters from the Latin alphabet, which are used to represent different values. The Roman numeral system has no symbol for zero, and it is not a positional system like the decimal system we use today.

There are seven basic symbols used in the Roman numeral system:

- I: represents the value 1
- V: represents the value 5
- X: represents the value 10
- L: represents the value 50
- C: represents the value 100
- D: represents the value 500
- M: represents the value 1000

These symbols can be combined in various ways to represent larger values. For example:

- II: represents the value 2
- III: represents the value 3
- IV: represents the value 4
- VI: represents the value 6
- IX: represents the value 9
- XI: represents the value 11
- XIV: represents the value 14
- XX: represents the value 20
- XL: represents the value 40
- LXX: represents the value 70
- XC: represents the value 90
- CXX: represents the value 120
- CD: represents the value 400
- DCC: represents the value 700
- CM: represents the value 900

Above example shows that some numerals are written using "subtractive notation", e.g. for 4 (IV) and 9 (IX), where the first symbol (I) is subtracted from the larger one (V, or X),
thus avoiding the clumsier IIII and VIIII. Subtractive notation is also used for 40 (XL), 90 (XC), 400 (CD) and 900 (CM). These are the only subtractive forms in standard use.

Roman numerals are often used today in situations where a more traditional or formal style is desired, such as in the numbering of book chapters or movie sequels. They are also used in clock faces, and in the names of monarchs and popes.

For more details see `Roman Numerals <https://en.wikipedia.org/wiki/Roman_numerals>`_ at Wikipedia.

Task
----

Create a `decimal_to_roman` function which given an integer number returns its representation as roman numeral.

Implementation Notes
--------------------

.. collapse:: Test Cases

   .. code-block:: python
      :linenos:

      import unittest
      from parameterized import parameterized

      class TestConvertFunction(unittest.TestCase):

         @parameterized.expand([
            ("1", 1, "I"),
            ("2", 2, "II"),
            ("3", 3, "III"),
            ("4", 4, "IV"),
            ("5", 5, "V"),
            ("6", 6, "VI"),
            ("8", 8, "VIII"),
            ("9", 9, "IX"),
            ("10", 10, "X"),
            ("11", 11, "XI"),
            ("19", 19, "XIX"),
            ("20", 20, "XX"),
            ("39", 39, "XXXIX"),
            ("40", 40, "XL"),
            ("41", 41, "XLI"),
            ("49", 49, "XLIX"),
            ("50", 50, "L"),
            ("90", 90, "XC"),
            ("95", 95, "XCV"),
            ("100", 100, "C"),
            ("400", 400, "CD"),
            ("500", 500, "D"),
            ("900", 900, "CM"),
            ("1000", 1000, "M"),
            ("Spanish flu", 1918, "MCMXVIII"),
            ("2023", 2023, 'MMXXIII')
         ])
         def test_convert(self, name, num, expected_result):
            result = decimal_to_roman(num)
            self.assertEqual(result, expected_result)



.. collapse:: Solution 1

   .. code-block:: python
      :linenos:

      def decimal_to_roman(num):
         roman = ''
         number_map = (
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, 'X'),
            (9, 'IX'),
            (5, 'V'),
            (4, 'IV'),
            (1, 'I'),
         )
         for arabic_num, roman_num in number_map:
            while num >= arabic_num:
                  roman += roman_num
                  num -= arabic_num
         return roman
