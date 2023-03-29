from django.core.management import call_command
from django.test import TestCase
from io import StringIO
from contextlib import redirect_stdout


class TestCSVLoader(TestCase):
    def test_command_output(self):
        out = StringIO()
        command = "load_sample"
        with out, redirect_stdout(out):
            call_command(command, stdout=out)
            expected = "Import complete"
            self.assertIn(expected, out.getvalue())
