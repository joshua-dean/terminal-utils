# Git Tab completion via posh-git
# https://github.com/dahlbyk/posh-git/blob/70e44dc0c2cdaf10c0cc8eb9ef5a9ca65ab63dcf/profile.example.ps1
$poshGitModule = Get-Module posh-git -ListAvailable | Sort-Object Version -Descending | Select-Object -First 1
if ($poshGitModule) {
    $poshGitModule | Import-Module
}
elseif (Test-Path -LiteralPath ($modulePath = Join-Path (Split-Path $MyInvocation.MyCommand.Path -Parent) (Join-Path src 'posh-git.psd1'))) {
    Import-Module $modulePath
}
else {
    throw "Failed to import posh-git."
}