"""
Based on https://rollout.io/blog/yaml-tutorial-everything-you-need-get-started/

>>> import yaml
>>> from io import StringIO
>>> from pprint import pprint
>>> yaml_string = '''
...         doe: "a deer, a female deer"
...         ray: "a drop of golden sun"
...         pi: 3.14159
...         xmas: true
...         french-hens: 3
...         calling-birds: 
...         - huey
...         - dewey
...         - louie
...         - fred
...         xmas-fifth-day: 
...         calling-birds: four
...         french-hens: 3
...         golden-rings: 5
...         partridges: 
...             count: 1
...             location: "a pear tree"
...         turtle-doves: two
... '''
>>> obj = yaml.load(StringIO(yaml_string))
>>> pprint(obj, indent=4)
{   'calling-birds': 'four',
    'doe': 'a deer, a female deer',
    'french-hens': 3,
    'golden-rings': 5,
    'partridges': {'count': 1, 'location': 'a pear tree'},
    'pi': 3.14159,
    'ray': 'a drop of golden sun',
    'turtle-doves': 'two',
    'xmas': True,
    'xmas-fifth-day': None}

>>> doc = '''
... bar: |
...   this is not a normal string it
...   spans more than
...   one line
...   see?
... '''
>>> obj = yaml.load(StringIO(doc))
>>> pprint(obj, indent=4)
{'bar': 'this is not a normal string it\\nspans more than\\none line\\nsee?\\n'}

>>> doc = '''
... foo: "this is not a normal string\\n"
... bar: this is not a normal string\\n
... '''
>>> obj = yaml.load(StringIO(doc))
>>> pprint(obj, indent=4)
{'bar': 'this is not a normal string', 'foo': 'this is not a normal string '}

Booleans
>>> doc = '''
... [true, True, Yes, On, false, False, No, Off]
... '''
>>> obj = yaml.load(StringIO(doc))
>>> pprint(obj, indent=4)
[True, True, True, True, False, False, False, False]


Arrays
>>> doc = '''
... items:
...   - things:
...       thing1: huey
...       things2: dewey
...       thing3: louie
...   - other things:
...       key: value
... '''
>>> obj = yaml.load(StringIO(doc))
>>> pprint(obj, indent=4)
{   'items': [   {   'things': {   'thing1': 'huey',
                                   'thing3': 'louie',
                                   'things2': 'dewey'}},
                 {'other things': {'key': 'value'}}]}
"""

if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

