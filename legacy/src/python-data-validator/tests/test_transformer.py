import unittest
import pytest

# For compatibility with Databricks notebook mode
if 'DataTransformer' not in globals().keys():
    from transform.transformer import DataTransformer, SkipRowInfo,RuleErrorInfo, SkipReason

class TestDataTransformer(unittest.TestCase):
    def test_execute_Transformer_class_returns_instance(self):
        transformer = DataTransformer()
        self.assertIsInstance(transformer, DataTransformer)

    
    def test_apply_with_no_rules_returns_same_dataset(self):
        data = [ {'id': 1}, {'id': 2}]
        transformer = DataTransformer()
        result = transformer.apply(data)
        assert data == result
        assert [] == transformer.skipped

    def test_apply_with_rules_applies_rules(self):
        def upper(row):
            row['name'] = row['name'].upper()
            return row
        data = [ {'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 1, 'name': 'JOHN'}, {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().transform(upper)

        result = transformer.apply(data)
        assert expect == result
        assert [] == transformer.skipped
        assert 0 == transformer.num_skipped
        assert 0 == transformer.num_errors

    def test_apply_with_rules_applies_rules_and_errors(self):
        def upper(row):
            name_len = len(row['name'])
            if name_len > 5:
                raise ValueError("'name' length exceeds 5 characters")
            row['name'] = row['name'].upper()
            return row

        data = [ {'id': 1, 'name': 'Long John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().transform(upper, 'upper-name')

        result = transformer.apply(data)
        assert expect == result
        expect_error_info = RuleErrorInfo(rule_name='upper-name',
                                       error_type=ValueError.__name__,
                                       error_text="'name' length exceeds 5 characters")
        expect_skip = [SkipRowInfo(row_id=0,
                                   reason=SkipReason.ERROR,
                                   errors=[expect_error_info],
                                   row={'id': 1, 'name': 'Long John'})]
        self.assertEqual(expect_skip, transformer.skipped)
        self.assertEqual(1, transformer.num_errors)
        self.assertEqual(expect_skip, transformer.errored)

    def test_apply_with_error_logs_row_id_from_named_column(self):
        def upper(row):
            name_len = len(row['name'])
            if name_len > 5:
                raise ValueError("'name' length exceeds 5 characters")
            row['name'] = row['name'].upper()
            return row

        data = [ {'id': 1, 'name': 'Long John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().id('id').transform(upper, 'upper-name')

        result = transformer.apply(data)
        assert expect == result
        expect_error_info = RuleErrorInfo(rule_name='upper-name',
                                       error_type=ValueError.__name__,
                                       error_text="'name' length exceeds 5 characters")
        expect_skip = [SkipRowInfo(row_id=1,
                                   reason=SkipReason.ERROR,
                                   errors=[expect_error_info],
                                   row={'id': 1, 'name': 'Long John'})]
        self.assertEqual(expect_skip, transformer.skipped)


    def test_apply_with_error_logs_row_id_from_getter(self):
        def upper(row):
            name_len = len(row['name'])
            if name_len > 5:
                raise ValueError("'name' length exceeds 5 characters")
            row['name'] = row['name'].upper()
            return row

        def id_getter(row):
            return '{}|{}'.format(row['id'], row['name'])

        data = [ {'id': 1, 'name': 'Long John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().id(id_getter).transform(upper, 'upper-name')

        result = transformer.apply(data)
        assert expect == result
        expect_error_info = RuleErrorInfo(rule_name='upper-name',
                                       error_type=ValueError.__name__,
                                       error_text="'name' length exceeds 5 characters")
        expect_skip = [SkipRowInfo(row_id='1|Long John',
                                   reason=SkipReason.ERROR,
                                   errors=[expect_error_info],
                                   row={'id': 1, 'name': 'Long John'})]
        self.assertEqual(expect_skip, transformer.skipped)



    def test_apply_with_field_transform(self):
        data = [ {'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 1, 'name': 'JOHN'}, {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().transform_field('name', lambda f: f.upper())

        result = transformer.apply(data)
        self.assertEqual(expect, result)


    def test_apply_with_changing_transform(self):
        def select(row):
            return dict(id=row['id'], name=row['name'])

        data = [ {'id': 1, 'name': 'John', 'age':65}, {'id': 2, 'name': 'Jane', 'age':43}]
        expect = [ {'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]

        transformer = DataTransformer().transform(select, 'select')

        result = transformer.apply(data)
        self.assertEqual(expect, result)
