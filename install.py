#!/usr/bin/env python
import os, sys, shutil

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
ALL_HOOKS_DIR = os.path.join(SCRIPT_DIR, 'hooks')
allHooks = None

def main(args):
	global allHooks
	selfGit = os.path.join(SCRIPT_DIR, '.git')
	if os.path.exists(selfGit):
		shutil.rmtree(selfGit)
	repoDir = getRepoDir(SCRIPT_DIR)
	if repoDir is None:
		die('Not in a repository.')
	gitconfigDir = os.path.join(repoDir, 'gitconfig')
	allHooks = getAllHooks()
	prepareGitConfig(gitconfigDir, allHooks)
	hooksDir = os.path.join(repoDir, '.git', 'hooks')
	shutil.move(os.path.join(SCRIPT_DIR, 'hookManager.py'), os.path.join(hooksDir, 'hookManager.py'))
	for hook in allHooks:
		src = os.path.join(SCRIPT_DIR, 'hooks', hook, '_' + hook)
		if os.path.exists(src):
			dest = os.path.join(hooksDir, hook)
			if os.path.exists(dest):
				shutil.move(dest, os.path.join(gitconfigDir, 'hooks', hook, hook + '.hook'))
			shutil.move(src, dest)
	shutil.rmtree(SCRIPT_DIR)

def prepareGitConfig(gitconfigDir, hooks):
	hooksDir = os.path.join(gitconfigDir, 'hooks')
	if not os.path.exists(hooksDir):
		os.makedirs(hooksDir)
	for hook in allHooks:
		directory = os.path.join(hooksDir, hook)
		if not os.path.isdir(directory):
			if os.path.exists(directory):
				shutil.move(directory, directory + '.hook')
			os.mkdir(directory)
			if os.path.exists(directory + '.hook'):
				shutil.move(directory + '.hook', directory)

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