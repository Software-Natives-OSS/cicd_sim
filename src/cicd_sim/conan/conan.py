from semver import max_satisfying


class Conan:
    """Simple implementation of Conan.io

    It tries to resemble the functionality of Conan regarding `semver` handling.
    """
    def __init__(self, output):
        self._output = output
        
    def install(self, branch, artifacts):
        """Basically resembles `conan install`. It therefore checks if this 
        branch has a `requires` file. If it has, it searches for the "best 
        matching" artifact in the list of artifacts.
        """
        resolved_package, requires = self.resolve_requires(artifacts, branch)
        if resolved_package:
            self._output.installing(branch.get_description(colorized = True), resolved_package)
        elif requires is not None:
            self._output.unresolved(branch, requires)
            raise(Exception("Conan install failed"))
        return resolved_package

    def resolve_requires(self, artifacts, branch):
        """Resolves any possibly required dependencies and returns that information.

        :arg artifacts: The artifacts
        :arg branch: The Git branch for which to resolve the required dependencies
        :return: tuple with (resolved package, this branch's requires) which may also result in `None`
        """
        requires = self._determine_requires(branch)
        resolved_package = None
        if requires:
            resolved_version_of_requires = self._resolve_version_of_requires(
                artifacts, requires)
            if resolved_version_of_requires:
                resolved_package = requires[0] + \
                    '/' + resolved_version_of_requires
                
        return resolved_package, requires

    def _determine_requires(self, branch):
        requires = branch.get_requires()
        if requires:
            try:
                project_name, version = requires.split('/')
                return project_name, version
            except ValueError:
                raise(Exception("Parsing 'REQUIRES' string failed: '{}'".format(requires)))
        return None

    def _resolve_version_of_requires(self, artifacts, requires):
        """@requires expect a tuple with like (project name, version)"""
        project_name, version = requires
        if project_name in artifacts:
            # print('#####', requires, '->', artifacts[project_name])
            return max_satisfying(artifacts[project_name],
                                  version, loose=False, include_prerelease=True)
