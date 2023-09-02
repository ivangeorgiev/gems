Event Hub for Python
============================

Event Handling
-----------------

.. literalinclude:: events/events.py
    :language: python
    :caption: events.py

Unit Tests
-----------

.. literalinclude:: events/test_events.py
    :language: python
    :caption: test_events.py


Integration with Django Signals
--------------------------------

.. code-block:: python
    :caption: signals.py

    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from .events import JobCreated, JobUpdated, handle

    from .models import Job


    @receiver(post_save, sender=Job)
    def job_post_save_handler(sender, instance, raw, created, **_):
        if raw: # pragma: no cover
            return
        if created:
            handle(JobCreated(instance))
        else:
            handle(JobUpdated(instance))


.. code-block:: python
    :caption: test_signals.py

    from unittest.mock import Mock, patch

    import pytest
    from .events import JobCreated, JobUpdated

    from .models import Job

    pytestmark = [pytest.mark.django_db]

    @pytest.fixture(name="job")
    def given_job():
        job = Job.objects.create(label="Test Job", arguments="Test Arguments", stage="new")
        yield job


    @patch("schema_discovery.signals.handle")
    def test_should_handle_JobCreated_event_when_creating_event(mock_handle: Mock, request):
        job = request.getfixturevalue("job")
        mock_handle.assert_called_once()
        event, = mock_handle.call_args.args
        assert isinstance(event, JobCreated)
        assert event.job is job

    @patch("schema_discovery.signals.handle")
    def test_should_handle_JobUpdated_event_when_updating_event(mock_handle: Mock, job, request):
        job.save()
        mock_handle.assert_called_once()
        event, = mock_handle.call_args.args
        assert isinstance(event, JobUpdated)
        assert event.job is job



2023-09-02
