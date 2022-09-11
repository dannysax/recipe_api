from django.db import OperationalError
from django.test.testcases import SimpleTestCase
from psycopg2 import OperationalError as PsycopError
from unittest.mock import patch
from django.core.management import call_command


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test Database ready and database still loading"""

    def test_database_ready(self, patched_check):
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_database_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = [PsycopError] * 2 + \
            [OperationalError] * 3 + [True]
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=["default"])
