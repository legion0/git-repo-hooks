import os, sys, stat, shutil, subprocess

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
HOOKSDIR = os.path.join(SCRIPT_DIR, '..', '..', 'gitconfig', 'hooks')

def processHooks(hook):
	argv = sys.argv[1:]
	print "DEBUG: processing hook: ", str(argv)
	hookDir = os.path.join(HOOKSDIR, hook)
	repoDir = getRepoDir(SCRIPT_DIR)
	if repoDir is None:
		die('Not in a repository.')
	fileNames = os.listdir(hookDir)
	if len(fileNames) > 0:
		for fileName in fileNames:
			if fileName.endswith('.hook'):
				print "DEBUG: found hook: ", fileName
				filePath = os.path.join(hookDir, fileName)
				exe = os.stat(filePath).st_mode & stat.S_IEXEC
				if exe:
					cmd = [filePath]
					cmd.extend(argv)
					returncode = subprocess.call(cmd)
					print "DEBUG: hook returned: ", returncode
					if returncode != 0:
						return returncode
				else:
					print >> sys.stderr, "ERROR: hook is not executable."
	else:
		print "DEBUG: no hooks found"
	print "DEBUG: all ok for hook: ", hook
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