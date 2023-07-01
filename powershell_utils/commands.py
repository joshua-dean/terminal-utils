"""Powershell command definitions."""
import re
from typing import Dict, List
from pathlib import Path

def get_command_name_from_raw_str(
    cmd_str: str
) -> str: 
    """Get the command name from a raw string."""
    # Remove any leading whitespace and newlines
    first_line = cmd_str.lstrip().split("\n")[0]
    cmd_name_regex = r"function\s+(?P<cmd_name>\w+)\s*[\(\{]"
    cmd_name_match = re.match(cmd_name_regex, first_line)
    if cmd_name_match:
        return cmd_name_match.group("cmd_name")
    else:
        return None

def get_alias_for_command(
    command_name: str,
    alias: str
) -> str:
    """Get an alias for a command."""
    return f"Set-Alias -Name {alias} -Value {command_name}\n"

def add_alias_to_command_str(
    command_str: str,
    command_name: str = None,
    alias: str = None
) -> str:
    """Add an alias to a command string."""
    if not alias:
        return command_str
    if not command_name:
        command_name = get_command_name_from_raw_str(command_str)
    
    if not command_str.endswith("\n"):
        command_str += "\n"
    
    alias_str = get_alias_for_command(command_name, alias)

    return f"{command_str}{alias_str}"

def indent_str(
    str_to_indent: str,
    indent: str = "\t",
): 
    """Indent a string."""
    return "\n".join([f"{indent}{line}" for line in str_to_indent.split("\n")]) + "\n"


def build_pwsh_command_str(
    cmd_name: str,
    cmd_body: str,
    cmd_args: List[str] = None,
    cmd_doc: str = None,
    alias: str = None
) -> str: 
    """Build a PowerShell command from given inputs."""
    arg_str = ", ".join(cmd_args) if cmd_args else ""

    doc_str = f"<# {cmd_doc} #>\n" if cmd_doc else ""
    cmd_body = f"{doc_str}{cmd_body}"

    cmd_str = f"function {cmd_name} ({arg_str}) {{\n{cmd_body}\n}}\n"
    return add_alias_to_command_str(cmd_str, cmd_name, alias)

def read_pwsh_command_str_from_file(
    pwsh_file_path: Path,
    strip_header_comments: bool = True
) -> str:
    """Read a PowerShell command string from a file."""
    with open(pwsh_file_path, "r") as pwsh_file:
        pwsh_str = pwsh_file.read()
    if strip_header_comments:
        pwsh_str = re.sub(r"^<#.*?#>\n", "", pwsh_str)
    
    return pwsh_str


def read_all_pwsh_commands_from_file(
    pwsh_file_path: Path,
) -> Dict[str, str]:
    """
    Read all PowerShell commands from a file.

    Returns a dictionary of command names to command strings.
    """
    pwsh_cmds = {}
    with open(pwsh_file_path, "r") as pwsh_file:
        pwsh_str = pwsh_file.read()
    
    function_regex = r"^function.*?\{.*?^\}"

    functions = re.findall(function_regex, pwsh_str, re.MULTILINE | re.DOTALL)
    for function in functions:
        function_name = get_command_name_from_raw_str(function)
        pwsh_cmds[function_name] = function + "\n"
    
    return pwsh_cmds



def get_all_pwsh_commands_from_dir(
    pwsh_dir_path: Path,
) -> Dict[str, str]:
    """Read all PowerShell commands from all files in a directory."""
    pwsh_cmds = {}
    for pwsh_file_path in pwsh_dir_path.glob("*.ps1"):
        pwsh_cmds.update(read_all_pwsh_commands_from_file(pwsh_file_path))
    
    return pwsh_cmds
