class NullOutput:
    """Null implementation useful for unit testing.
    """
    
    def building(self, project_desc):
        """Dummy outputter"""

    def installing(self, branch_description, resolved_package):
        """Dummy outputter"""

    def publish(self, project_name, branch_description, version):
        """Dummy outputter"""

    def resolved(self, project_desc, resolved_package):
        """Dummy outputter"""

    def unresolved(self, project_desc, requires):
        """Dummy outputter"""
