import copy

from . branch import Branch
from . sha import SHA

class Repo:
    """A "Repo" is a single Git repo
    """
    def __init__(self, name, repos):
        self._branches = []
        self._sha = SHA()
        self._name = name
        self._repos = repos
        self._create_default_branch()

    def __repr__(self):
        return self.get_name()

    def generate_next_sha(self):
        return self._sha.generate_next()

    def push(self, branch):
        self._repos.trigger_buildmachine(branch)

    def get_name(self):
        return self._name
    
    def checkout(self, branch_name, colour = None):
        """
        Checkout a branch. If the branch doesn't exist, it'll be created on the fly.
        
        :branch_name: A Git branch name, e.g. "master", "develop", etc.
        :colour: The colour for this branch. If set to 'None', a default colour 
        will be applied if the branch is newly created. If the branch already 
        exists, the existing colour will be kept. If a colour unequal to 'None' 
        is set, the branch will end up with the specified colour. The library 
        used to colorize is documented here: https://pypi.org/project/colored/
        :return: The branch object
        """
        branch = self._find_branch(branch_name)
        if branch is None:
            colour = colour if colour is not None else 'black'
            branch = Branch(branch_name, self)
            self._add_branch(branch)
        if colour is not None:
            branch.set_colour(colour)
        return branch
    
    def get_branches(self):
        return self._branches

    def delete_branch(self, branch):
        if branch in self._branches: self._branches.remove(branch)
        
    def _create_default_branch(self):
        # Create the default branch
        self.checkout('master', 'green')

    def _add_branch(self, branch):
        self._branches.append(branch)
    
    def _find_branch(self, branch_name):
        for branch in self.get_branches():
            if branch.get_name() == branch_name:
                return branch
