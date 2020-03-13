#!env python3
import unittest

from cicd_sim import Repos

class TestGitRepos(unittest.TestCase):

    def setUp(self):
        self._repos = Repos()

    def test_create_repo(self):
        repo = self._repos.create_repo("ProjectName")
        self.assertIn(repo, self._repos.get_repos())

    def test_no_repos_after_creation(self):
        self.assertEqual(0, len(self._repos.get_repos()))

    def test_create_two_repos(self):
        repo1 = self._repos.create_repo("Prj1")
        repo2 = self._repos.create_repo("Prj2")
        self.assertIn(repo1, self._repos.get_repos())
        self.assertIn(repo2, self._repos.get_repos())

    def test_create_repo_that_already_exists__expect__return_existing(self):
        repo1 = self._repos.create_repo('repo')
        repo2 = self._repos.create_repo('repo')
        self.assertEqual(repo1, repo2)
