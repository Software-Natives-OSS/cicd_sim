from .. util.stdoutput import StdOutput
from .. util.build_id_generator import BuildIdGenerator
from .. conan import Conan


class Jenkins:
    """ A Jenkins simulation. It supports 'building a branch' which results in an artifact that gets published to an 'artifactory'
    """
    def __init__(self, artifactory, repos, config = {}):
        self._artifactory = artifactory
        self._repos = repos
        self._setup(config)        
        self._remember_built_branches = {}
        self._register_build_hooks()
    
    def _setup(self, config):
        self._conan = config['conan'] if 'conan' in config else Conan()
        self._output = config['output'] if 'output' in config else StdOutput()
        self._build_id_generator = config['build_id_generator'] if 'build_id_generator' in config else BuildIdGenerator()

    def _register_build_hooks(self):
        self._repos.set_buildmachine(self)
       
    def build(self, branch):
        """Build a Git branch.

        This means:

        - Execute `Conan install` to install requirements
        - It creates an artifact with an identifier
        - The artifact gets published to artifactory

        Finally, Jenkins iterates through all repositories (i.e. 'projects') 
        and checks whether the new artifact will change the version that'd be 
        taken by `conan install` because of the newly created artifact.
        """
        self._output.building(branch)
        resolved_requires = self._conan.install(branch, self._artifactory.get_artifacts())
        if self._shall_publish_artifact(branch):
            version = branch.get_version()
            suffix = self._get_version_suffix(branch)
            artifact_version = "{}{}".format(version, suffix)
            self._publish_artifact(branch, artifact_version)
            self._remember_built_artifact(branch, resolved_requires)
            self.check_repos_require_build()
    
    def check_repos_require_build(self):
        """Check if projects needs to be rebuild becuase their 'requires' have 
        new artifacts. E.g. if a library artifacts get added, the application 
        may need a rebuild."""
        for repo in self._repos.get_repos():
            for branch in repo.get_branches():
                resolved_requires, _ = self._conan.resolve_requires(self._artifactory.get_artifacts(), branch)
                if resolved_requires and self._is_artifact_rebuild_required(branch, resolved_requires):
                    self.build(branch)

    def _shall_publish_artifact(self, branch):
        branch_name = branch.get_name()
        if branch_name == 'master':
            return True
        if branch_name == 'develop':
            return True
        if branch_name.startswith('release/'):
            return True
        if branch_name.startswith('support/'):
            return True
        if branch_name.startswith('hotfix/'):
            return True
        # e.g. 'feature/xyz'
        return False

    def _remember_built_artifact(self, branch, resolved_requires):
        project_desc = branch.get_description(True)
        self._remember_built_branches[project_desc] = resolved_requires
     
    def _is_artifact_rebuild_required(self, branch, resolved_requires):
        project_desc = branch.get_description(True)
        branch_built_before = self._remember_built_branches.get(project_desc)
        return resolved_requires != branch_built_before

    def _publish_artifact(self, branch, version):
        descr = branch.get_description(colorized = True)
        self._output.publish(branch.get_project_name(), descr, version)
        self._artifactory.publish(branch.get_project_name(), version)
    
    def _get_version_suffix(self, branch):
        build_id = self._get_build_id()
        sha1 = branch.get_commit_sha()
        branch_name = branch.get_name()
        if branch_name == 'master':
            return ""
        elif branch_name.startswith('support/'):
            return ""
        elif branch_name.startswith('hotfix/'):
            return "-rc.{}+{}".format(build_id, sha1)
        elif branch_name.startswith('release/'):
            return "-rc.{}+{}".format(build_id, sha1)
        else:
            return "-{}+{}".format(build_id, sha1)

    def _get_build_id(self):
        return self._build_id_generator.generate_id()
