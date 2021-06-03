import unittest
import pytest
from transform.transformations import *

class TestDataTransformer(unittest.TestCase):
    def test_select_with_multiple_fields(self):
        input = dict(id=1,name='John',age=65)
        selector = select('id,name')
        result = selector(input)
        expect = dict(id=1,name='John')
        self.assertEqual(expect, result)

