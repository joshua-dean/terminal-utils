# Utilities for python packages in Powershell 

# Globals
$Global:VersionRegex = '(?<major>\d+)\.(?<minor>\d+)\.(?<patch>\*|\d+)';

function VersionToString($MajorVer, $MinorVer, $PatchVer) {
    # Convert a version to a string
    Return $MajorVer.ToString() + "." + $MinorVer.ToString() + "." + $PatchVer.ToString()
}

function GetPythonPackageName {
    # Get the name of a python package in the current directory
    $PythonVersionFile = Get-ChildItem -Path . -Include _version.py -Depth 1 | Select-Object -First 1
    Return $PythonVersionFile.Directory.Name
}

function GetPythonPackageVersion { 
    # Get the version of a python package in the current directory
    $PythonPackageName = GetPythonPackageName
    $VersionFileData = Get-Content -Path $PythonPackageName\_version.py
    $RegexMatches = $VersionFileData | Select-String -Pattern $VersionRegex
    $MajorVer = [int]$RegexMatches.Matches.Groups[1].Value
    $MinorVer = [int]$RegexMatches.Matches.Groups[2].Value
    $PatchVer = [int]$RegexMatches.Matches.Groups[3].Value
    Return $MajorVer, $MinorVer, $PatchVer
}

function ApplyNewVersionToVersionFile($NewVersionString) { 
    # Apply a new version to the version file
    $PythonPackageName = GetPythonPackageName
    $VersionFileData = Get-Content -Path $PythonPackageName\_version.py
    $VersionFileData = $VersionFileData.Replace($VersionRegex, $NewVersionString)
    Set-Content -Path $PythonPackageName\_version.py -Value $VersionFileData
}

function ApplyNewVersionToPyprojectToml($NewVersionString) { 
    # Apply a new version to the pyproject.toml file
    $PyprojectTomlData = Get-Content -Path pyproject.toml
    # There are many versions in this file so we have to match this one specifically
    $TomlPrefix = 'version = "'
    $PyprojectTomlData = $PyprojectTomlData.Replace($TomlPrefix + $VersionRegex, $TomlPrefix + $NewVersionString)
    Set-Content -Path pyproject.toml -Value $PyprojectTomlData
}

function PythonPkgBumpMinor { 
    # Bump the minor version of a python package in the current directory
    $PythonPackageVersion = GetPythonPackageVersion

    $NewVersionString = VersionToString($PythonPackageVersion[0], $PythonPackageVersion[1] + 1, 0)
    ApplyNewVersionToVersionFile($NewVersionString)
    ApplyNewVersionToPyprojectToml($NewVersionString)
}

function PythonPkgBumpPatch { 
    # Bump the patch version of a python package in the current directory
    $PythonPackageVersion = GetPythonPackageVersion

    $NewVersionString = VersionToString($PythonPackageVersion[0], $PythonPackageVersion[1], $PythonPackageVersion[2] + 1)
    ApplyNewVersionToVersionFile($NewVersionString)
    ApplyNewVersionToPyprojectToml($NewVersionString)
}
Set-Alias -Name bump-minor -Value PythonPkgBumpMinor
Set-Alias -Name bump-patch -Value PythonPkgBumpPatch

# Utilities for running commands.

function RunCommandAtInterval ($Fn, $IntervalMins) {
    # Run the given function every $IntervalMins minutes.
    $IntervalSeconds = $IntervalMins * 60;
    Write-Output "Running command every $IntervalSeconds seconds.";
    while ($True) {
        $Fn;
        Start-Sleep -Seconds $IntervalSeconds;
    }
}
Set-Alias -Name run-command-at-interval -Value RunCommandAtInterval

# Utilities for Git CLI

function PostPRCleanup{
    # Cleans up local git after a PR or other merge on remote.
    if (git branch --list 'master') {
        git checkout master
    }
    else {
        git checkout main
    }
    git pull 
    $Merged = git branch --merged
    $Lines = $Merged -Split '\n'
    foreach($Line in $Lines) { 
        if ($Line -Match '\*' -or $Line -Match 'master') { 
            continue 
        }
        $Line = $Line -Replace '\s', ''
        git branch -d $Line
    }
    git remote prune origin
}
Set-Alias -Name git-cleanup -Value PostPRCleanup

    function GetMyEC2InstanceIp {        aws ec2 describe-instances --instance-ids i-0c8f8f8f8f8f8f8f8 --query 'Reservations[0].Instances[0].PublicIpAddress' --output text    }    function StartMyEC2Instance {        aws ec2 start-instances --instance-ids i-0c8f8f8f8f8f8f8f8    }    function StopMyEC2Instance {        aws ec2 stop-instances --instance-ids i-0c8f8f8f8f8f8f8f8    }    function SSHMyEC2Instance {        ssh  ec2-user@{GetMyEC2InstanceIp}    }
Set-Alias -Name get-my-ec2-ip -Value GetMyEC2InstanceIp
Set-Alias -Name start-my-ec2-instance -Value StartMyEC2Instance
Set-Alias -Name stop-my-ec2-instance -Value StopMyEC2Instance
Set-Alias -Name ssh-my-ec2-instance -Value SSHMyEC2Instance