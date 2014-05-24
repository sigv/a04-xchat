# License: The MIT License
# Project: https://github.com/sigv/a04-xchat

# Modify the following line to represent the location of the a04 project
projectpath = '/home/user/a04'

__module_name__ = 'a04'
__module_version__ = '0.1.0'
__module_description__ = 'Provides simple a04 decoding and encoding support on the run'

import xchat

import os
os.sys.path.append(projectpath)

encode = None
decode = None
try:
	from encoder import encode
	from decoder import decode
except ImportError:
	print('Unable to import the main a04 project. Did you set the path?')

def command_cb(word, word_eol, userdata):
	msg = None
	key = None
	hashsys = 'sha1'
	say = False
	sayloud = False

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
		if cmd == 'say ':
			say = True
		if cmd == 'loud ':
			sayloud = True

	if msg is None:
		xchat.prnt('You must specify a message to ' + act + ': /a04 ' + act + ' --msg <msg>')
		return xchat.EAT_ALL
	if key is None:
		xchat.prnt('You must specify a key to ' + act + ': /a04 ' + act + ' --key <key>')
		return xchat.EAT_ALL

	if act == 'encode':
		out = ' '.join(encode(msg, key, hashsys))
		if say:
			if sayloud:
				xchat.get_context().command('say ' + hashsys + ' | ' + key + ' | ' + out)
			else:
				xchat.get_context().command('say ' + out)
		else:
			xchat.prnt('encoded message: ' + out)
	if act == 'decode':
		out = decode(msg, key, hashsys)
		if say:
			xchat.get_context().command('say decoded message: ' + out);
		else:
			xchat.prnt('decoded message: ' + out)

	return xchat.EAT_ALL

if encode is not None and decode is not None:
	xchat.hook_command('a04', command_cb, help='Usage: a04 encode|decode [--say [--loud]] --msg <msg> --key <key> [--hash <hash>], prints (or, if instructed to, says) the resulting message')
	print('a04 has been loaded successfully')

