from .. util.build_id_generator import BuildIdGenerator

class BuildStrategyA:
    """This build strategy, which is intentionally got a neutral name 'A', 
    implements the following strategy: It assumes development happens by GitFlow.

    - Artfiacts are published for the following branches: develop, release/..., 
    support/..., hotfix/... and, of course, master. For all other branches, 
    namely feature/..., no artifacts are published
    - 'master' and 'support' branches get no 'pre-release',
      such as in "1.2.3"
    - 'hotfix' and 'release' branches get a '-rc.DATTIME+SHA' pre-release,
      such as in "1.2.3-rc.200407123456+0000001"
    - all other branches, namely 'feature' gets a '-DATTIME+SHA' pre-release,
      such as in "1.2.3-200407123456+0000001"
    """
    def __init__(self, build_id_generator = BuildIdGenerator()):
        self._build_id_generator = build_id_generator
        self.name = "Build Strategy A"

    def shall_publish_artifact(self, branch):
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

    def generate_artifact_version(self, branch):
        branch_version = branch.get_version()
        version_suffix = self._get_version_suffix(branch)
        return "{}{}".format(branch_version, version_suffix)

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
