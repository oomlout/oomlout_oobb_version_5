@echo off
setlocal
if defined OOBB_PYTHON (
  "%OOBB_PYTHON%" "%~dp0presentation\scripts\catalogue.py" %*
) else (
  python "%~dp0presentation\scripts\catalogue.py" %*
)
exit /b %errorlevel%
