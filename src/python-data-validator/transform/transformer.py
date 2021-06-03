from collections import namedtuple
from enum import Enum

RuleInfo = namedtuple('RuleInfo', 'name,rule')
RuleErrorInfo = namedtuple('RuleErrorInfo', 'rule_name,error_type,error_text')
SkipRowInfo = namedtuple('SkipRowInfo', 'row_id,reason,errors,row')

class SkipReason(Enum):
    ERROR = 'ERROR'

class DataTransformer():
    def __init__(self):
        self.rules = []
        self._id = None
        self._init()

    @property
    def num_skipped(self):
        """Returns the number of rows skipped by the `apply` method.
        """
        return len(self.skipped)

    @property
    def errored(self):
        """Returns a list of SkipRowInfo objects for each row with `apply` error.
        """
        return [skip_info for skip_info in self.skipped if skip_info.reason==SkipReason.ERROR]

    @property
    def num_errored(self):
        """Returns the number of rows with `apply` error.
        """
        return len(self.errored)

    @property
    def num_errors(self):
        """Returns the total number of errors during `apply`.
        """
        return sum(map(lambda skip_info: len(skip_info.errors), self.skipped))

    @property
    def num_output(self):
        """Returns the number of errors returned by `apply` method."""
        return len(self.output)


    def _init(self):
        """Initialize the transformer before applying the transformations."""
        self.skipped = []
        self.output = []
        self.num_input = 0

    def id(self, getter):
        """Set the row identifier.

        This `getter` can be:
           - string - the `getter` designates a field name to be used as row identifier.
           - callable - the `getter` designates a function/callable that retruns the 
                        row identifier. The function signature is `getter(row)->id`
        """
        if callable(getter):
            self._id = getter
        else:
            self._id = lambda row: row[getter]
        return self

    def transform(self, rule, name=None):
        """Append a row transformation.

        Row transformation is a function/callable which takes one argument - `row`
        and returns the transformed row.
        """
        rule = RuleInfo(name=name, rule=rule)
        self.rules.append(rule)
        return self
    
    def transform_field(self, field_name, rule, name=None):
        """Append a field transformation.

        Field transformation is a function/callable which takes one argument - `value` - 
        the value of the input field with name `field_name` and returns the new value for that field.
        """ 
        def field_transformer(row):
            row[field_name] = rule(row[field_name])
            return row
        return self.transform(field_transformer, name)


    def apply(self, dataset):
        """Apply all defined transformations to an iterable `dataset`.

        Parameters
        ----------
           :dataset:iterable: a collection or other iterable holidng input rows.
                              Each row is a dictionary-like object (`dict()` is used to clone rows).

        Retruns
        -------
           :list: A list of transformed rows. Each row is a dictionary.

        Transformations are applied in the order they are registered.
        
        Side Effects
        ------------
        - `num_input` attribute contains the number of input rows processed by `apply` method
        - `output` same as the return result of the `apply` method
        - `skipped` attribute contains a list of SkipRowInfo for each skipped rows

        """
        self._init()
        result = self.output
        for index, row in enumerate(dataset):
            self.num_input += 1
            transformed_row = dict(row)
            row_errors = []
            for rule_info in self.rules:
                try:
                    transformed_row = rule_info.rule(transformed_row)
                except Exception as exc:
                    error_text = str(exc)
                    error = RuleErrorInfo(rule_name=rule_info.name,
                                          error_type=type(exc).__name__,
                                          error_text=error_text,
                                          )
                    row_errors.append(error)
            if row_errors:
                row_id = index if (self._id is None) else self._id(row)
                skip_info = SkipRowInfo(row_id=row_id,
                                        reason=SkipReason.ERROR,
                                        errors=row_errors,
                                        row=row)
                self.skipped.append(skip_info)
            else:
                result.append(transformed_row)
        return result

