"""Dataclass to provide structure for constructing PowerShell profiles."""
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class PwshInclude:
    """Include dataclass: no inputs, no commands, fixed output."""
    name: str
    str_out: str

@dataclass 
class PwshSetting:
    """Setting dataclass: one input, no commands, one non-command output."""
    name: str
    input: Dict


    @property
    def str_out(self) -> str:
        """Return the output string for this `PwshSetting`."""
        raise NotImplementedError
    
@dataclass 
class PwshCommand:
    """Command dataclass: one input (alias), one command, no non-command outputs."""
    command_name: str
    command_args: List[str]
    command_body: str
    command_doc: str = None
    indent_body: bool = True
    alias: str = None

    def get_command(self) -> str:
        """Get the command string for this `PwshCommand`."""
        if self.indent_body:
            command_lines = self.command_body.split("\n")
            command_lines = [f"\t{line}" for line in command_lines]
            command_lines = "\n".join(command_lines)
        else:
            command_lines = self.command_body
        if self.command_doc:
            command_lines = f"<# {self.command_doc} #>\n{command_lines}"
        return (
            f"function {self.command_name} ({', '.join(self.command_args)}) {{\n"
            f"{self.command_lines}\n"
            f"}}\n"
        )

    @property
    def str_out(self) -> str:
        """Return the output string for this `PwshCommand`."""
        alias_str = f"Set-Alias -Name {self.alias} -Value {self.command_name}\n" if self.alias else ""
        return f"{self.get_command()}{alias_str}"

@dataclass 
class PwshTemplate:
    """Template dataclass: 0-n inputs, 0-n command outputs, 0-n non-command outputs."""
    name: str
    input: Dict[str, str]

    