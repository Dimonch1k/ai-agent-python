import os
import subprocess

from langchain_core.tools import tool


@tool
def execute_terminal_command(command: str) -> str:
	"""Executes a system shell command safely on the host machine and returns stdout/stderr.
	Use this to install packages, check system hardware details, list files, or execute automation commands.
	"""
	# Strict boundary safeguards to avoid complete data wiping catastrophes
	dangerous_keywords = ["rm -rf /", "mkfs", "dd if=", "shutdown", "reboot"]
	if any(k in command for k in dangerous_keywords):
		return "Error: Command explicitly rejected due to security policy violations."

	try:
		result = subprocess.run(
			command, shell=True, capture_output=True, text=True, timeout=30
		)
		output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
		return output if output.strip() else "Action completed successfully with empty output logs."
	except Exception as e:
		return f"Execution Failed Error: {str(e)}"


@tool
def manage_local_file(action: str, filepath: str, content: str = "") -> str:
	"""Manages files locally on the disk drive.
	Actions available: 'write' (creates/overwrites), 'read' (reads content), 'append' (adds text data).
	"""
	# 🛠️ SAFEGUARD: If the model provides a root path like "/system_info.log",
	# strip the leading slash to make it a local path "system_info.log" instead.
	if filepath.startswith("/"):
		filepath = filepath.lstrip("/")

	try:
		if action == "write":
			with open(filepath, "w", encoding="utf-8") as f:
				f.write(content)
			return f"Successfully created/wrote file to local project path: {filepath}"

		elif action == "read":
			if not os.path.exists(filepath):
				return f"Error: File paths structural check indicates {filepath} does not exist."
			with open(filepath, "r", encoding="utf-8") as f:
				return f"Content of {filepath}:\n{f.read()}"

		elif action == "append":
			with open(filepath, "a", encoding="utf-8") as f:
				f.write(content)
			return f"Successfully appended content to target path: {filepath}"

		else:
			return "Error: Unknown action selection. Pick from ['write', 'read', 'append']."
	except Exception as e:
		return f"File System Stream Modification Failed: {str(e)}"
