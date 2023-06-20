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