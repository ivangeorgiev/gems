# Test HTTP and API interactions with vcrpy

## Background

We have a simple `PeopleRepository` class which we are going to use to interact with the [Star Wars API](https://swapi.dev/). The repository class implements two methods:

| Method           | Purpose                                                      |
| ---------------- | ------------------------------------------------------------ |
| `all()`          | Return a list of all people from Star Wars                   |
| `find(**filter)` | Return a list of all people from Star Wars who match the given filter. |

Interaction with the API is through Python's request package.

We want to write tests to test our repository class.

## Solution

We are using the `pytest-recording` plugin for `pytest` which uses `pyvcr` to record HTTP interaction.

To install `pytest-recording` you can use `pip`:

```bash
pip install pytest-recording
```

Here is an example what our tests would look like:

```python
# File: test_peoplerepository.py

import pytest
from swapi import repository

# Apply these marks to all test cases from the module.
# Instruct VCR that default cassete should be stored in "swapi.yaml" rather than
# <test-case>.yaml
pytestmark = [pytest.mark.default_cassette("swapi.yaml"), ]

@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "ignore_localhost": True,
        # Instruct VCR that we want to record the interaction only once.
        "record_mode": "once",
    }

@pytest.fixture
def people_repo():
    return repository.PeopleRepository()

@pytest.mark.vcr()
def test_people_repo_all_returns_expected_number_of_people(people_repo):
    people = people_repo.all()
    assert len(list(people)) == 82

@pytest.mark.vcr()
def test_people_repo_find_returns_expectd_person(people_repo):
    results = list(people_repo.find(hair_color='blond', mass=None))
    assert len(results) == 1
    assert results.pop().name == 'Finis Valorum'

```

Running the tests with `pytest`:

```bash
$ pytest tests/test_peoplerepository.py -vv --cov repository.py
```

Produces similar output:

```
============================================== test session starts ===============================================
platform win32 -- Python 3.9.6, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- c:\sandbox\repos\pyvcr-examples\.venv\scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Sandbox\repos\pyvcr-examples
plugins: cov-3.0.0, recording-0.12.0
collected 2 items

star-wars-api/tests/test_repository.py::test_people_repo_all_returns_expected_number_of_people PASSED [ 50%]
star-wars-api/tests/test_repository.py::test_people_repo_find_returns_expectd_person PASSED           [100%]

----------- coverage: platform win32, python 3.9.6-final-0 -----------
Name                  Stmts   Miss  Cover
-----------------------------------------
swapi\repository.py      41      6    85%
-----------------------------------------
TOTAL                    41      6    85%

=============================================== 2 passed in 0.28s ================================================ 
```



## Complete example

You can find the complete example in Github: [https://github.com/ivangeorgiev/pyvcr-examples/tree/main/star-wars-api](https://github.com/ivangeorgiev/pyvcr-examples/tree/main/star-wars-api)



## Further Reading

* [pytest-recording](https://github.com/kiwicom/pytest-recording) at Github

* [vcrpy source](https://vcrpy.readthedocs.io/) at Github

* [vcrpy documentation](https://vcrpy.readthedocs.io/en/latest/) at Readthedocs

* [Explore Python Libraries: Speed Up HTTP Tests with VCR.py article](https://www.pluralsight.com/guides/explore-python-libraries:-speed-up-http-tests-with-vcr.py) article (Pluralsight)

* [Automatically mock your HTTP interactions to simplify and speed up testing](https://pythonrepo.com/repo/kevin1024-vcrpy-python-testing-codebases-and-generating-test-data) article

  