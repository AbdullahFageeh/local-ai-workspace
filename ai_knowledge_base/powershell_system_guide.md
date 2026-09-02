# PowerShell & Windows System Administration Guide

## Process Management
- Check running processes: `Get-Process -Name "<process_name>"`
- Terminate process: `Stop-Process -Name "<process_name>" -Force`
- Start background process: `Start-Process -FilePath "<exe>" -ArgumentList "<args>" -WindowStyle Hidden`

## Network & Port Diagnostics
- Check active listening ports: `Get-NetTCPConnection -State Listen | Select-Object LocalAddress, LocalPort, OwningProcess`
- Test port connectivity: `Test-NetConnection -ComputerName localhost -Port 8080`

## Environment & Path Operations
- Get persistent machine path: `[System.Environment]::GetEnvironmentVariable("Path", "Machine")`
- Refresh active PowerShell session path: `$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")`
