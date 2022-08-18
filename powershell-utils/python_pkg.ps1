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
    $PythonPackageName = GetPythonPackageName
    $PyprojectTomlData = Get-Content -Path $PythonPackageName\pyproject.toml
    # There are many versions in this file so we have to match this one specifically
    $TomlPrefix = 'version = "'
    $PyprojectTomlData = $PyprojectTomlData.Replace($TomlPrefix + $VersionRegex, $TomlPrefix + $NewVersionString)
    Set-Content -Path $PythonPackageName\pyproject.toml -Value $PyprojectTomlData
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