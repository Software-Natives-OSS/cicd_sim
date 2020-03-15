#!env python3
import pytest
import unittest
from unittest.mock import MagicMock, ANY

from cicd_sim import Repos
from cicd_sim import NullOutput
from cicd_sim import Conan

class TestConan(unittest.TestCase):

    def setUp(self):
        self._repos = Repos()

    def _create_test_library(self):
        return self._repos.create_repo('lib').checkout('master')

    def _create_test_app(self):
        app_master = self._repos.create_repo('app').checkout('master')
        app_master.set_version('6.0.0')
        return app_master

    def _create_conan(self, output = NullOutput()):
        return Conan(output)

    def test_check_empty_requires(self):
        artifacts = {
            'lib': []
        }
        self._create_test_library()
        output = MagicMock()
        output.resolved = MagicMock()
        app_branch = self._create_test_app()
        resolved_packages, requires = self._create_conan(output).resolve_requires(artifacts, app_branch)
        self.assertIsNone(resolved_packages)
        self.assertIsNone(requires)

    def test_check_requires_resolve(self):
        artifacts = {
            'lib': ['1.2.3']
        }
        app_branch = self._create_test_app()
        app_branch.set_requires('lib/1.x')
        resolved_packages, requires = self._create_conan().resolve_requires(artifacts, app_branch)
        self.assertEqual('lib/1.2.3', resolved_packages)
        self.assertEqual(('lib', '1.x'), requires)

    def test_check_requires_unresolved(self):
        artifacts = {
            'lib': ['2.2.3']
        }
        app_branch = self._create_test_app()
        app_branch.set_requires('lib/1.x')
        resolved_packages, requires = self._create_conan().resolve_requires(artifacts, app_branch)
        self.assertIsNone(resolved_packages)
        self.assertEqual(('lib', '1.x'), requires)

    def test_check_requires_requires_syntax_error(self):
        lib = self._repos.create_repo('lib')
        branch = lib.checkout('master')
        branch.set_requires('invalid | format')
        conan = self._create_conan()
        self.assertRaises(Exception, lambda: conan._determine_requires(branch))

    def test_conan_install(self):
        app_branch = self._create_test_app()
        app_branch.set_requires('lib/2.x')
        artifacts = {
            'lib': ['2.0.3']
        }

        output = MagicMock()
        self._create_conan(output).install(app_branch, artifacts)
        output.installing.assert_called_once()
        output.installing.assert_called_with(ANY, 'lib/2.0.3')

# [ 'requires', ['lib version 1', 'lib version 2', ...], 'expected installed version' ]
conan_install_test_values = [
    [   
        'lib/>1.0.0-0', 
        [
            '1.0.0-beta'
        ], 
        'lib/1.0.0-beta'
    ],
    [   
        'lib/>1.0.0-0', 
        [
            '1.0.0-beta', '1.0.0-rc'
        ], 
        'lib/1.0.0-rc'
    ],
    [   
        'lib/1.x', 
        [
            '1.0.0-beta', '1.0.0-rc', '1.0.0'
        ], 
        'lib/1.0.0'
    ],
    [   
        'lib/1.x', 
        [
            '1.0.0-beta', '1.0.0-rc', '1.0.0',
            '1.0.1'
        ], 
        'lib/1.0.1'
    ],
    # below, we're hit by https://github.com/podhmo/python-semver/issues/37
    # [   
    #     'lib/1.0.x', 
    #     [   
    #         '1.0.0-beta', '1.0.0-rc', '1.0.0', 
    #         '1.1.0-beta'
    #     ],
    #     'lib/1.0.0'
    # ],
    # [   
    #     'lib/1.0.x', 
    #     [   
    #         '1.0.0-beta', '1.0.0', '1.0.1',
    #         '1.1.0-beta', '1.1.0'
    #     ],
    #     'lib/1.0.0'
    # ]
]

@pytest.mark.parametrize("require_version, versions, expected_version", conan_install_test_values)
def test_conan_install_parametrized(require_version, versions, expected_version):
    app_branch = Repos().create_repo('lib').checkout('master')
    app_branch.set_requires(require_version)
    artifacts = {
        'lib': versions
    }

    output = MagicMock()
    Conan(output).install(app_branch, artifacts)
    output.installing.assert_called_once()
    output.installing.assert_called_with(ANY, expected_version)
