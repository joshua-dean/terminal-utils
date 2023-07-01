"""Build .ps1 file for use."""
from pathlib import Path
from powershell_utils.commands import get_alias_for_command, get_all_pwsh_commands_from_dir, read_all_pwsh_commands_from_file
from powershell_utils.templates.ec2_ssh import get_ec2_ssh_fns
from powershell_utils.modules.pwsh_settings import set_vi_bindings, set_intellisense_bindings
from powershell_utils.modules.external_modules import posh_git

if __name__ == "__main__":
    # loosely defined for now
    config = { 
        "command_dirs": [
            "powershell_utils/commands",
        ],
        "command_files": [],
        "aliases": {
            "bump-minor": "PythonPkgBumpMinor",
            "bump-patch": "PythonPkgBumpPatch",
            "run-command-at-interval": "RunCommandAtInterval",
            "git-cleanup": "PostPRCleanup"
        },
        "templates": [ 
            {
                "str_out": get_ec2_ssh_fns("MyEC2Instance", "i-0c8f8f8f8f8f8f8f8"),
                "aliases": [ 
                    "get-my-ec2-ip",
                    "start-my-ec2-instance",
                    "stop-my-ec2-instance",
                    "ssh-my-ec2-instance",
                ]
            }
        ],
        "modules": [
            {
                "str_out": set_vi_bindings(),
            },
            {
                "str_out": set_intellisense_bindings(
                    "Shift+Tab"
                )
            },
            {
                "str_out": posh_git(),
            }
        ],
        "output": "./demo.ps1",
    }

    with open(config["output"], "w") as output_fd:
        for command_dir in config["command_dirs"]:
            commands = get_all_pwsh_commands_from_dir(Path(command_dir))
            for command_name, command_str in commands.items():
                output_fd.write(command_str)
        for command_file in config["command_files"]:
            commands = read_all_pwsh_commands_from_file(Path(command_file))
            for command_name, command_str in commands.items():
                output_fd.write(command_str)
        for alias, command_name in config["aliases"].items():
            output_fd.write(get_alias_for_command(command_name, alias))
        for module in config["modules"]:
            cmd_str = module["str_out"]
            output_fd.write(cmd_str)
        for template in config["templates"]:
            cmd_str, command_names = template["str_out"]
            output_fd.write(cmd_str)
            for alias in template["aliases"]:
                output_fd.write(f"\nSet-Alias -Name {alias} -Value {command_names[template['aliases'].index(alias)]}")
    