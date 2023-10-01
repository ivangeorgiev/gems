Custom Sequential Number Django Model Field
##############################################################

.. post:: 2023-10-01 12:40:00
   :tags: django,sql database,core,orm
   :category: django
   :author: ivan
   :language: en

Sometimes we need certain functionality again, and again, and again,... Sometimes it just makes sense to
encapsulate certain logic into a separate module so it is easier to test and maintan. For example, we might need
Django model field that is capable of keeping seqential number of the items in the order they are stored in the database.

Requirements
*************************

* If value for the field is assigned, do not change it
* The sequence is defined through database key - *sequence key*
* The *sequence key* could be composite
* The *sequence key* could be global (empty)
* If value is not assigned, get the highest used value from the sequence + increment
* If value is not assigned and sequence is empty use initial value

.. warning::
   Not concurrency-safe.

Custom Django model field
**********************************

Following is the source for the sequence number custom Django model field.

.. literalinclude:: assets/sequential_number_field.py
   :caption: sequential_number_field.py
   :linenos:

Object initializer stores the sequence key, the sequence initial value (*start_at*) at the sequence *increment*.

The `pre_save` method is called by Django before persisting the model instance into the database.
We override this method so that if no value is assigned to the attribute, a new value is generated and
assigned. If value is already assigned, the default Django implementation from the parent class is called.

For clean code considerations I split the `pre_save` int small self-contained methods. If we follow the
all-in-one approach and inline all the methods, the `pre_save` could look like:

.. code-block:: python
   :caption: inlined version of the `pre_save` method
   :linenos:

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self._get_queryset()
                if self.key:
                    query = {field: getattr(model_instance, field) for field in self.key}
                    qs = qs.filter(**query)
                highest_item = qs.latest(self.attname)
                highest_value = getattr(highest_item, self.attname)
                value = highest_value + self.increment
            except ObjectDoesNotExist:
                value = self.start_at
            setattr(model_instance, self.attname, value)
            return value
        return super().pre_save(model_instance, add)

In this case the inlined version of the code is still readable so it might make sense using it. However from
testability perspective, it is not that easy to unit test the method as for each unit test it would require quite some
mocking and patching.

I would rather prefer something in-between:

.. code-block:: python
   :caption: structured version of the `pre_save` method
   :linenos:

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self._get_queryset_for(model_instance)
                highest_item = qs.latest(self.attname)
                highest_value = getattr(highest_item, self.attname)
                value = highest_value + self.increment
            except ObjectDoesNotExist:
                value = self.start_at
            setattr(model_instance, self.attname, value)
            return value
        return super().pre_save(model_instance, add)

    def _get_queryset_for(self, model_instance: Model) -> models.QuerySet:
        qs = self.model.objects.all()
        if self.key:
            query = {field: getattr(model_instance, field) for field in self.key}
            qs = qs.filter(**query)
        return qs

Once you have good tests in place, you could experiment with implementation that suits your preferences. In our case
I created tests which evaluate the behavior of the `SequentialNumberField` instances through the public interface.
This allows me for experimenting with different implementations while still using the same tests. Since I am not
testing methods in isolation, this is known as the *testing trophy* (as oppiosed to the *testing pyramid*).

For the sake of fun I asked ChatGPT to restructure my code to follow better the Single Responsibility Principle (SRP). Here is what it came with:

.. code-block:: python
   :caption: `pre_save` method with SRP in mind - ChatGPT version
   :linenos:

   class SequentialNumberField(models.PositiveIntegerField):
      # ... (constructor remains the same)

      def pre_save(self, model_instance: Model, add: bool) -> Any:
         if getattr(model_instance, self.attname) is None:
               value = self._generate_sequential_number(model_instance)
               setattr(model_instance, self.attname, value)
               return value
         return super().pre_save(model_instance, add)

      def _generate_sequential_number(self, model_instance: Model) -> int:
         try:
               highest_value = self._get_highest_value(model_instance)
               return highest_value + self.increment
         except ObjectDoesNotExist:
               return self.start_at

      def _get_highest_value(self, model_instance: Model) -> int:
         qs = self._get_queryset(model_instance)
         highest_item = qs.latest(self.attname)
         return getattr(highest_item, self.attname)

      def _get_queryset(self, model_instance: Model) -> models.QuerySet:
         qs = model_instance.__class__.objects.all()
         if self.key:
               query = {field: getattr(model_instance, field) for field in self.key}
               qs = qs.filter(**query)
         return qs


Pytest tests for our SequentialNumberField custom Django model field
*********************************************************************

Here is a sample implementation for pytest tests that verify the implementation matches the requirements.

.. literalinclude:: assets/test_sequential_number_field.py
   :caption: test_sequential_number_field.py
   :linenos:

