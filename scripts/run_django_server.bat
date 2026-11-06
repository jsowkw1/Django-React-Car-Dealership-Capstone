@echo off
title Django Development Server
cd /d "%~dp0..\server"
echo (venv) %CD%^> python manage.py runserver 8000
"%~dp0..\.venv\Scripts\python.exe" manage.py runserver 8000
