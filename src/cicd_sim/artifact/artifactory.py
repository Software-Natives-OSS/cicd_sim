class Artifactory:
    """A very minimalistic JFrog Artfiactory simulation.
    
    Stores published artifacts. Artifacts have an 'identifier' and belong to a 
    'project'
    """
    def __init__(self):
        self._artifacts = {}
        
    def publish(self, project_name, artifact_identifier):
        """Publishs an artifact

        :param project_name: The project to which this artfiact belongs to
        :param artifact_identifier: An artifact identifier, e.g. 'lib/1.0.0-beta'
        """
        if project_name not in self._artifacts:
            self._artifacts[project_name] = []
        if artifact_identifier not in self._artifacts[project_name]:
            self._artifacts[project_name].append(artifact_identifier)
        
    def get_artifacts(self):
        """

        :return: return a dict with 'project name' as key and a list of 'artifacts' that belongs to each project
        """
        return self._artifacts
