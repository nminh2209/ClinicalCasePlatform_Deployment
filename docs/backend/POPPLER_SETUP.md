# Poppler Setup for PDF Preview

Poppler is required for embedding PDF attachments into case PDFs.

## Windows Installation

Poppler has been installed to: `C:\Users\ADMIN\poppler\poppler-24.08.0`

The binaries are located at: `C:\Users\ADMIN\poppler\poppler-24.08.0\Library\bin`

This path has been added to your system PATH.

## Verification

Test if poppler is working:
```bash
python -c "from pdf2image import convert_from_path; print('pdf2image is working!')"
```

## If Poppler is Missing

If you need to reinstall or install on another machine:

```powershell
$popplerUrl = "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip"
$output = "$env:TEMP\poppler.zip"
$extractPath = "$env:USERPROFILE\poppler"

Invoke-WebRequest -Uri $popplerUrl -OutFile $output
Expand-Archive -Path $output -DestinationPath $extractPath -Force

# Add to PATH (User environment variable)
$popplerBin = "$extractPath\poppler-24.08.0\Library\bin"
[Environment]::SetEnvironmentVariable("PATH", "$popplerBin;$([Environment]::GetEnvironmentVariable('PATH', 'User'))", "User")
```

Then restart your terminal/IDE.

## Alternative: Linux

```bash
sudo apt-get install poppler-utils  # Debian/Ubuntu
sudo yum install poppler-utils       # CentOS/RHEL
```

## Alternative: macOS

```bash
brew install poppler
```
