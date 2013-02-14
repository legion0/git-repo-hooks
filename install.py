#!python
import os, sys, shutil

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ALL_HOOKS_DIR = os.path.join(SCRIPT_DIR, 'hooks')

def main(args):
	shutil.rmtree(os.path.join(SCRIPT_DIR, '.git'))
	repoDir = getRepoDir(SCRIPT_DIR)
	if repoDir is None:
		die('Not in a repository.')
	allHooks = getAllHooks()
	print allHooks
	hooksDir = os.path.join(repoDir, '.git', 'hooks')
	shutil.move(os.path.join(SCRIPT_DIR, 'hookManager.py'), os.path.join(hooksDir, 'hookManager.py'))
	for hook in allHooks:
		src = os.path.join(SCRIPT_DIR, 'hooks', hook, '_' + hook)
		print src, '>'
		if os.path.exists(src):
			dest = os.path.join(hooksDir, hook)
			print '>', dest
			if os.path.exists(dest):
				shutil.move(dest, os.path.join(SCRIPT_DIR, 'hooks', hook, hook + '.hook'))
			shutil.move(src, dest)
	os.remove(os.path.join(SCRIPT_DIR, 'install.py'))

def getAllHooks():
	hooks = []
	for fileName in os.listdir(ALL_HOOKS_DIR):
		filePath = os.path.join(ALL_HOOKS_DIR, fileName)
		if os.path.isdir(filePath):
			hooks.append(fileName)
	return hooks

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