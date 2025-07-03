@echo off
REM Amigurumi Store Frontend Setup Script for Windows

echo Setting up Amigurumi Store Frontend...

REM Navigate to frontend directory
cd frontend

REM Install dependencies with yarn
echo Installing dependencies with yarn...
yarn install

echo Frontend setup complete!
echo To start the development server, run: yarn start
pause
