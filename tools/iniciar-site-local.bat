@echo off
cd /d "%~dp0.."
echo Iniciando servidor em http://localhost:8080/
python tools/serve-local.py
