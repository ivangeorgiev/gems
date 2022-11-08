# pytest Command Line Option to include integration tests

You need to declare the custom marker, e.g. in `pytest.ini`: 

```ini
# pytest.ini
[pytest]
markers = 
	integration: mark a test as integration
```

To maintain the  `--integration` command line option some changes need to be done to the pytest plugin module `conftest.py`:

```python
# conftest.py

def pytest_addoption(parser):
	parser.addoption("--integration", action="store_true",
					  help="run integration tests")

def pytest_runtest_setup(item):
	if 'integration' in item.keywords and not \
			item.config.getvalue("integration"):
		pytest.skip("need --integration option to run")
```

First function `pytest_addoption` is a pytest hook which is executed during command line options setup. The function adds the `--integration`  command line option to pytest.

The second function `pytest_runtest_setup` is a pytest hook which is invoked during the setup for each test. If the test is marked with `integration` it will be skipped.



You could mark all tests from a python file as integration tests:

```python
# test_something.py

# ... your code ...

pytestmark = pytest.mark.integration

# ... your code ...
```

