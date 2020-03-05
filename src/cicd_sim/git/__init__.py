"""A trivial Git implementation.

It supports the very basics like a "Repos" which can be seen like GitHub/GitLab/BitBucket. I.e. "Repos" manages 0..n Git repos. The Git repos are resembled by "Repo". Each "Repo" has branches, resembled by "Branch" which has files "Files". Finally, there's an "SHA" class that simulates Git SHAs
"""
from . repos import Repos
from . repo import Repo
from . branch import Branch
from . files import Files
from . sha import SHA

__all__ = ['Repos', 'Repo', 'Branch']
