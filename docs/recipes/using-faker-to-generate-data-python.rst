Using faker to generate fake data
==================================

Use ``pip`` to install `faker`_:

.. code-block:: console

   $ pip install faker
   ..................

Examples:
-----------

.. code-block:: python

   >>> from faker import Faker
   >>> fake = Faker()
   >>> fake.name()
   'Lauren Mendez'
   >>> fake.phone_number()
   '4390337172'
   >>> fake.email()
   'melissa99@example.net'
   >>> fake.city()
   'Port Benjaminmouth'

`Faker`_ uses providers to generate fake data. Each provider adds methods to the ``Faker`` instance. E.g. ``name()`` method is implemented by ``faker.providers.person`` while ``address()`` method is implemented by the ``faker.providers.address`` provider. Check the list of `standard providers`_ and the `community providers`_ to find out what methods can be used.

Some of providers are also `localized providers`_::

   >>> fake_bg = Faker("bg-BG")
   >>> fake_bg.name()
   'Др. Войнка Яркова'

Faker ``pytest`` fixture
----------------------------

Faker has its own ``pytest`` plugin which provides a ``faker`` fixture which can be used directly by tests.

.. code-block:: python

   def test_person_is_saved(faker):
      name = faker.name()
      address = faker.address()
      _ = Person(name, address)
      person = Person.objects.get(name=name)
      assert address == person.address

`Faker`_ also provides customization for the ``faker`` fixture through autouse fixtures::

   import pytest

   @pytest.fixture(scope='session', autouse=True)
   def faker_session_locale():
      return ['it_IT', 'ja_JP', 'en_US']

   @pytest.fixture(scope='session', autouse=True)
   def faker_seed():
      return 12345


For further details check the `faker pytest fixtures`_ documentation.

Further reading
----------------

- `Faker`_ documentation
- `Faker source`_ on github
- `Faker pypi project`_


.. _faker: https://faker.readthedocs.io/en/latest/index.html
.. _faker pypi project: https://pypi.org/project/Faker/
.. _faker pytest fixtures: https://faker.readthedocs.io/en/latest/pytest-fixtures.html
.. _faker source: https://github.com/joke2k/faker
.. _standard providers: https://faker.readthedocs.io/en/latest/providers.html
.. _community providers: https://faker.readthedocs.io/en/latest/communityproviders.html
.. _localized providers: https://faker.readthedocs.io/en/latest/locales.html
