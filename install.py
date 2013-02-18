#!/usr/bin/env python
import os, sys, shutil, stat

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

HOOKS = [
	"applypatch-msg", "pre-applypatch", "post-applypatch",
	"pre-commit", "prepare-commit-msg", "commit-msg", "post-commit",
	"pre-rebase", "post-checkout", "post-merge", "pre-receive",
	"update", "post-receive", "post-update",
	"pre-auto-gc", "post-rewrite"
]

HOOK_TEMPLATE = """#!/usr/bin/env python
import os, hookManager
_, scriptName = os.path.split(__file__)
exit(hookManager.processHooks(scriptName))"""

def main(args):
	repoDir = os.getcwd()
	if not ".git" in os.listdir(repoDir):
		die('Not in a repository: ' + repoDir)
	hooksDir = os.path.join(repoDir, '.git', 'hooks')
	newHooksDir = os.path.join(repoDir, 'gitconfig', "hooks")
	if os.path.exists(newHooksDir):
		die("Cannot create new hooks directory: \"" + newHooksDir + "\", aborting.")
	
	if os.path.exists(os.path.join(hooksDir, 'hookManager.py')):
		# Do update only:
		for hook in HOOKS:
			oldHookPath = os.path.join(hooksDir, hook)
			with open(oldHookPath, "w") as f:
				f.write(HOOK_TEMPLATE)
			st = os.stat(oldHookPath)
			os.chmod(oldHookPath, st.st_mode | stat.S_IEXEC)
		exit(0)
	
	shutil.copy(os.path.join(SCRIPT_DIR, 'hookManager.py'), os.path.join(hooksDir, 'hookManager.py'))
	for hook in HOOKS:
		oldHookPath = os.path.join(hooksDir, hook)
		newHookDir = os.path.join(newHooksDir, hook)
		if not os.path.isdir(newHookDir):
			os.makedirs(newHookDir)
		if os.path.exists(oldHookPath):
			shutil.move(oldHookPath, os.path.join(newHookDir, hook + '.hook'))
		with open(oldHookPath, "w") as f:
			f.write(HOOK_TEMPLATE)
		st = os.stat(oldHookPath)
		os.chmod(oldHookPath, st.st_mode | stat.S_IEXEC)

def die(msg = None, exitcode = 1):
	if msg is not None:
		print >> sys.stderr, msg
	exit(exitcode)
	
if __name__=="__main__":
	main(sys.argv[1:])