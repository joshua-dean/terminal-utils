"""Build .ps1 file for use."""

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
            }
        ],
        "output": "./test.ps1",
    }

    with open(config["output"], "w") as output_fd:
        for command in config["commands"]:
            with open(f"powershell-utils/{command['script_name']}", "r") as script_fd:
                output_fd.write(script_fd.read())
                for alias, command in command["aliases"].items():
                    output_fd.write(f"\nSet-Alias -Name {alias} -Value {command}")
                output_fd.write("\n\n")
    