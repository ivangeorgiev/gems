from django.conf import settings
from django.db import connection
from django.core import exceptions

class DbLockTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.lock_timeout = int(getattr(settings, "DB_LOCK_TIMEOUT", -1))
        if self.lock_timeout == -1:
            raise exceptions.MiddlewareNotUsed("No lock timeout is required")

    def __call__(self, request):
        with connection.execute_wrapper(self._set_lock_timeout_execute_wrapper):
            response = self.get_response(request)
        return response

    # pylint: disable=too-many-arguments
    def _set_lock_timeout_execute_wrapper(self, execute, sql, params, many, context):
        execute(f"SET LOCK_TIMEOUT {self.lock_timeout}", [])
        result = execute(sql, params, many, context)
        return result
