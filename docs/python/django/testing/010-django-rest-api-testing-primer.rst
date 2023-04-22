Django REST API Testing Primer
======================================

In this primer we will create a simple API test for Django API using pytest as testing framework.

Define pytest mark
--------------------------

I like grouping tests using `@pytest.mark`. Our test covers full scenario so I am marking it as end-to-end test.
Before this I need to define an `end2end` marker in `pytest.ini`:

.. code-block:: ini

   [pytest]
   junit_family=xunit1
   DJANGO_SETTINGS_MODULE=todos.test_settings
   markers=
      end2end: mark a test as end-to-end test
   addopts =
      -v
      -m not end2end


Test Implementation
------------------------------


.. code-block:: python

   import pytest
   from django.test import Client
   from django.urls import reverse
   from rest_framework import status

   class TestTodo

      def test_should_fail_to_list_when_not_authenticted(self):
         #
         # Given
         request.getfixturevalue('given_truncated_user_model')
         #
         # When request list of todos, matching a query
         url = reverse("todo-list")
         response = client.get(url, query)
         # Then request fails because not authorized
         assert response.status_code == status.HTTP_401_UNAUTHORIZED

      def test_should_return_list_of_todos_matching_query(self, request, client: Client):
         #
         # Given
         request.getfixturevalue('given_truncated_user_model')
         # AND
         request.getfixturevalue('given_logged_in_user')
         # AND
         request.getfixturevalue('given_truncated_todos')
         # AND
         search_query = request.getfixturevalue('given_search_query')
         # AND
         todos_that_match = request.getfixturevalue('given_todos_that_match_search_query')
         # AND
         request.getfixturevalue('todos_that_do_not_match_search_query')
         #
         # When request list of todos, matching a query
         url = reverse("todo-list")
         response = client.get(url, search_query)
         #
         # Then request succeeds with status 200-OK
         assert response.status_code == status.HTTP_200_OK
         # AND
         response_data = response.json()
         assert response_data["count"] == len(todos_that_match)

      @pytest.fixture
      def given_truncated_user_model(self, django_user_model):
         django_user_model.objects.all().delete()
         return django_user_model

      @pytest.fixture
      def given_existing_user(self, django_user_model):
         user = django_user_model.objects.create(
               username="todouser", is_staff=True
         )
         return user

      @pytest.fixture
      def given_logged_in_user(self, request, client: Client):
         user = request.getfixturevalue("given_existing_user")
         client.force_login(user)
         return user

      @pytest.fixture
      def given_truncated_todos(self):
         # TODO: Implement

      @pytest.fixture
      def given_search_query(self):
         return {"search": "pilates"}

      @pytest.fixture
      def given_todos_that_match_search_query(self):
         # TODO: Add todos that match the query
         # TODO: Return the todos

      @pytest.fixture
      def todos_that_do_not_match_search_query(self):
         # TODO: Add todos that do not match the query
         # TODO: Return the todos
