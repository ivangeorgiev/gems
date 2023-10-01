import pytest
from tests.fake_app import models

from iris.fields import SequentialNumberField


class TestSequentialNumberField:
    def test_can_create_instance(self):
        f = SequentialNumberField()

    def test_can_specify_field_name_as_key(self):
        f = SequentialNumberField(key="field")
        assert f.key == ["field"]

    def test_can_specify_no_key(self):
        f = SequentialNumberField()
        assert f.key is None

    def test_can_specify_composite_key(self):
        f = SequentialNumberField(["field1", "field2"])
        assert f.key == ["field1", "field2"]

    @pytest.mark.django_db
    def test_should_use_assigned_value(self, order):
        item = models.OrderItem.objects.create(
            order=order,
            sequential_number=101,
        )
        item.refresh_from_db
        assert item.sequential_number == 101

    @pytest.mark.django_db
    def test_should_use_start_at_as_first_sequence_number(self, order):
        item = models.OrderItem.objects.create(
            order=order,
        )
        item.refresh_from_db
        assert item.sequential_number == 11

    @pytest.mark.django_db
    def test_should_use_max_existing_sequenc_number_incremented_with_increment(self, order, order_item):
        item = models.OrderItem.objects.create(
            order=order,
        )
        item.refresh_from_db
        expected_sequential_number = (
            order_item.sequential_number + models.OrderItem._meta.get_field("sequential_number").increment
        )
        assert item.sequential_number == expected_sequential_number


@pytest.fixture(name="order")
def given_order():
    order = models.Order.objects.create()
    yield order


@pytest.fixture(name="order_item")
def given_order_item(order):
    item = models.OrderItem.objects.create(
        order=order,
        sequential_number=5,
    )
    return item
