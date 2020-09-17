from collections import namedtuple
from enum import Enum

RuleInfo = namedtuple('RuleInfo', 'name,rule')
RuleErrorInfo = namedtuple('RuleErrorInfo', 'rule_name,row_id,error_type,error_text,row')

class ErrorAction(Enum):
    """No action. Error is logged, but the row is sent to the output."""
    NONE = 0
    """Row with at least one error is skipped from output"""
    SKIP = 1

class DataTransformer():
    def __init__(self):
        self.rules = []
        self._error_action = ErrorAction.SKIP
        self._id = None
        self._init()

    @property
    def num_errors(self):
        """Returns the number of errors logged by `apply` method.
        
        Note: Because one row might generate multiple errors, this
        number might be higher than the number of rows with error.
        """
        return len(self.errors)

    @property
    def num_output(self):
        """Returns the number of errors returned by `apply` method."""
        return len(self.output)

    @property
    def num_skipped(self):
        """Returns the number of rows skipped by `apply` method."""
        return len(self.skipped)

    def on_error(self, action):
        """Set error action."""
        self._error_action = action
        return self

    def _init(self):
        """Initialize the transformer before applying the transformations."""
        self.errors = []
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
        """Append row transformation.

        Row transformation is a function/callable which takes one argument - `row`
        and returns the transformed row.
        """
        rule = RuleInfo(name=name, rule=rule)
        self.rules.append(rule)
        return self
    
    def transform_field(self, field_name, rule, name=None):
        """Append field transformation.

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
        - `skipped` attribute contains a list of skipped (normally due to a transformation error)
        - `errors`  a list of error RuleErrorInfo objects for each transformation error

        """
        self._init()
        result = self.output
        for index, row in enumerate(dataset):
            self.num_input += 1
            transformed_row = dict(row)
            is_skip_row = False
            for rule_info in self.rules:
                try:
                    transformed_row = rule_info.rule(row)
                except Exception as exc:
                    is_skip_row = (self._error_action == ErrorAction.SKIP)
                    row_id = index if (self._id is None) else self._id(row) 
                    error_text = str(exc)
                    error = RuleErrorInfo(rule_name=rule_info.name,
                                          row_id=row_id,
                                          error_type=type(exc).__name__,
                                          error_text=error_text,
                                          row=row,
                                          )
                    self.errors.append(error)
            if is_skip_row:
                self.skipped.append(row)
            else:
                result.append(transformed_row)
        return result

