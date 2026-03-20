@echo off
title Sigma Web Dev - Auto Starter

REM --- CRITICAL: USER'S EXACT DIRECTORY ---
set "PROJECT_ROOT=C:\Users\samsm\OneDrive\Desktop\RAG-Based-Ai-Teaching-Assistant-main\RAG-Based-Ai-Teaching-Assistant-main"
set "NODE_PATH=C:\Program Files\nodejs"

REM --- ADD NODE TO PATH ---
set "PATH=%PATH%;%NODE_PATH%"

echo ===========================================
echo        STARTING SIGMA AI ASSISTANT
echo ===========================================
echo Project Root: %PROJECT_ROOT%
echo.

REM ---------- START SIGMA BACKEND ----------
echo Starting Sigma Backend (FastAPI @8000)...
cd /d "%PROJECT_ROOT%"
REM Using --host 0.0.0.0 to fix "Could not connect" errors (IPv4 vs IPv6)
start "Sigma Backend" cmd /k "python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000"
echo.

REM ---------- WAIT ----------
timeout /t 3 >nul

REM ---------- START SIGMA FRONTEND ----------
echo Starting Sigma Frontend (Vite @5173)...
cd /d "%PROJECT_ROOT%\sigma-assistant"
start "Sigma Frontend" cmd /k "npm run dev -- --port 5173"
echo.

REM ---------- OPEN BROWSER ----------
echo Opening Sigma Web App...
start http://localhost:5173

echo ===========================================
echo     SIGMA AI ASSISTANT IS RUNNING! 🚀
echo ===========================================

pause
