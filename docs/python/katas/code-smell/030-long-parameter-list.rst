Long Parameter List
=========================================

Given following class `Order`:

.. code-block:: python

   class Order:
      _id: str
      _customer_id: str
      _customer_address: str
      _has_priority: bool
      _product_ids: list[str]

      def __init__(
         self,
         id: str,
         customer_id: str,
         customer_address: str,
         product_ids: list[str],
         is_premium_customer: bool,
      ) -> None:
         self._id = id
         self._customer_id = customer_id
         self._customer_address = customer_address
         self._product_ids = product_ids.copy()
         self._has_priority = is_premium_customer

      def get_product_ids(self):
         return self._product_ids

      def get_customer_id(self) -> str:
         return self._customer_id


Issues
------------

Make `id` parameter optional
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This would require moving the parameter to the end breaking all client code.

Knowing too much
~~~~~~~~~~~~~~~~~~

Initializer receives a set of arguments which characterize customer.
What if we need to add another customer attribute?

This would break all client code.

Parameter order
~~~~~~~~~~~~~~~~~~~

Because the list of parameters is more than 2-3, it is very likely the client code
to pass parameters in wrong order.

.. collapse:: Solution 1

   One possible approach is to make all parameters keyword parameters, by specifying asterisk
   '*' after the `self` parameter. This will force the client code to always pass keyword arguments.

   Further to address the knowledge about customer we create a Customer class and replace all
   customer-related parameters with a single parameter `customer`.

   .. code-block:: python
      :linenos:

      from dataclasses import dataclass
      from uuid import uuid4

      @dataclass
      class Customer:
         id: str
         address: str
         has_premium_subscription: bool = False

      class Order:
         _id: str
         _customer: Customer
         _product_ids: list[str]

         def __init__(
            self,
            *,
            customer: Customer,
            product_ids: list[str],
            id: str = None
         ) -> None:
            self._id = id | uuid4()
            self._customer = customer
            self._product_ids = product_ids.copy()

         def get_product_ids(self):
            return self._product_ids

         def get_customer_id(self) -> str:
            return self._customer_id


