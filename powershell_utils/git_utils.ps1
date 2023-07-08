# Utilities for Git CLI

function PostPRCleanup{
    # Cleans up local git after a PR or other merge on remote.
    if (git branch --list 'master') {
        git checkout master
    }
    elseif (git branch --list 'main') {
        git checkout main
    }
    else {
        Write-Warning 'PostPRCleanup only supports an initial branch of either "master" or "main"'
        return
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