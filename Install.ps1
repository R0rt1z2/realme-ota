#
# PowerShell displays error messages regardless of whether you redirect it whatever you're executing to null.
# To prevent this from happening, disable all the output(s) by using PowerShell's default variables.
#
$ProgressPreference    = 'SilentlyContinue'
$ErrorActionPreference = 'SilentlyContinue'

#
# There is no built-in function to update the (global) Windows env %PATH%. Instead, use this function to update
# the registry directly (https://stackoverflow.com/a/69239861).
#

function Add-Path {
  param(
    [Parameter(Mandatory, Position=0)]
    [string] $LiteralPath,
    [ValidateSet('User', 'CurrentUser', 'Machine', 'LocalMachine')]
    [string] $Scope 
  )

  Set-StrictMode -Version 1; $ErrorActionPreference = 'Stop'

  $isMachineLevel = $Scope -in 'Machine', 'LocalMachine'
  if ($isMachineLevel -and -not $($ErrorActionPreference = 'Continue'; net session 2>$null)) { throw "You must run AS ADMIN to update the machine-level Path environment variable." }  

  $regPath = 'registry::' + ('HKEY_CURRENT_USER\Environment', 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment')[$isMachineLevel]

  $currDirs = (Get-Item -LiteralPath $regPath).GetValue('Path', '', 'DoNotExpandEnvironmentNames') -split ';' -ne ''

  if ($LiteralPath -in $currDirs) {
    return
  }

  $newValue = ($currDirs + $LiteralPath) -join ';'

  Set-ItemProperty -Type ExpandString -LiteralPath $regPath Path $newValue

  $dummyName = [guid]::NewGuid().ToString()
  [Environment]::SetEnvironmentVariable($dummyName, 'foo', 'User')
  [Environment]::SetEnvironmentVariable($dummyName, [NullString]::value, 'User')

  $env:Path = ($env:Path -replace ';$') + ';' + $LiteralPath
}

#
# Function to remove items from PATH
#

function Remove-Path {
  param(
    [Parameter(Mandatory, Position=0)]
    [string] $LiteralPath,
    [ValidateSet('User', 'CurrentUser', 'Machine', 'LocalMachine')]
    [string] $Scope 
  )

  Set-StrictMode -Version 1; $ErrorActionPreference = 'Stop'

  $isMachineLevel = $Scope -in 'Machine', 'LocalMachine'
  if ($isMachineLevel -and -not $($ErrorActionPreference = 'Continue'; net session 2>$null)) { throw "You must run AS ADMIN to update the machine-level Path environment variable." }  

  # Get PATH
  $path = [System.Environment]::GetEnvironmentVariable(
      'PATH',
      'User'
  )

  # Remove only unwanted elements
  $path = ($path.Split(';') | Where-Object { ($_.TrimEnd('\') -ne $LiteralPath.TrimEnd('\')) } ) -join ';'
  
  # Set it
  [System.Environment]::SetEnvironmentVariable(
      'PATH',
      $path,
      'User'
  )

  # Refresh PATH
  $env:Path = [System.Environment]::GetEnvironmentVariable(
      'PATH',
      'User'
  )
}

#
# Helper cleanup function, calls Remove-Path function
#

function Cleanup {
  param(
    [Parameter(Mandatory, Position=0)]
    [string] $LiteralPath
  )

  if ($LiteralPath.EndsWith("realme-ota.bat")) {
      LogToConsole 4 "Removing obsolete realme-bat file...: $LiteralPath"   
      Remove-Item -Path $LiteralPath
  }
  
  $targetPath = $LiteralPath.TrimEnd('realme-ota.bat')
  if (($targetPath -match "realme-ota") -or ($targetPath -match "realme_ota")) {
      LogToConsole 4 "Removing directory from PATH...: $targetPath"
      Remove-Path $targetPath
  }
}


#
# Small logger. Includes color-like and symbol-like verbosity.
#   @param $verbosity: Logging verbosity (info, fail, success)
#   @param $logmessage: Message to print to the console.
#
function LogToConsole {
    Param
    (
        [Parameter(Mandatory = $true)] [int] $verbosity,
        [Parameter(Mandatory = $true)] [string] $logmessage
    )

    Switch ($verbosity) {
        1 {
            Write-Host "[?] $logmessage" -ForegroundColor White
        }
        2 {
            Write-Host "[-] $logmessage" -ForegroundColor Red
        }
        3 {
            Write-Host "[+] $logmessage" -ForegroundColor Green
        }
        4 {
            Write-Host "[!] $logmessage" -ForegroundColor Yellow
        }
        default {
            Write-Host "[~] $logmessage" -ForegroundColor Gray
        }
    }
}

#
# We need special privilegies to install the script globally, if we don't have them, bail out.
#
$per = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-Not $per.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    LogToConsole 2 "You need privilegies to execute this script!"
} else {
  #
  # For some reason, Windows 10 (and 11) include different aliases that are used with priority when one
  # of the defined keywords is detected. These include python and python3. By default, these aliases cause
  # the Windows Store to open regardless of whether Python is installed or not. Since we can't really get
  # rid of the aliasses, delete the python(3) Store shortcuts so it uses the real python executables.
  #

  Remove-Item $env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe
  Remove-Item $env:LOCALAPPDATA\Microsoft\WindowsApps\python3.exe

  #
  # Python installer
  #

  if ([string]::IsNullOrEmpty((Get-Command python.exe).Path)) {
      LogToConsole 4 "Python is not installed!"
      LogToConsole 1 "Downloading python..."

      Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe -OutFile PythonSetup.exe

      if (-Not (Test-Path -Path PythonSetup.exe -PathType Leaf)) {
          LogToConsole 2 "Unable to download python!"
          exit 1
      }

      LogToConsole 1 "Installing python..."
      Start-Process -Wait -FilePath "PythonSetup.exe" -ArgumentList "InstallAllUsers=1 PrependPath=1 /quiet /log log.txt"
      
      try {
          $PythonPath = (Get-Command python.exe).Path.Replace("python.exe", "")
      }
      catch {
          LogToConsole 2 "Unable to install python (check log.txt for more details), please install manually!"
          exit 1
      }
      

      if (-Not ($env:Path.Contains("Python"))) {
          LogToConsole 4 "Adding python to the PATH..."
          Add-Path $PythonPath
      }

      LogToConsole 3 "Successfully installed python!"
  } else {
      LogToConsole 3 "Found $(python.exe --version) installed"
      $PythonPath = (Get-Command python.exe).Path.Replace("python.exe", "")
  }

  #
  # Pip installer
  #

  if ([string]::IsNullOrEmpty((Get-Command pip.exe).Path)) {
      LogToConsole 4 "Pip is not installed!"
      LogToConsole 1 "Downloading pip..."

      Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py. -OutFile get-pip.py

      if (!Test-Path -Path get-pip.py -PathType Leaf) {
          LogToConsole 2 "Unable to download pip!"
          exit 1
      }

      LogToConsole 1 "Installing pip..."
      Start-Process -Wait -FilePath "python.exe" -ArgumentList "get-pip.py"

      try {
          $PipPath = (Get-Command pip.exe).Path.Replace("pip.exe", "")
          
          if (-Not ($env:Path.Contains("Scripts"))) {
              LogToConsole 4 "Adding scripts to the PATH..."
              Add-Path $PipPath
          }
      }
      catch {
          LogToConsole 2 "Unable to install pip, please install manually!"
          exit 1
      }

      LogToConsole 3 "Successfully installed pip!"
  } else {
      LogToConsole 3 "Found $(pip.exe --version)installed"
      $PipPath = (Get-Command pip.exe).Path.Replace("pip.exe", "")
  }

  #
  # Dependencies install
  #

  LogToConsole 1 "Installing Python modules: Requests and Pycryptodome..."
  Start-Process -Wait -FilePath "python.exe" -ArgumentList "-m pip install requests pycryptodome"
  Rename-Item -Path $PythonPath + 'Lib\site-packages\crypto' -NewName "Crypto"


  #
  # Obsolete .bat and PATH cleanup
  # First pass removes .bat files found via CMD, second via PowerShell, third cleans PATH
  # Only paths that contain "realme-ota" or "realme_ota" will be removed from PATH
  #

  [bool]$cleanup = 0
  LogToConsole 1 "Checking for obsolete or invalid realme-ota files and PATH..."

  # First pass
  & cmd.exe /c cd %userprofile% "&" where realme-ota | ForEach-Object {
      
      if ($_ -match "realme-ota.bat") {
          $cleanup = 1
          Cleanup $_
      }
  }

  # Second pass
  & (Get-Command realme-ota).Path | ForEach-Object {

      if ($_ -match "realme-ota.bat") {
          $cleanup = 1
          Cleanup $_
      }
  }

  # Third pass - check PATH

  $env:Path.Split(';') | ForEach-Object {
      
      if (($_ -match "realme-ota") -or ($_ -match "realme_ota")) {
          $cleanup = 1
          Cleanup $_
      }
  }

  if ($cleanup -eq 1) {
      LogToConsole 4 "Cleanup completed. You may need to remove obsolete directories manually."
  }
  else {
      LogToConsole 3 "No cleanup required."
  }


  #
  # Download Realme-Ota package from Github and extract to \Scripts\
  #

  if ([string]::IsNullOrEmpty($PipPath)) {
      LogToConsole 2 "Pip path Python*\Scripts could not be found. Aborting..."
      exit 1
  }
  else {
      cd $PipPath
  }

  $oldPath = $PipPath + 'realme-ota\'
  if (Test-Path $oldPath) {
      LogToConsole 1 "Found previous realme-ota install in $oldPath"
      do {
          $confirmation = Read-Host "Do you want to remove previous realme-ota folder? [y/n]"
          $confirmation = $confirmation.ToLower()
      }
      until (($confirmation -eq 'y') -or ($confirmation -eq 'n'))

      if ($confirmation -eq 'y') {
          Remove-Item $oldPath -Recurse -Force
          LogToConsole 3 "Previous realme-ota was removed."
      }
  }

  LogToConsole 4 "Downloading realme-ota..."
  Invoke-WebRequest -Uri https://github.com/R0rt1z2/realme-ota/archive/refs/heads/master.zip -OutFile dist.zip

  


  LogToConsole 4 "Extracting realme-ota..."
  Expand-Archive dist.zip -DestinationPath realme-ota -Force; rm -Force dist.zip

  LogToConsole 4 "Copying files..."
  mv -Force realme-ota\realme-ota-master\* realme-ota\; rm -Force realme-ota\realme-ota-master


  #
  # Wrapper directory updater
  # Replaces 'cd' in .bat file with path to where main.py is located
  #

  $RealmeOtaPath = $PipPath + 'realme-ota\realme_ota\'
  $file = $RealmeOtaPath + 'realme-ota.bat'
  $regex = 'cd\s"[^"]*"'
  $target = 'cd ' + '"' + $RealmeOtaPath + '"'
  
  try {
      (Get-Content $file) -replace $regex, $target | Set-Content $file
      LogToConsole 3 "Adjusted working directory in the realme-ota.bat to $target"
  }
  catch {
      LogToConsole 2 "Failed to access realme-ota.bat file. Make sure the file exists and is in correct location of $PipPath\realme_ota\"
      exit 1
  }
  
  #
  # Add realme-ota.bat to PATH
  #

  if ([string]::IsNullOrEmpty((Get-Command realme-ota).Path)) {
      
      if (-Not ($env:Path.Contains("realme-ota"))) {
          LogToConsole 1 "Adding realme-ota to PATH..."
          Add-Path $RealmeOtaPath
      }

  } else {
      LogToConsole 3 "Found realme-ota in PATH already"
  }

  # Test if Windows finds .bat
  try {
      $BatPath = (Get-Command realme-ota).Path.Replace("realme-ota.bat", "")
      LogToConsole 3 "Successfully installed realme-ota!"
      LogToConsole 3 "Realme-ota was installed in $BatPath"
  }
  catch {
      LogToConsole 2 "Realme-ota failed to be added to PATH, or Windows can't locate .bat file"
      exit 1
  }

  cd ~
}

pause; exit 0
