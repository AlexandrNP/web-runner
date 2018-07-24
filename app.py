#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, jsonify
from flask import abort
from flask import url_for
from flask import request

import os
import sys
import json
import base64
from subprocess import Popen, PIPE
from toolconfig import ToolConfig

app = Flask(__name__)

CONFIG = None
CONFIG_FILE = 'config'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


#Creates input filr in tool directory
@app.route('/api/input', methods=['POST'])
def create_input_file():
	global CONFIG
	eprint(request.json)
	if not request.json or not 'file' in request.json:
		abort(400)
	if not 'name' in request.json['file'] or not 'content' in request.json['file']:
		abort(400)
	file_name = os.path.join(CONFIG.get_tool_dir(), CONFIG.get_input_dir(), request.json['file']['name'])
	with open(file_name, 'w') as text_file:
		content = request.json['file']['content']
		text_file.write(content.decode('base64'))
	return jsonify({'File created': True}), 200
	

def setup_environment():
	global CONFIG 
	conf_success = config()
	INPUT_DIR = os.path.join(CONFIG.get_tool_dir(), CONFIG.get_input_dir())
	OUTPUT_DIR = os.path.join(CONFIG.get_tool_dir(), CONFIG.get_output_dir())
	if not os.path.isdir(INPUT_DIR):
		os.system('mkdir {}'.format(INPUT_DIR))
	if not os.path.isdir(OUTPUT_DIR):
		os.system('mkdir {}'.format(OUTPUT_DIR))

def clean_environment():
	global CONFIG 
	INPUT_DIR = os.path.join(CONFIG.get_tool_dir(), CONFIG.get_input_dir())
	OUTPUT_DIR = os.path.join(CONFIG.get_tool_dir(), CONFIG.get_output_dir())
	if os.path.isdir(INPUT_DIR):
		os.system('rm -rf {}'.format(INPUT_DIR))
	if os.path.isdir(OUTPUT_DIR):
		os.system('rm -rf {}'.format(OUTPUT_DIR))

#@app.route('/api/config', methods=['POST'])
def config():
	global CONFIG 
	if CONFIG is None:
		CONFIG = ToolConfig()
	config_file = open(CONFIG_FILE, 'r')
	file_json = json.load(config_file)
	#if not request.json:
	#	abort(400)
	if not 'config' in file_json:
		raise ValueError("""'config' is a required field in configuration file""")
	config_json = file_json['config']
	#config_json = request.json['config']
	if not 'tool' in config_json:
		raise ValueError("""'tool' is a required field in configuration file""")
	if not 'tool-dir' in config_json:
		raise ValueError("""'tool-dir' is a required field in configuration file""")
	if not 'executor' in config_json:
		raise ValueError("""'executor' is a required field in configuration file""")
	if not 'runfile' in config_json:
		raise ValueError("""'runfile' is a required field in configuration file""")
	if not 'input-file-names' in config_json:
		raise ValueError("""'input-file-names' is a required field in configuration file""")
	if not 'output-file-names' in  config_json:
		raise ValueError("""'output-file-names' is a required field in configuration file""")
	CONFIG.set_tool_name(config_json['tool'])
	CONFIG.set_tool_dir(config_json['tool-dir'])
	CONFIG.set_executor(config_json['executor'])
	CONFIG.set_runfile(config_json['runfile'])
	CONFIG.set_input_files(config_json['input-file-names'])
	CONFIG.set_output_files(config_json['output-file-names'])
	CONFIG.set_input_dir(config_json.get('input-dir', 'input'))
	CONFIG.set_output_dir(config_json.get('outputi-dir', 'output'))
	return True


def get_tool_output():
	global CONFIG
	output = {'output': {}}
	output_dir = os.path.join(CONFIG.get_tool_dir(), CONFIG.get_output_dir())
	output_file_names = os.listdir(output_dir)
	for fname in output_file_names:
		f = open(os.path.join(output_dir, fname), 'r')
		content = f.read()
		output['output'][fname] = content.encode('base64')
	return output

	
@app.route('/api/run')
def run_tool():
	global CONFIG
	run_tool_command_tokenized = CONFIG.get_run_command_tokenized()
	cur_dir = os.getcwd()
	tool_dir = CONFIG.get_tool_dir()
	os.chdir(tool_dir)
	eprint(run_tool_command_tokenized)
	eprint(CONFIG.get_output_files())
	shell_output = Popen(run_tool_command_tokenized, stdout=PIPE, stderr=PIPE)
	eprint(shell_output.stderr.read())
	eprint(shell_output.stdout.read())
	os.chdir(cur_dir)
	#clean_environment()

	return jsonify(get_tool_output())


if __name__ == '__main__':
	setup_environment()
	app.run(debug=True)
	#if CONFIG is not None:
	#	clean_environment()
