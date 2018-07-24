import os

#def eprint(*args, **kwargs):
#    print(*args, file=sys.stderr, **kwargs)

		
class ToolConfig: 
	"""A class that contains all sufficient information to run tools (executables or script files) 	

	Attributes:
		tool_name_		 (Optional) Name of the tool
		tool_dir_		Working directory of the tool
		executor_		(Required for scripts) An interpreter that would execute script
		runfile_		 Name of the script file or executable
		input_files_	 Input files for the tool
		output_files_	 Files produced for the tool
		input_dir_	 	Path to the directory with input files
		output_dir_	 	Path to the directory with output files
	"""
	tool_name_ = None 
	tool_dir_ = None
	executor_ = None
	runfile_ = None
	input_files_ = None 
	output_files_ = None
	input_dir_ = ''
	output_dir_ = ''
	#input_file_param_ = ''
	#output_file_param_ = ''
	#params = [] 
	#execution_command_template_ = None 

	def __init__(self):
		pass

	def set_tool_name(self, name):
		self.tool_name_ = name

	def set_tool_dir(self, directory):
		self.tool_dir_ = directory

	def set_runfile(self, runfile):
		self.runfile_ = runfile

	def set_executor(self, executor):
		self.executor_ = executor

	def set_input_files(self, input_files):
		self.input_files_ = input_files

	def set_output_files(self, output_files):
		self.output_files_ = output_files

	def set_input_dir(self, input_dir):
		self.input_dir_ = input_dir		

	def set_output_dir(self, output_dir):
		self.output_dir_ = output_dir

	def get_run_command_tokenized(self): 
		input_files = [os.path.join(self.input_dir_, f) for f in self.input_files_]
		output_files = [os.path.join(self.output_dir_, f) for f in self.output_files_]
		return [self.executor_, self.runfile_] + input_files + output_files

	def get_output_files(self):
		output_files = self.output_files_#[os.path.join(self.output_dir_, f) for f in self.output_files_]
		return output_files

	def get_input_dir(self):
		return self.input_dir_

	def get_output_dir(self):
		return self.output_dir_

	def get_tool_dir(self):
		return self.tool_dir_
