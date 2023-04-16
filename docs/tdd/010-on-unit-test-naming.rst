On Unit Test Naming
===========================

Unit Test Name Pattern
------------------------

.. code-block:: python

   class TestMyClass:
      def test_should_dosomething(self):
         pass

.. code-block:: python

   class TestUserRepository:
      @pytest.fixture
      def given_fake_user_objects_manager(self):
         with pytest.mock.object(models.User, 'objects') as fake_manager:
            yield fake_manager

      @pytest.fixture
      def given_non_existent_user_id(self, request):
         user_id = 1923
         manager = request.getfixturevalue('given_fake_user_objects_manager')
         manager.get.side_effect = ObjectDoesNotExist
         return user_id

      @pytest.fixture
      def given_dummy_user(self):
         dummy_user = SimpleNamespace(
            id = 123,
            name = "johndoe",
            first_name = "John",
            last_name = "Doe",
         )
         return dummy_user

      @pytest.fixture
      def given_existing_user(self, request):
         manager = request.getfixturevalue('given_fake_user_objects_manager')
         dummy_user = request.getfixturevalue('given_dummy_user')
         manager.get.return_value = dummy_user
         return dummy_user

      @pytest.fixture
      def given_existing_user_id(self, request):
         user = request.getfixturevalue('given_existing_user')
         return user.id

      @pytest.fixture
      def given_user_repository(self, requests):
         return UserRepository()

      def test_should_load_existing_user_by_id(self, request):
         existing_user_id = request.getfixturevalue('given_existing_user_id')
         repo = request.getfixturevalue('given_user_repository')
         #
         result = repo.get(existing_user_id)
         #
         manager = request.getfixturevalue('given_fake_user_objects_manager')
         manager.get.assert_called_once_with(user_id=existing_user_id)
         assert result is manager.get.return_value

      def test_should_fail_to_load_missing_user_raising_ObjectDoesNotExist_exception(self, request):
         non_existent_user_id = request.getfixturevalue('given_non_existent_user_id')
         repo = request.getfixturevalue('given_user_repository')
         #
         with pytest.raises(ObjectDoesNotExist, match=f"User does not exist: {non_existent_user_id}"):
            repo.get(non_existent_user_id)
         manager = request.getfixturevalue('given_fake_user_objects_manager')
         manager.get.assert_called_once_with(user_id=non_existent_user_id)
