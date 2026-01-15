import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file relative to the working directory with optional arguments and captures its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            # "args": types.Schema(
            #     type=types.Type.ARRAY,
            #     items=types.Schema(type=types.Type.STRING),
            #     description="Optional list of arguments to pass to the Python file",
            # ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'"{file_path}" does not exist or is not a regular file'
        
        if not target_file.endswith('.py'):
            return f'"{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
            
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if result.stdout or result.stderr:
            if result.stdout:
                output += f"STDOUT: {result.stdout}\n"
            if result.stderr:
                output += f"STDERR: {result.stderr}\n"
        else:
            output += "No output produced\n"
        
        return output.rstrip()
        
    except Exception as e:
        return f"Error: executing Python file: {e}"