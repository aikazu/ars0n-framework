Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; $file = Get-Item -Path "docker-run.sh"; $file.IsReadOnly = $false
