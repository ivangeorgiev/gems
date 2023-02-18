---
created: 2020-09-03 10:22:00
tags: python,kata,object oriented,oop
---

# Python Kata #4: Hello Mars!

Me and my friends like to travel to other planets. To keep track on which planets we visited I created a Python `VisitTracker` class. 

```python
class VisitTracker:
  visited = []

  def __init__(self, name):
    self.name = name

  def visit(self, place):
    if place not in self.visited:
      self.visited.append(place)

  def list(self):
    print("====== " + self.name + "'s visits ======")
    print(self.visited)
```

I put all the Python source code in an Jupyter Notebook (I made it available for you as [GitHub gist](https://gist.github.com/ivangeorgiev/693b45b78b37921191381a9f880a9ebc)) and started using it. Added recent planetary visits John and Jane made:

1. John visited Saturn together with Jane
2. John visited Mars
3. Jane visited Jupiter

Here is how I tracked this:

```python
johns_visits = VisitTracker('John')
janes_visits = VisitTracker('Jane')

#1 John visited Saturn together with Jane
johns_visits.visit('Saturn')
janes_visits.visit('Saturn')

#2 John visited Mars
johns_visits.visit('Mars')
johns_visits.list()

#3 Jane visited Jupiter
janes_visits.visit('Jupiter')
janes_visits.list()
```

And the output was not quite what I was expecting:

```
====== John's visits ======
['Saturn', 'Mars']
====== Jane's visits ======
['Saturn', 'Mars', 'Jupiter']
```

I was expecting:

```
====== John's visits ======
['Saturn', 'Mars']
====== Jane's visits ======
['Saturn', 'Jupiter']
```

If you do not believe me - check the Jupyter Notebook with the Python code and the results in [Colab](https://colab.research.google.com/gist/ivangeorgiev/693b45b78b37921191381a9f880a9ebc/hello-mars.ipynb).

What went wrong?

