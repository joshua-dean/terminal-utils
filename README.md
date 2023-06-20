# terminal-utils
General utilites for bash, powershell, AWS CLI, etc.

Currently only Powershell configurations get built, but support for other terminal configurations could be added using the same command and configuration structure.

There are `commands`, which simply include a script (and optionally aliases), and `templates`, which generate a script from their configuration object.

Configuration is a JSON object that gets passed to `script_builder.py`.

The configuration builds a powershell script to a specified filename, and this can be used as a Powershell profile script.

## Configuration
The configuration is currently very loosely defined and will change in the future.
The configuration is a JSON object with the following structure:

```
{
    "commands": [ 
        {
            "script_name": "script_name.ps1",
            "aliases": {
                "alias1": "alias1_value",
                "alias2": "alias2_value"
            }
        }
    ],
    "templates": [
        {
            "str_out": python_fn(args),
            "aliases": [
                "alias1",
                "alias2"
            ]
        }
    ],
    "output": "output/path/script_name.ps1"
}
```
Where `script_name` refers to a script in `powershell_utils`, and `str_out` is a string that will be written to a file.
This currently requires the JSON to get written programmatically within `script_builder.py`, so in the future the `templates` section might take on this format:
```
{
    "templates": [
        {
            "template": "template_name.py",
            "args": {
                "arg1": "value1",
                "arg2": "value2"
            }
            "aliases": {
                "alias1": "alias1_value",
                "alias2": "alias2_value"
            }
        }
    ]
}
```

## Commands
The script files to contain additional utility functions, which are not listed here.
The following notable commands can be included:

[//]: # (Make a table)

| Command | Script Name | Description |
| ------- | ----------- | ----------- |
| `RunCommandAtInterval` | `command_utils.ps1` | Runs a command at a specified interval (in seconds). |
| `PythonPkgBumpMinor` | `python_pkg.ps1` | Bumps the minor version of a python package. |
| `PythonPkgBumpPatch` | `python_pkg.ps1` | Bumps the patch version of a python package. |
| `PostPRCleanup` | `git_utils.ps1` | Cleans up a branch after a PR is merged. Checks out master, deletes all merged refs, and prunes `origin`. |

## Templates
Templates are intended to make commands programmatically, usually to extend similar logic to different aliases.

### EC2 SSH
This generates commands to manage EC2 instances. Given an `instance_name`, `instance_id`, `username`, and optionally a `pemfile_path`, it will yield the following commands:
```
Get{instance_name}Ip
Start{instance_name}
Stop{instance_name}
SSH{instance_name}
```
To get the IP of, start, stop, and ssh into the instance, respectively.
