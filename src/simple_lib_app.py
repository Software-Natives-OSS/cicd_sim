from cicd_sim import *

output = StdOutput()
bb = Repos()
conan = Conan(StdOutput())
artifactory = Artifactory()
build_id = BuildIdGenerator()
jenkins = Jenkins(artifactory, conan, bb, output, build_id)

lib = bb.create_repo('lib', jenkins)
app = bb.create_repo('app', jenkins)

lib_dev = lib.create_branch('develop', 'blue')
lib_dev.commit_file('VERSION', '1.0.1')
lib_dev.push()

app_dev = app.create_branch('develop', 'blue')
app_dev.commit_file('VERSION', '1.0.0')
app_dev.commit_file('REQUIRES', 'lib/1.x')
app_dev.push()

lib_dev.push()
