#!env python3
import unittest
from unittest.mock import MagicMock

from cicd_sim import Repo

class TestGitRepo(unittest.TestCase):

    def _createRepo(self, project_name = 'no-prj-name', services = {}):
        return Repo(project_name, services)

    def test_repo_name(self):
        repo = self._createRepo('MyRepoName')
        self.assertEqual('MyRepoName', repo.get_name())

    def test_new_repo_creates_default_branch(self):
        repo = self._createRepo()
        branches = repo.get_branches()
        self.assertEqual(1, len(branches), "Expect the default branch to be created")
        master = repo.checkout('master')
        self.assertEqual('master', master.get_name())
        self.assertEqual('green', master.get_colour())
    
    def test_first_sha(self):
        sha = self._createRepo().generate_next_sha()
        self.assertIsInstance(sha, str)

    def test_push_a_branch(self):
        buildmachine = MagicMock()
        buildmachine.build = MagicMock()
        branch = 'The Branch'
        repo = self._createRepo('a name', buildmachine)
        repo.push(branch)
        buildmachine.build.assert_called_with('The Branch')

    def test_create_branch(self):
        repo = self._createRepo()
        develop = repo.create_branch("develop")
        self.assertIn(develop, repo.get_branches())
        
    def test_delete_branch(self):
        repo = self._createRepo()
        develop = repo.create_branch('develop')
        repo.delete_branch(develop)
        self.assertNotIn(develop, repo.get_branches())

    def test_create_several_branches(self):
        repo = self._createRepo()
        master = repo.checkout('master')
        self.assertIsNotNone(master, "A default branch must be there")
        develop = repo.create_branch('develop')
        feature_a = repo.create_branch('feature/a')
        self.assertIn(master, repo.get_branches())
        self.assertIn(develop, repo.get_branches())
        self.assertIn(feature_a, repo.get_branches())

    def test_checkout_new_branch(self):
        repo = self._createRepo()
        new_branch = repo.checkout('new_branch')
        self.assertIsNotNone(new_branch)

    def test___repr___expect_contains_project_name(self):
        repo = self._createRepo()
        repo_name = repo.get_name()
        repr = (str)(repo)
        self.assertTrue(repr.find(repo_name) != -1)
