from cicd_sim import *

# Setup environment
github = Repos()
artifactory = Artifactory()
jenkins = Jenkins(artifactory, github)

# Create Git repos/projects
lib = github.create_repo('lib', jenkins)
app = github.create_repo('app', jenkins)

# Start developing
lib_dev = lib.create_branch('develop', 'blue')
lib_dev.commit_file('VERSION', '1.0.1')
lib_dev.push()

app_dev = app.create_branch('develop', 'blue')
app_dev.commit_file('VERSION', '1.0.0')
app_dev.commit_file('REQUIRES', 'lib/1.x')
app_dev.push()
