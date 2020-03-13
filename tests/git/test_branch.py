#!env python3
import unittest
from unittest.mock import MagicMock

from cicd_sim import Branch
from cicd_sim import Repos

class TestGitBranch(unittest.TestCase):

    def setUp(self):
        self._project_name = 'ProjectName'
        self._repo = self._create_repo(buildmachine=None)

    def _create_repo(self, buildmachine):
        repos = Repos()
        repos.set_buildmachine(buildmachine)
        return repos.create_repo(self._project_name)

    def test_default_branch(self):
        branch = Branch('develop', self._repo)
        self.assertEqual('black', branch.get_colour())
        self.assertEqual('develop', branch.get_name())
        self.assertEqual(self._project_name, branch.get_project_name())
        # As we're creating a new SHA for each new branch, and because
        # a new repo creates a default branch ('master'), we're at 
        # 0000002 now
        self.assertEqual("0000002", branch.get_commit_sha())
    
    def test_create_branch_file_copied(self):
        master = self._repo.checkout('master')
        master.commit_file('FileA', 'aaa')
        master.commit_file('FileB', 'bbb')
        develop = master.create_branch('develop')
        self.assertEqual('aaa', develop.get_file_content('FileA'))
        self.assertEqual('bbb', develop.get_file_content('FileB'))

    def test_merge_branch(self):
        master = self._repo.checkout('master')
        master.commit_file('FileA', 'aaa')
        master.commit_file('FileB', 'bbb')
        develop = master.create_branch('develop')
        develop.commit_file('FileA', 'aaa222')
        develop.commit_file('FileDevelop', 'develop')
        master.merge(develop)
        self.assertEqual('aaa222', master.get_file_content('FileA'))
        self.assertEqual('bbb', master.get_file_content('FileB'))
        self.assertEqual('develop', master.get_file_content('FileDevelop'))

    def test_delete_branch(self):
        master = self._repo.checkout('master')
        self.assertIn(master, self._repo.get_branches())
        master.delete()
        self.assertNotIn(master, self._repo.get_branches())

    def test___repr___expect_no_error(self):
        master = self._repo.checkout('master')
        self.assertIsNotNone((str)(master))
        
    def test_push_expect_build_trigger(self):
        buildmachine = MagicMock()
        buildmachine.build = MagicMock()
        repo = self._create_repo(buildmachine)
        master = repo.checkout('master')
        master.push()
        buildmachine.build.assert_called_once_with(master)

    def test_chaining(self):
        buildmachine = MagicMock()
        repo = self._create_repo(buildmachine)
        branch = repo.checkout('master').set_version('1.2.3')
        self.assertEqual(repo.checkout('master'), branch)

    def test_create_branch__new_color(self):
        branch1 = self._repo.create_branch('branch1', 'colour1')
        self.assertEqual('colour1', branch1.get_colour())
        branch2 = branch1.create_branch('branch2', 'colour2')
        self.assertEqual('colour2', branch2.get_colour())
        
    def test_create_branch__already_exists__checkout_instead(self):
        branch1 = self._repo.create_branch('branch1')
        branch2 = self._repo.create_branch('branch1')
        self.assertEqual(branch1, branch2)
        
    def test_branch_description__expect_branch_name(self):
        branch2 = self._repo.create_branch('branch1')
        self.assertTrue(branch2.get_description().find('branch1') >= 1)
        