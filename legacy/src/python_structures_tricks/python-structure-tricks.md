
## Keeping the last N items

```
>>> from collections import deque
>>> q = deque(maxlen=2)
>>> q.append(1)
>>> q.append(2)
>>> q.append(3)
>>> list(q)
[2, 3]

```

You can add or pop items from either end of the queue:

```python
>>> from collections import deque

# Create unbound queu
>>> q = deque()

# Append to the right
>>> q.append(1)
>>> q.append(2)
>>> q.append(3)
>>> list(q)
[1, 2, 3]

# Pop from the right
>>> q.pop()
3
>>> list(q)
[1, 2]

# Append to the left
>>> q.appendleft(4)
>>> list(q)
[4, 1, 2]

# Pop from the left
>>> q.popleft()
4
>>> list(q)
[1, 2]

```

Adding or popping items from either end of a queue has O(1) complexity. This is
unlike a list where inserting or removing items from the front of the list is O(N).


## Finding the Largest or Smallest N items in list

```python
>>> import heapq
>>> nums = [1, 8, 2, 23, 7, -4, 18, 23, 42,
...         37, 2]
>>> heapq.nlargest(3, nums)
[42, 37, 23]
>>> heapq.nsmallest(3, nums)
[-4, 1, 2]

```

Both functions accept `key` parameter so that you can place random objects.

The trick is that heapq first converts the data into a list where items are 
ordered as a heap.

```python
>>> import heapq
>>> nums = [1, 8, 2, 23, 7, -4, 18, 23, 42,
...         37, 2]
>>> heapq.heapify(nums)
>>> nums
[-4, 2, 1, 23, 7, 2, 18, 23, 42, 37, 8]

```

# heap[0] is always the smallest

```
>>> nums[0]
-4

```

`heapq.heappop` pops the first item and replaces with
the next smalest item. Operation is O(log N).

```python
>>> heapq.heappop(nums)
-4
>>> nums[0]
1

```

## Implement a Priority Queue

You want to implement a queue that maintains the items priority and
always returns the item with the highest priority.

```python
>>> import heapq

>>> class PriorityQueue(object):
...    def __init__(self):
...        self._queue = []
...        self._index = 0
...
...    def push(self, item, priority):
...        ### Adding self._index causes items with same priority
...        ### to be returned in the order they were added to the queue.
...        queue_item = (-priority, self._index, item)
...        heapq.heappush(self._queue, queue_item)
...        self._index += 1
...
...    def pop(self):
...        return heapq.heappop(self._queue)[-1]
...
>>> queue = PriorityQueue()
>>> queue.push('lorem', 1)
>>> queue.push('ipsum', 5)
>>> queue.push('dolorem', 4)
>>> queue.push('septum', 1)
>>> # Note - returns items in order of prioritoy.
>>> # Items with same priority are returned in the order they were added.
>>> (queue.pop(), queue.pop(), queue.pop(), queue.pop())
('ipsum', 'dolorem', 'lorem', 'septum')

```

