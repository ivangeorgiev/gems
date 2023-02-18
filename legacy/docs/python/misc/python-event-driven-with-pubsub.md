# Event-Driven Python with pubsub

## Simple Event Driven Python Example - Explained

To demonstrate the event-driven approach we will create a simplified ordering system in Python.

The workflow we are implementing takes following steps:
1. Order is placed by a customer
2. Order is created by persisting it to the database
3. Sales department receives a notfication about the new order

All the source for this example is available in [GitHub](https://github.com/ivangeorgiev/python-pubsub-example/blob/main/simple_pubsub.py).

Let's start by installing the `pypubsub` package:

```bash
$ pip install pypubsub
```

Our order is very simple - just a list items. Each item is represented by a string:

```python
items = ["100 inch TV", "magic carpet"]
```

To store the order we need a bit more complex strucure. We use a dictionary with two items: order id and order items. 
We are using `uuid4()` to generate unique order id.

```python
order = {
    "id": uuid4(),
    "items": ["100 inch TV", "magic carpet"]
}
```

As database we use Python dictionary. As dictionary key we use the order id:

```python
orders: Dict[UUID, dict] = {}
```

Saving an order to the database is as simple as adding a key to the `orders` dictionary.

```python
orders[order["id"]] = order
```

Our system uses `pubsub` to orchestrate messages with two topics:

```puthon
PLACE_ORDER_TOPIC = 'place-order'
ORDER_CREATED_TOPIC = 'order-created'
```

When an order is placed by a customer, we want to call a service function which takes care about
creating a new order object and storing it into the database. Once the order is created, an event
is triggered to notify other parts of the system:

```python
def place_order(items: List[str]):
    order = Order(items.copy())
    orders[order.id] = order
    pub.sendMessage(ORDER_CREATED_TOPIC, order_id=order.id)
```

We need to subscribe the `place_order` handler to the `PLACE_ORDER_TOPIC` command topic:

```python
pub.subscribe(place_order, PLACE_ORDER_TOPIC)
```

To notify the sales department about new orders, we are listening for events on the `ORDER_CREATED_TOPIC`:

```python
def notify_sales(message: str):
    print(message)

def order_created(order_id: UUID):
    order = orders[order_id]
    notify_sales(f"============\nNew Order:\n============\nID: {order['id']}\nItems: {order['items']}")

pub.subscribe(order_created, ORDER_CREATED_TOPIC)
```

Publishing a message to the `PLACE_ORDER_TOPIC` will kick our process:
- Trigger the `place_order` handler which will store the order and place a message to the `ORDER_CREATED_TOPIC`
- Trigger the `order_created` handler which will call the `notify_sales` service function


```python
pub.sendMessage(PLACE_ORDER_TOPIC, items=["100 inch TV", "magic carpet"])
```

This will produce following output:

```
============
New Order:
============
ID: aafc3ad9-417c-484b-8ed7-3960e7241ba8
Items: ['100 inch TV', 'magic carpet']
```

## Simple Event Driven Python Example - Full Code

Below is the full source code (file `simple_pubsub.py`) for our simple event-driven sales system in Python:

```python
from dataclasses import dataclass, field
from typing import Dict, List
from uuid import UUID, uuid4
from pubsub import pub

PLACE_ORDER_TOPIC = 'place-order'
ORDER_CREATED_TOPIC = 'order-created'

orders: Dict[UUID, 'Order'] = {}


def place_order(items: List[str]):
    order = Order(items.copy())
    orders[order.id] = order
    pub.sendMessage(ORDER_CREATED_TOPIC, order_id=order.id)

def notify_sales(message: str):
    print(message)

def order_created(order_id: UUID):
    order = orders[order_id]
    notify_sales(f"============\nNew Order:\n============\nID: {order.id}\nItems: {order.items}")

pub.subscribe(place_order, PLACE_ORDER_TOPIC)
pub.subscribe(order_created, ORDER_CREATED_TOPIC)

pub.sendMessage(PLACE_ORDER_TOPIC, items=["100 inch TV", "magic carpet"])
pub.sendMessage(PLACE_ORDER_TOPIC, items=["soft cheese", "dutch mashrooms"])
```

Running the `simple_pubsub.py` produces two notifications about placed orders:

```
============
New Order:
============
ID: aafc3ad9-417c-484b-8ed7-3960e7241ba8
Items: ['100 inch TV', 'magic carpet']
============
New Order:
============
ID: 6d9be0ec-6671-43d8-81c7-a2aa317d375c
Items: ['soft cheese', 'dutch mashrooms']
```

## Event Driven Python with pubsub - Advanced Example

The same scenario could be implemented by using more advanced and more flexible architecture.

You could find the full example in [github](https://github.com/ivangeorgiev/python-pubsub-example).

We define a `Messager` (`orders.message` module) class as base class for messages passed to pubsub. Further we define two sub-classes: `Event` (`orders.events` module) and `Command` (`orders.commands` module).

Following commands are defined:

- `PlaceOrder` create a new order
- `NotifySales` send a message to Sales department


For our application we define single `Event`:

- `OrderCreated` to be triggered once order is created

We also define handlers (`orders.handlers` module):

- `place_order` - handle the `PlaceOrder` command
- `notify_sales` - handle the `NotifySales` command
- `order_created` - handle the `OrderCreated` event

To provide persistence we also need a repository (`orders.repository` module). As storage layer we use the [TinyDB])(https://tinydb.readthedocs.io/) package to save
our orders in JSON file.

Everything is put together in the `advanced_pubsub.py` file:

```python
from pubsub import pub
from orders import commands, handlers, settings

pub.subscribe(handlers.place_order, settings.PLACE_ORDER_TOPIC)
pub.subscribe(handlers.order_created, settings.ORDER_CREATED_TOPIC)
pub.subscribe(handlers.notify_sales, settings.NOTIFY_SALES_TOPIC)

pub.sendMessage(settings.PLACE_ORDER_TOPIC, command=commands.PlaceOrder(items=["100 inch TV", "magic carpet"]))
pub.sendMessage(settings.PLACE_ORDER_TOPIC, command=commands.PlaceOrder(items=["soft cheese", "dutch mashrooms"]))
```

Here we register pubsub listeners and submit two `PlaceOrder` commands.

The output is the same as in the simple example:

```
============
New Order:
============
ID: 35f18675-7600-48ca-bf5d-48a303ab70fb
Items: ['100 inch TV', 'magic carpet']
============
New Order:
============
ID: b07794c7-21f7-4eea-b3a7-986f6098235f
Items: ['soft cheese', 'dutch mashrooms']
```

