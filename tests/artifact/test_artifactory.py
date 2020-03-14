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
        artifactory.publish('unitTestProject', '1.0.1-pre')
        artifacts = artifactory.get_artifacts()
        self.assertEqual({'unitTestProject': ['1.0.1-pre']}, artifacts)

    def test_overwrite_artefacts(self):
        artifactory = self._create_artifactory()
        artifactory.publish('unitTestProject', '1.0.0')
        artifactory.publish('unitTestProject', '1.0.0')
        artifacts = artifactory.get_artifacts()
        self.assertEqual({'unitTestProject': ['1.0.0']}, artifacts)
