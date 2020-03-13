
#!env python3
import unittest
from unittest.mock import MagicMock

from cicd_sim import Jenkins
from cicd_sim import Artifactory
from cicd_sim import Repos
from cicd_sim import BuildIdGenerator

class TestJenkins(unittest.TestCase):

    def setUp(self):
        self._repos = Repos()
        self._repo = self._repos.create_repo('theRepo', {})
        self._build_id_generator = BuildIdGenerator()

    def _create_jenkins(self, artifactory = Artifactory()):
        return Jenkins(artifactory, self._repos, build_id_generator=self._build_id_generator)

    def _create_jenkins_artifactory_mock(self):
        self._mock_artifactory = Artifactory()
        self._mock_artifactory.publish = MagicMock()
        return self._create_jenkins(self._mock_artifactory)

    def _get_or_create_branch(self, branch_name, version, requires = ''):
        branch = self._repo.checkout(branch_name)
        branch.commit_file('VERSION', version)
        return branch.commit_file('REQUIRES', requires)

    def test_build_develop(self):
        self._build_id_generator.generate_id = MagicMock(return_value = "theBuildId")
        branch = self._get_or_create_branch('develop', '1.2.3')
        branch.get_commit_sha = MagicMock(return_value = "0000000")
        jenkins = self._create_jenkins_artifactory_mock()
        jenkins.build(branch)
        self._mock_artifactory.publish.assert_called_with('theRepo', '1.2.3-theBuildId+0000000')

    def test_build_release(self):
        self._build_id_generator.generate_id = MagicMock(return_value = "theBuildId")
        branch = self._get_or_create_branch('release/1.2', '1.2.3')
        branch.get_commit_sha = MagicMock(return_value = "0000000")
        jenkins = self._create_jenkins_artifactory_mock()
        jenkins.build(branch)
        self._mock_artifactory.publish.assert_called_with('theRepo', '1.2.3-rc.theBuildId+0000000')

    def test_build_master(self):
        self._build_id_generator.generate_id = MagicMock(return_value = "theBuildId")
        branch = self._get_or_create_branch('master', '1.2.3')
        branch.get_commit_sha = MagicMock(return_value = "0000000")
        jenkins = self._create_jenkins_artifactory_mock()
        jenkins.build(branch)
        self._mock_artifactory.publish.assert_called_with('theRepo', '1.2.3')

    def test_build_feature_a(self):
        self._build_id_generator.generate_id = MagicMock(return_value = "theBuildId")
        branch = self._get_or_create_branch('feature/a', '1.2.3')
        branch.get_commit_sha = MagicMock(return_value = "0000000")
        jenkins = self._create_jenkins_artifactory_mock()
        jenkins.build(branch)
        self._mock_artifactory.publish.assert_called_with('theRepo', '1.2.3-theBuildId+0000000')

    def test_build_hotfix_1_2_4(self):
        self._build_id_generator.generate_id = MagicMock(return_value = "theBuildId")
        branch = self._get_or_create_branch('hotfix/a', '1.2.4')
        branch.get_commit_sha = MagicMock(return_value = "0000000")
        jenkins = self._create_jenkins_artifactory_mock()
        jenkins.build(branch)
        self._mock_artifactory.publish.assert_called_with('theRepo', '1.2.4-rc.theBuildId+0000000')

    def test_build_support_1_2(self):
        self._build_id_generator.generate_id = MagicMock(return_value = "theBuildId")
        branch = self._get_or_create_branch('support/1.2', '1.2.5')
        branch.get_commit_sha = MagicMock(return_value = "0000000")
        jenkins = self._create_jenkins_artifactory_mock()
        jenkins.build(branch)
        self._mock_artifactory.publish.assert_called_with('theRepo', '1.2.5')

    def test_build__build_same_lib_twice__expect_app_rebuild(self):
        artifactory = Artifactory()
        jenkins = self._create_jenkins(artifactory)

        lib_repo = self._repos.create_repo('lib', jenkins)
        lib = lib_repo.checkout('develop').commit_file('VERSION', '1.0.1')
        lib.push()

        app_repo = self._repos.create_repo('app', jenkins)
        app = app_repo.checkout('develop').commit_file('VERSION', '1.0.1').commit_file('REQUIRES', 'lib/1.x')
        app.push()

        # Expect a rebuild of 'app' because a new artifact for 'lib' will be created
        self.assertEqual(1, len(artifactory.get_artifacts()['app']))
        lib.push()
        self.assertEqual(2, len(artifactory.get_artifacts()['app']))

    def test_push_app__before_lib_available__conan_install_should_fail(self):
        jenkins = self._create_jenkins()

        lib_repo = self._repos.create_repo('lib', jenkins)
        lib_repo.checkout('master').commit_file('VERSION', '1.0.1')

        app_repo = self._repos.create_repo('app', jenkins)
        app = app_repo.checkout('master').commit_file('VERSION', '1.0.1').commit_file('REQUIRES', 'lib/1.x')
        # conan install should fail with exception
        self.assertRaises(Exception, lambda: app.push())
