import copy
import colored
from colored import stylize

from . files import Files

class Branch:
    """A Git branch

    It basically has a `name` and a `list of files`. With every `commit`, the 
    branch's SHA changes.
    """
    def __init__(self, name, repo):
        self._name = name
        self._repo = repo
        self._files = Files()
        self._colour = 'black'
        self._commit_sha = repo.generate_next_sha()

    def __repr__(self):
        return self.get_description(True)
    
    def commit_file(self, file_name, content):
        """
        Commits a file specified by the file name and its content. If the file 
        already exists, its content will be overwritten.

        The changes will be committed, thereby, a new SHA will be generated.
        
        :return: Itself (the branch)
        """
        self._files.set_file_content(file_name, content)
        self._commit()
        return self
        
    def checkout(self, name, colour = 'black'):
        new_branch = self._repo.checkout(name, colour)
        new_branch.set_files(copy.deepcopy(self._files))
        return new_branch

    def delete(self):
        self._repo.delete_branch(self)
        
    def get_description(self, colorized = False):
        description = '{}[{}]'.format(self.get_project_name(), self.get_name())
        if colorized:
            description = stylize(description, colored.bg(self.get_colour()))
        return description
        
    def set_files(self, files):
        self._files = files
        
    def merge(self, foreign_branch, delete_after_merge = True):
        self._files = copy.deepcopy(foreign_branch._files)
        self._commit()
        if delete_after_merge:
            foreign_branch.delete()
        return self

    def push(self):
        self._repo.push(self)

    def _commit(self):
        self._commit_sha = self._repo.generate_next_sha()
    
    def get_name(self):
        return self._name
        
    def get_project_name(self):
        return self._repo.get_name()
          
    def get_commit_sha(self):
        return self._commit_sha
        
    def get_version(self):
        return self.get_file_content('VERSION')

    def set_version(self, version):
        """Set the project version

        :version: A string denoting a semver.org version. E.g. '1.2.3-pre.0+20200313'
        
        Technically, this function commits a file named 'VERSION' as this CICD
        simulator expects an according file to determine the project version.
        """
        self.commit_file('VERSION', version)

    def get_requires(self):
        return self.get_file_content('REQUIRES')

    def set_requires(self, requires):
        """Set the project requires (AKA dependencies)

        :requires: A string composed of the required package and the required 
        semver version or version range delimited by a slash ('/'). 
        E.g. 'lib/1.2.4', 'libA/1.x' or even 'lib/>1.0.0.0-0 <2.0.0'
        
        Technically, this function commits a file named 'REQUIRES' as this CICD
        simulator expects an according file to determine the projects 
        requirements.
        """
        self.commit_file('REQUIRES', requires)

    def get_file_content(self, file_name):
        return self._files.get_file_content(file_name)
        
    def set_colour(self, colour):
        self._colour = colour

    def get_colour(self):
        return self._colour