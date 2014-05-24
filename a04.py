# License: The MIT License
# Project: https://github.com/sigv/a04-xchat

# Modify the following line to represent the location of the a04 project
runnables = '/home/user/a04'

__module_name__ = 'a04'
__module_version__ = '0.1.0'
__module_description__ = 'Provides simple a04 decoding and encoding support on the run'

import xchat
import subprocess

def command_cb(word, word_eol, userdata):
	msg = None
	key = None
	hashsys = 'sha1'

	if len(word) < 2:
		xchat.prnt('You must specify whether you want to encode or decode: /a04 encode|decode')
		return xchat.EAT_ALL

	act = word[1]
	if act != 'encode' and act != 'decode':
		xchat.prnt('You must specify whether you want to encode or decode: /a04 encode|decode')
		return xchat.EAT_ALL

	for cmd in ' '.join(word[2:]).split('--'):
		if cmd.startswith('msg '):
			msg = cmd[4:].strip()
		if cmd.startswith('key '):
			key = cmd[4:].strip()
		if cmd.startswith('hash '):
			hashsys = cmd[5:].strip()

	if msg is None:
		xchat.prnt('You must specify a message to ' + act + ': /a04 ' + act + ' --msg <msg>')
		return xchat.EAT_ALL
	if key is None:
		xchat.prnt('You must specify a key to ' + act + ': /a04 ' + act + ' --key <key>')
		return xchat.EAT_ALL

	try:
		output = subprocess.check_output([ runnables + '/' + act + 'r.py', '--msg=' + msg, '--key=' + key, '--hash=' + hashsys ])
	except OSError:
		xchat.prnt('Unable to run the executable. Did you set the runnable path?')
		return xchat.EAT_ALL
	output = filter(None, output.split('\n'))
	xchat.prnt(output[len(output) - 1]);

	return xchat.EAT_ALL

xchat.hook_command('a04', command_cb, help='Usage: a04 encode|decode --msg <msg> --key <key> [--hash <hash>], prints the resulting message')
print 'a04 has been loaded successfully'

