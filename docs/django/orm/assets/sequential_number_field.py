from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Model


class SequentialNumberField(models.PositiveIntegerField):
    def __init__(self, key=None, start_at=1, increment=1, *args, **kwargs):
        """
        Initializes a SequentialNumberField.

        Args:
            key (list of str, optional): A list of field names to use as keys for sequential number grouping.
                If specified, the sequential number will be unique within the group specified by the key.
                Defaults to None.
            start_at (int, optional): The initial value for the sequence. Defaults to 1.
            increment (int, optional): The increment value for the sequence. Defaults to 1.
        """
        if isinstance(key, str):
            self.key = [key]
        else:
            self.key = key
        self.start_at = start_at
        self.increment = increment
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance: Model, add: bool) -> Any:
        """
        Pre-save method to generate and assign the sequential number.

        Args:
            model_instance (Model): The model instance being saved.
            add (bool): True if the model instance is being added, False if it's being updated.

        Returns:
            int: The generated sequential number.
        """
        if getattr(model_instance, self.attname) is None:
            value = self._generate_value(model_instance)
            setattr(model_instance, self.attname, value)
            return value
        return super().pre_save(model_instance, add)

    def _generate_value(self, model_instance: Model) -> Any:
        try:
            query = self._get_filter_query(model_instance)
            highest = self._find_highest_used_value(query)
            value = highest + self.increment
        except ObjectDoesNotExist:
            value = self.start_at
        return value

    def _get_filter_query(self, model_instance: Model) -> dict:
        if self.key:
            query = {field: getattr(model_instance, field) for field in self.key}
            return query
        return {}

    def _find_highest_used_value(self, query: dict):
        qs = self._get_queryset().filter(**query)
        last_item = qs.latest(self.attname)
        return getattr(last_item, self.attname)

    def _get_queryset(self):
        return self.model.objects.all()
