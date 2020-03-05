#!env python3
from io import StringIO
import unittest
from unittest.mock import patch

from cicd_sim import StdOutput

class TestStdOutput(unittest.TestCase):

    def test_publish(self):
        out = StdOutput()
        with patch('sys.stdout', new=StringIO()) as capturedOutput:
            project_desc = 'MyProject'
            branch_descr = 'develop'
            version = '1.2.3-pre+1234'
            out.publish(project_desc, branch_descr, version)
            expected_string = ['PUBLISH', 'develop', '+', 'MyProject/1.2.3-pre+1234']
            effective_string = capturedOutput.getvalue().split()
            self.assertEqual(expected_string, effective_string)

    def test_resolved(self):
        out = StdOutput()
        with patch('sys.stdout', new=StringIO()) as capturedOutput:
            project_desc = 'MyProject'
            resolved_package = 'lib/1.2.3-pre+1234'
            out.resolved(project_desc, resolved_package)
            expected_string = ['RESOLVE', 'MyProject', '>', 'lib/1.2.3-pre+1234']
            effective_string = capturedOutput.getvalue().split()
            self.assertEqual(expected_string, effective_string)

    def test_installing(self):
        out = StdOutput()
        with patch('sys.stdout', new=StringIO()) as capturedOutput:
            branch_descr = 'TheBranch'
            resolved_package = 'lib/1.2.3-pre+1234'
            out.installing(branch_descr, resolved_package)
            expected_string = ['INSTALLING', 'TheBranch', '*', 'lib/1.2.3-pre+1234']
            effective_string = capturedOutput.getvalue().split()
            self.assertEqual(expected_string, effective_string)

    def test_building(self):
        out = StdOutput()
        with patch('sys.stdout', new=StringIO()) as capturedOutput:
            project_desc = 'MyProject'
            out.building(project_desc)
            expected_string = ['BUILDING', 'MyProject']
            effective_string = capturedOutput.getvalue().split()
            self.assertEqual(expected_string, effective_string)

    def test_unresolved(self):
        out = StdOutput()
        with patch('sys.stdout', new=StringIO()) as capturedOutput:
            project_desc = 'MyProject'
            requires = 'libA/1.2.x'
            out.unresolved(project_desc, requires)
            expected_string = ['ERROR', 'MyProject>', 'Unresolved', 'requires:', 'libA/1.2.x']
            effective_string = capturedOutput.getvalue().split()
            self.assertEqual(expected_string, effective_string)
