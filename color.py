#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
GNU General Public License v3.0

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
'''

import sys

class Color(object):
	''' Helper object for easily printing colored text to the terminal. '''

	# Basic console colors
	colors = {
		'W' : '\033[0m',  # white (normal)
		'R' : '\033[31m', # red
		'G' : '\033[32m', # green
		'O' : '\033[33m', # orange
		'B' : '\033[34m', # blue
		'P' : '\033[35m', # purple
		'C' : '\033[36m', # cyan
		'GR': '\033[37m', # gray
		'D' : '\033[2m' ,  # dims current color. {W} resets.
		'BR' : '\033[1;31m', # red
		'BG' : '\033[1;32m', # green
		'BO' : '\033[1;33m', # orange
		'BB' : '\033[1;34m', # blue
		'BP' : '\033[1;35m', # purple
		'BC' : '\033[1;36m', # cyan
		'BGR': '\033[1;37m' # gray
	}

	# Helper string replacements
	replacements = {
		'{+}': ' {W}{D}[{W}{G}+{W}{D}]{W}',
		'{!}': ' {O}[{R}!{O}]{W}',
		'{?}': ' {W}[{C}?{W}]'
	}

	last_sameline_length = 0

	@staticmethod
	def p(text):
		'''
		Prints text using colored format on same line.
		Example:
			Color.p('{R}This text is red. {W} This text is white')
		'''
		sys.stdout.write(Color.s(text))
		sys.stdout.flush()
		if '\r' in text:
			text = text[text.rfind('\r')+1:]
			Color.last_sameline_length = len(text)
		else:
			Color.last_sameline_length += len(text)

	@staticmethod
	def pl(text):
		'''Prints text using colored format with trailing new line.'''
		Color.p('%s\n' % text)
		Color.last_sameline_length = 0

	@staticmethod
	def pe(text):
		'''Prints text using colored format with leading and trailing new line to STDERR.'''
		sys.stderr.write(Color.s('%s\n' % text))
		Color.last_sameline_length = 0

	@staticmethod
	def s(text):
		''' Returns colored string '''
		output = text
		for (key,value) in Color.replacements.items():
			output = output.replace(key, value)
		for (key,value) in Color.colors.items():
			output = output.replace('{%s}' % key, value)
		return output

	@staticmethod
	def clear_line():
		spaces = ' ' * Color.last_sameline_length
		sys.stdout.write('\r%s\r' % spaces)
		sys.stdout.flush()
		Color.last_sameline_length = 0

	@staticmethod
	def clear_entire_line():
		import os
		(rows, columns) = os.popen('stty size', 'r').read().split()
		Color.p('\r' + (' ' * int(columns)) + '\r')


if __name__ == '__main__':
	Color.pl('{R}Testing{G}One{C}Two{P}Three{W}Done')
	print(Color.s('{C}Testing{P}String{W}'))
	Color.pl('{+} Good line')
	Color.pl('{!} Danger')
