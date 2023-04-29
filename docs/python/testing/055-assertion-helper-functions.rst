Assertion Helper Functions
============================

Here is a assertion helper function example. The `__tracebackhide__ = True` line
instructs pytest to not include traceback for the assertion helper function.

.. code-block:: python

   def assert_something():
      __tracebackhide__ = True
      pytest.fail("I like failing")

And a very simple test wchich uses our assertion helper function.

.. code-block:: python

   def test_me()
      assert_something()

Executing the test:

.. code-block::

   ~/DjangoPytest$ python -m pytest
   ================ test session starts ================
   platform linux -- Python 3.8.12, pytest-7.3.1, pluggy-0.13.1
   rootdir: /home/runner/DjangoPytest
   collected 1 item

   tests/test_me.py F                            [100%]

   ===================== FAILURES ======================
   ______________________ test_me ______________________

      def test_me():
   >       assert_something()
   E       Failed: I like failing

   tests/test_me.py:10: Failed
   ============== short test summary info ==============
   FAILED tests/test_me.py::test_me - Failed: I like failing
   ================= 1 failed in 0.11s =================

More Complex Example
-------------------------

Here is a more complex example of testing the `urls/` endpoing from the Django Rest Framework
`installation example <https://www.django-rest-framework.org/#example>`__.

The `assert_response_userlist_equals()` assertion helper performs more complex assert. It
checks that the response jsoin is a list, than it checks that the list of users from the
response matches the expected users. Before comparing the lists, the assertion helper sorts them
by url.

.. code-block:: python

   from operator import itemgetter

   import pytest

   from django.urls import reverse
   from django.contrib.auth.models import User
   from rest_framework import status


   def assert_response_userlist_equals(response, users):
      __tracebackhide__ = True
      result = response.json()
      assert isinstance(
         result, list), f'Result is of type {type(result)}. Expected <list>'
      assert len(users) == len(
         result
      ), f'Result contains {len(result)} item(s). Expected {len(users)} item(s)'
      expected_items = [{
         'username': u.username,
         'email': u.email,
         'is_staff': u.is_staff,
         'url': f'http://testserver/users/{u.id}/',
      } for u in users]
      expected_items.sort(key=itemgetter('url'))
      result.sort(key=itemgetter('url'))
      assert result == expected_items


   @pytest.fixture
   def given_user_1():
      user = User.objects.create(username='user1')
      yield user
      user.delete()


   @pytest.fixture
   def given_user_2():
      user = User.objects.create(username='user2')
      yield user
      user.delete()


   @pytest.fixture
   def given_user_model_is_empty():
      User.objects.all().delete()


   @pytest.fixture
   def given_user_model_has_two_users(request):
      request.getfixturevalue('given_user_model_is_empty')
      return [
         request.getfixturevalue('given_user_1'),
         request.getfixturevalue('given_user_2')
      ]


   @pytest.mark.django_db
   def test_should_return_list_of_users(client, request):
      given_users = request.getfixturevalue('given_user_model_has_two_users')
      # When get user-list endpoint is executed
      url = reverse('user-list')
      response = client.get(url)
      # Then request is successfull
      assert response.status_code == status.HTTP_200_OK
      # And response matches expected
      assert_response_userlist_equals(response, given_users)

The complete project is available as `repl <https://replit.com/@ivangeorgiev7/DjangoPytest>`__.

The code of the test is also available as `Github gist <https://gist.github.com/ivangeorgiev/592aa63d177f6ede0c3bb7f6e115ca68>`.
