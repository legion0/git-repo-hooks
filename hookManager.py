#!python
import os, sys, shutil, subprocess

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
HOOKSDIR = os.path.join(SCRIPT_DIR, '..', '..', 'gitconfig', 'hooks')

def processHooks(hook):
	hookDir = os.path.join(HOOKSDIR, hook)
	cwd = os.getcwd()
	repoDir = getRepoDir(SCRIPT_DIR)
	if repoDir is None:
		die('Not in a repository.')
	#os.chdir(repoDir)
	for fileName in os.listdir(hookDir):
		if fileName.endswith('.hook'):
			filePath = os.path.join(hookDir, fileName)
			returncode = subprocess.call([filePath])
			if returncode != 0:
				return returncode
	return 0

def getRepoDir(directory):
	while '.git' not in os.listdir(directory) and directory != '/':
		directory, _ = os.path.split(directory)
	return directory if '.git' in os.listdir(directory) else None

def die(msg = None, exitcode = 1):
	if msg is not None:
		print >> sys.stderr, msg
	exit(exitcode)
	
if __name__=="__main__":
	main(sys.argv[1:])