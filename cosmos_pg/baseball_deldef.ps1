
param(
    [Parameter()]
    [String]$env_name  = "<env>",
    [String]$db_name   = "<db>"
)

# Usage: .\baseball_deldef.ps1 cosmos citus > tmp\baseball_deldef.txt

Write-Output "baseball_deldef"
.\psql.ps1 $env_name $db_name psql\baseball_deldef.sql
