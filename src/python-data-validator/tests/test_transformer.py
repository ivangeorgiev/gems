import unittest

# For compatibility with Databricks notebook mode
if 'DataTransformer' not in globals().keys():
    from transform.transformer import DataTransformer, ErrorAction, RuleErrorInfo

class TestDataTransformer(unittest.TestCase):
    def test_execute_Transformer_class_returns_instance(self):
        transformer = DataTransformer()
        self.assertIsInstance(transformer, DataTransformer)

    
    def test_apply_with_no_rules_returns_same_dataset(self):
        data = [ {'id': 1}, {'id': 2}]
        transformer = DataTransformer()
        result = transformer.apply(data)
        assert data == result
        assert [] == transformer.errors
        assert 0 == transformer.num_errors

    def test_apply_with_rules_applies_rules(self):
        def upper(row):
            row['name'] = row['name'].upper()
            return row
        data = [ {'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 1, 'name': 'JOHN'}, {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().transform(upper)

        result = transformer.apply(data)
        assert expect == result
        assert [] == transformer.errors
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
        expect_errors = [RuleErrorInfo(rule_name='upper-name',
                                       row_id=0,
                                       row={'id': 1, 'name': 'Long John'},
                                       error_type=ValueError.__name__,
                                       error_text="'name' length exceeds 5 characters")]
        self.assertEqual(expect_errors, transformer.errors)
        expect_num_errors = 1
        actual_num_errors = transformer.num_errors
        assert expect_num_errors == actual_num_errors

    def test_apply_with_error_action_NONE(self):
        def upper(row):
            name_len = len(row['name'])
            if name_len > 5:
                raise ValueError("'name' length exceeds 5 characters")
            row['name'] = row['name'].upper()
            return row

        data = [ {'id': 1, 'name': 'Long John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 1, 'name': 'Long John'}, {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().on_error(ErrorAction.NONE).transform(upper, 'upper-name')

        result = transformer.apply(data)
        assert expect == result
        expect_errors = [RuleErrorInfo(rule_name='upper-name',
                                       row_id=0,
                                       row={'id': 1, 'name': 'Long John'},
                                       error_type=ValueError.__name__,
                                       error_text="'name' length exceeds 5 characters")]
        assert expect_errors == transformer.errors


    def test_apply_with_error_logs_row_id_from_named_column(self):
        def upper(row):
            name_len = len(row['name'])
            if name_len > 5:
                raise ValueError("'name' length exceeds 5 characters")
            row['name'] = row['name'].upper()
            return row

        data = [ {'id': 1, 'name': 'Long John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 1, 'name': 'Long John'}, {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().id('id').on_error(ErrorAction.NONE).transform(upper, 'upper-name')

        result = transformer.apply(data)
        assert expect == result
        expect_errors = [RuleErrorInfo(rule_name='upper-name',
                                       row_id=1,
                                       row={'id': 1, 'name': 'Long John'},
                                       error_type=ValueError.__name__,
                                       error_text="'name' length exceeds 5 characters")]
        assert expect_errors == transformer.errors

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
        expect = [ {'id': 1, 'name': 'Long John'}, {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().id(id_getter).on_error(ErrorAction.NONE).transform(upper, 'upper-name')

        result = transformer.apply(data)
        assert expect == result
        expect_errors = [RuleErrorInfo(rule_name='upper-name',
                                       row_id='1|Long John',
                                       row={'id': 1, 'name': 'Long John'},
                                       error_type=ValueError.__name__,
                                       error_text="'name' length exceeds 5 characters")]
        assert expect_errors == transformer.errors


    def test_apply_with_field_transform(self):
        data = [ {'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
        expect = [ {'id': 1, 'name': 'JOHN'}, {'id': 2, 'name': 'JANE'}]

        transformer = DataTransformer().transform_field('name', lambda f: f.upper())

        result = transformer.apply(data)
        assert expect == result
