
param(
    [Parameter()]
    [String]$env_name  = "<env>",
    [String]$db_name   = "<db>"
)

# Usage: .\extensions.ps1 cosmos citus > tmp\extensions.txt

Write-Output "extensions"
.\psql.ps1 $env_name $db_name psql\extensions.sql
