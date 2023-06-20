"""Build .ps1 file for use."""
from powershell_utils.templates.ec2_ssh import get_ec2_ssh_fns
from powershell_utils.modules.pwsh_settings import set_vi_bindings, set_intellisense_bindings
from powershell_utils.modules.external_modules import posh_git

if __name__ == "__main__":
    # loosely defined for now
    config = { 
        "commands": [ 
            {
                "script_name": "python_pkg.ps1",
                "aliases": {
                    "bump-minor": "PythonPkgBumpMinor",
                    "bump-patch": "PythonPkgBumpPatch",
                },
            },
            { 
                "script_name": "command_utils.ps1",
                "aliases": {
                    "run-command-at-interval": "RunCommandAtInterval",
                }, 
            },
            {
                "script_name": "git_utils.ps1",
                "aliases": {
                    "git-cleanup": "PostPRCleanup",
                }
            }
        ],
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
        for module in config["modules"]:
            cmd_str, command_names = module["str_out"]
            output_fd.write(cmd_str)
        for command in config["commands"]:
            with open(f"powershell_utils/commands/{command['script_name']}", "r") as script_fd:
                output_fd.write(script_fd.read())
                for alias, command in command["aliases"].items():
                    output_fd.write(f"\nSet-Alias -Name {alias} -Value {command}")
                output_fd.write("\n\n")
        for template in config["templates"]:
            cmd_str, command_names = template["str_out"]
            output_fd.write(cmd_str)
            for alias in template["aliases"]:
                output_fd.write(f"\nSet-Alias -Name {alias} -Value {command_names[template['aliases'].index(alias)]}")
    