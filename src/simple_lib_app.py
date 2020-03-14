from cicd_sim import *

# Setup environment
github = Repos()
artifactory = Artifactory()
jenkins = Jenkins(artifactory, github)

# Create Git repos/projects
lib = github.create_repo('lib')
app = github.create_repo('app')

# Start developing
lib_dev = lib.checkout('develop', 'blue')
lib_dev.set_version('1.0.1')
lib_dev.push()

app_dev = app.checkout('develop', 'blue')
app_dev.set_version('1.0.0')
app_dev.set_requires('lib/1.x')
app_dev.push()
