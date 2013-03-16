gitHookManager
==============

Store your git hooks inside the repository.

Requires python (tested only on 2.7)

Installation:

run: `git clone git://github.com/legion0/gitHookManager.git && cd gitHookManager && chmod +x ./setup.py && ./setup.py install`.

This will install the `git-hooks` command.

To install the functionality into a specific repository run `git hooks install` in the repository directory.

Run `git hooks help` for more info.


NOTE: as this is still in development there are some printed messages even when all works fine.
This is to show that the hooks are actually called when needed.
The output will be removed later on but you can remove it now by changing PRINT_RUN_MESSAGES to False in the script and reinstall.


Enjoy, and please report bugs or feature requests :)