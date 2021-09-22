$ErrorActionPreference = "Stop"

function Invoke-Check([string]$command, [string]$taskName)
{
    cmd.exe /c $command

    if ($LASTEXITCODE -ne 0)
    {
        Write-Error "Error @ ${taskName}"
        Read-Host
        Exit 1
    }
}

# Check for `dlparse`

Write-Host "Checking with pydocstyle..." -Fore Cyan
Invoke-Check "pydocstyle dlparse --count" "pydocstyle (dlparse)"

Write-Host "Checking with flake8..." -Fore Cyan
Invoke-Check "flake8 dlparse --count" "flake8 (dlparse)"

Write-Host "Checking with bandit..." -Fore Cyan
Invoke-Check "bandit -r dlparse" "bandit (dlparse)"

Write-Host "Checking with pylint..." -Fore Cyan
Invoke-Check "pylint dlparse" "pylint (dlparse)"

# Check for `tests.utils`

Write-Host "Checking with pydocstyle..." -Fore Cyan
Invoke-Check "pydocstyle tests.utils --count" "pydocstyle (test utils)"

Write-Host "Checking with flake8..." -Fore Cyan
Invoke-Check "flake8 tests/utils --count" "flake8 (test utils)"

Write-Host "Checking with bandit..." -Fore Cyan
Invoke-Check "bandit -r tests/utils" "bandit (test utils)"

Write-Host "Checking with pylint..." -Fore Cyan
Invoke-Check "pylint tests.utils" "pylint (test utils)"

# Code Tests

Write-Host "Running code tests..." -Fore Cyan
Invoke-Check "pytest --all" "code test"

# (Completed)

Write-Host "--- All checks passed. ---" -Fore Green
Write-Host "Press any key to continue."
Read-Host
