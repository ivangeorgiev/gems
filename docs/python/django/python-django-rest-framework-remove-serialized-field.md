# Remove Field from Django Rest Framework Serializer Output

## Problem

We need to remove a field from Django Rest Framework serializer output. There could be many reasons for this. For example:

* Authorization - user is not authorized to see certain data.
* Feature toggle - we want certain feature to be available based on a feature flag (toggle)

## Solution

Override the default `to_representation` method to drop the field from the output:

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

  	def to_representation(self, instance):
    	representation = super().to_representation(instance)
        representation.pop('salary')
        return representation
```



## Discussion

To make the solution more reusable, you could create a mix-in class:

```python
class DropFieldsSerializerMixin:
    def drop_representation_fields(self, representation:dict, fields):
        """Drop a one or more fields from serializer representation"""
        fields = (fields,) if type(fields) == str else fields
        for remove_field in fields:
            representation.pop(remove_field)
```

You could use the mix-in to remove (drop) fields from the serializer output:

```python
class UserSerializer(serializers.ModelSerializer, DropFieldsSerializerMixin):
  	def to_representation(self, instance):
    	representation = super().to_representation(instance)
        self.drop_representation_fields(representation, 'salary')
        return representation
```

A unit test (pytest) to test our drop serializer field mix-in might look like:

```python
from mylib.django.restframework import serializers

class MySerializer(serializers.DropFieldsSerializerMixin):
    pass

def test_drop_representation_fields_removes_single_field():
    data = dict(city='Sofia', name='John Doe', salary=1e6)
    expected = dict(city='Sofia', name='John Doe')

    serializer = MySerializer()
    serializer.drop_representation_fields(data, 'salary')

    assert data == expected

def test_drop_representation_fields_removes_multiple_field():
    data = dict(city='Sofia', name='John Doe', salary=1e6)
    expected = dict(name='John Doe')

    serializer = MySerializer()
    serializer.drop_representation_fields(data, ('salary', 'city'))

    assert data == expected
```

You could add further test cases to verify scenarios like "raises keyerror when trying to drop missing field". Or you might decide to silently ignore missing fields and handle the KeyError exception in the mix-in class and implement test scenario "silently ignores missing field".