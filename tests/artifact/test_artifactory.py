#!env python3
import unittest

from cicd_sim import Artifactory

class TestArtifactory(unittest.TestCase):

    def _create_artifactory(self):
        artifactory = Artifactory()
        return artifactory

    def test_empty_artifacts(self):
        artifactory = self._create_artifactory()
        self.assertEqual({}, artifactory.get_artifacts())

    def test_publish_artifact_expect_artifact_in_store(self):
        artifactory = self._create_artifactory()
        artifactory.publish('unitTestProject', 'ArtifactIdentifier')
        artifacts = artifactory.get_artifacts()
        self.assertEqual({'unitTestProject': ['ArtifactIdentifier']}, artifacts)
