from . repo import Repo

class Repos:
    """"Repos" which can be seen like GitHub/GitLab/BitBucket

    It has a list of "Repo" instances.
    """
    def __init__(self):
        self._repos = []

    def create_repo(self, project_name, buildmachine):
        repo = self._find_repo(project_name)
        if repo is None:
            repo = Repo(project_name, buildmachine)
            self._repos.append(repo)
        return repo
    
    def get_repos(self):
        return self._repos

    def _find_repo(self, repo_name):
        for repo in self._repos:
            if repo.get_name() == repo_name:
                return repo
