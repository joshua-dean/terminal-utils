"""Configuration for external powershell modules."""


def posh_git():
    """Posh-git configuration."""
    cmd_str = "# Posh-git\n"
    cmd_str += """$poshGitModule = Get-Module posh-git -ListAvailable | Sort-Object Version -Descending | Select-Object -First 1
if ($poshGitModule) {
    $poshGitModule | Import-Module
}
elseif (Test-Path -LiteralPath ($modulePath = Join-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) (Join-Path src 'posh-git.psd1'))) {
    Import-Module $modulePath
}
else {
    throw "Failed to import posh-git."
}
"""
    return cmd_str
