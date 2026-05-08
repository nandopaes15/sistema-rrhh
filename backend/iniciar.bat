@echo off
title Sistema RRHH - Backend
cd /d "%~dp0"

echo.
echo  ================================
echo   Sistema RRHH - Iniciando...
echo  ================================
echo.

call venv\Scripts\activate.bat

echo  Backend corriendo en http://localhost:8000
echo  Documentacion en   http://localhost:8000/docs
echo  Presiona CTRL+C para detener.
echo.

uvicorn main:app --reload
