$venvName = ".venv"
$requirementsFile = "requirements.txt"
$mainScript = "Main.py"

try {
    $null = python --version
} catch {
    Write-Output "Error: Python is not installed or not in PATH"
    exit 1
}

if (-Not (Test-Path -Path $venvName)) {
    Write-Output "Creating virtual environment..."
    python -m venv $venvName
} else {
    Write-Output "Virtual environment already exists."
}

Write-Output "Activating virtual environment..."
. "$venvName\Scripts\Activate.ps1"

try {
    $null = pip --version
} catch {
    Write-Output "Error: pip is not installed or not in PATH"
    exit 1
}

try {
    $null = pyinstaller --version
} catch {
    Write-Output "Installing PyInstaller..."
    pip install pyinstaller
}

if (Test-Path -Path $requirementsFile) {
    Write-Output "Installing dependencies..."
    pip install -r $requirementsFile
} else {
    Write-Error "requirements.txt not found."
}

Write-Output "Building executable with PyInstaller..."
pyinstaller --onefile --windowed --name "DromParser" --icon=static/icon.ico --add-data="static/icon.ico;static" --add-data="static/notification.wav;static" --hidden-import=bs4 --hidden-import=requests --collect-all=bs4 --collect-all=requests --collect-all=dataclasses $mainScript

Write-Output "Build process completed."