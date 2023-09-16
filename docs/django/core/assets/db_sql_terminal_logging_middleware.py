from logging import getLogger
from system import stdout

from django.conf import settings
from django.db import connection

class SqlTerminalLogging:
    def __init__(self, get_reponse):
        self.logger = getLogger(__name__)
        self.get_response = get_reponse

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(settings, "SQL_TERMINAL_LOGGING_SQL", settings.DEBUG):
            self._log_queries()
        return response

    def _log_queries(self):
        if stdout.isatty():
            for query in connection.queries:
                sql_str = " ".join(query["sql"].split())
                self.logger.debug(
                    f"\033[1;31m[{query['time']}s]\033[0m \033[1m{sql_str}\033[0m"
                )
