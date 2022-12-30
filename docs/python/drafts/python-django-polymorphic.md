

```python
import uuid
from django.db import models

from techmeta import settings

class DatasetDeliveryModel(models.Model):
    dataset_delivery_id = models.UUIDField(primary_key=True, db_index=True, unique=True, default=uuid.uuid4)
    type_name = models.CharField(max_length=255)
    delivery_schedule_id = models.UUIDField(unique=True)
    physical_dataset_id = models.UUIDField(unique=True)
    flat_file_id = models.BigIntegerField(db_index=True, unique=True, null=True)

    class Meta:
        db_table = f"{settings.TABLENAME_PREFIX}Dataset_Delivery"
        app_label = settings.DJANGO_APP_LABEL
```







```python
from __future__ import annotations
import dataclasses
import inspect

import uuid

from .delivery_schedule import DeliveryScheduleId
from .flat_file import FlatFileId
from .physical_dataset import PhysicalDatasetId

DatasetDeliveryId = uuid.UUID


class DatasetDeliveryFactory:
    dataset_delivery_types: dict[str, type] = {}

    @classmethod
    def create_dataset_delivery(cls, type_name, **attributes) -> DatasetDelivery:
        klass = cls.dataset_delivery_types[type_name]
        return klass.create(**attributes)

    @classmethod
    def register(cls, klass):
        cls.dataset_delivery_types[klass.type_name()] = klass


@dataclasses.dataclass(frozen=True)
class DatasetDelivery:
    """Abstract Physical Dataset Delivery"""

    dataset_delivery_id: DatasetDeliveryId
    delivery_schedule_id: DeliveryScheduleId
    physical_dataset_id: PhysicalDatasetId
    flat_file_id: FlatFileId

    @classmethod
    def type_name(cls):
        return cls.__qualname__

    @classmethod
    def create(cls, **kwargs) -> DatasetDelivery:
        """Create instance from attributes, ignoring unknown attributes."""
        return cls(
            **{
                k: v
                for k, v in kwargs.items()
                if k in inspect.signature(cls).parameters
            }
        )

    @property
    def attributes(self) -> dict:
        return dataclasses.asdict(self)

    def __init_subclass__(cls) -> None:
        DatasetDeliveryFactory.register(cls)


```



```python

from django.forms.models import model_to_dict

from ..exceptions import DoesNotExist
from ..models import DatasetDeliveryModel
from ..strings import ERR_DATASET_DELIVERY_DOESNT_EXIST, ERR_DATASET_DELIVERY_FOR_FLAT_FILE_DOESNT_EXIST
from techmeta.persistence.repository import DatasetDeliveryRepository
from techmeta.domain import DatasetDelivery, DatasetDeliveryFactory, DatasetDeliveryId
from techmeta.legacy.flat_file.domain import FlatFileId


class DatasetDeliveryDjangoRepository(DatasetDeliveryRepository):
    def get(self, dataset_delivery_id: DatasetDeliveryId) -> DatasetDelivery:
        try:
            dataset_delivery_model = DatasetDeliveryModel.objects.get(pk=dataset_delivery_id)
            dataset_delivery_attributes = model_to_dict(dataset_delivery_model)
            dataset_delivery_attributes.pop("type_name")

            dataset_delivery = DatasetDeliveryFactory.create_dataset_delivery(dataset_delivery_model.type_name, **dataset_delivery_attributes)
            return dataset_delivery
        except DatasetDeliveryModel.DoesNotExist:
            raise DoesNotExist(
                ERR_DATASET_DELIVERY_DOESNT_EXIST.format(dataset_delivery_id=dataset_delivery_id)
            )

    def find_flat_file(self, flat_file_id: FlatFileId):
        try:
            dataset_delivery_model = DatasetDeliveryModel.objects.get(flat_file_id=flat_file_id)
            dataset_delivery_attributes = model_to_dict(dataset_delivery_model)
            dataset_delivery_attributes.pop("type_name")

            dataset_delivery = DatasetDeliveryFactory.create_dataset_delivery(dataset_delivery_model.type_name, **dataset_delivery_attributes)
            return dataset_delivery
        except DatasetDeliveryModel.DoesNotExist:
            raise DoesNotExist(
                ERR_DATASET_DELIVERY_FOR_FLAT_FILE_DOESNT_EXIST.format(flat_file_id=flat_file_id)
            )

```

