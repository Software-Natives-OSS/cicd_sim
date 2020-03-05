import copy

from . branch import Branch
from . sha import SHA

class Repo:
    """A "Repo" is a single Git repo
    """
    def __init__(self, name, buildmachine):
        self._branches = []
        self._sha = SHA()
        self._name = name
        self._buildmachine = buildmachine
        self._create_default_branch()

    def __repr__(self):
        return self.get_name()

    def generate_next_sha(self):
        return self._sha.generate_next()

    def push(self, branch):
        self._buildmachine.build(branch)

    def get_name(self):
        return self._name
    
    def checkout(self, branch_name):
        return self.create_branch(branch_name)

    def create_branch(self, branch_name, colour = 'black'):
        branch = self._find_branch(branch_name)
        if branch is None:
            branch = Branch(branch_name, self)
            branch.set_colour(colour)
            self._add_branch(branch)
        return branch
    
    def get_branches(self):
        return self._branches

    def delete_branch(self, branch):
        if branch in self._branches: self._branches.remove(branch)
        
    def _create_default_branch(self):
        # Create the default branch
        self.create_branch('master', 'green')

    def _add_branch(self, branch):
        self._branches.append(branch)
    
    def _find_branch(self, branch_name):
        for branch in self.get_branches():
            if branch.get_name() == branch_name:
                return branch
