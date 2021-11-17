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
    def drop_representation_fields(self, representation):
        """Drop fields listed in Meta.drop_fields attribute from serializer representation"""
        fields = getattr(getattr(self, 'Meta', object()), 'drop_fields', tuple())
        for remove_field in fields:
            representation.pop(remove_field)
```

You could use the mix-in to remove (drop) fields from the serializer output:

```python
class UserSerializer(serializers.ModelSerializer, DropFieldsSerializerMixin):
    class Meta:
        model = User
        
  	def to_representation(self, instance):
        # Here you might have logic to determine which fields to be dropped
        self.Meta.drop_fields = ('salary',)
        # Drop fields defined in the Meta class drop_fields attribute
    	representation = super().to_representation(instance)
        self.drop_representation_fields(representation)
        return representation
```

In this approach fields that need to be removed are defined, using the Meta class. If a collection of field names is assigned to the Meta class drop_fields attribute, these fields will be removed from the output. 

You could use some logic during the object creation (`__init__` method), the `to_representation` method, etc.



