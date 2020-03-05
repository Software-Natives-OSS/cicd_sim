class StdOutput:
    """Outputter writing everything to 'stdout'
    """

    def building(self, project_desc):
        print("{}{}".format('BUILDING'.ljust(20), project_desc))

    def installing(self, branch_description, resolved_package):
        print('{}{}* {}'.format('    INSTALLING'.ljust(20), branch_description.ljust(40), resolved_package))

    def publish(self, project_desc, branch_description, version):
        print("{}{}".format('        PUBLISH'.ljust(20), branch_description).ljust(60) +
                '+ {}/{}'.format(project_desc, version))

    def resolved(self, project_desc, resolved_package):
        print('{}{}{}> {}'.format('RESOLVE'.ljust(20), ' ' * 20, project_desc.ljust(30), resolved_package))

    def unresolved(self, project_desc, requires):
        print('{}{}> Unresolved requires: {}'.format('ERROR'.ljust(15), project_desc, requires))
