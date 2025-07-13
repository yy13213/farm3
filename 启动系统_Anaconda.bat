@echo off
chcp 65001 > nul
echo ===============================================
echo 🌾 智播农链 - 保定阜平智慧农业管理平台
echo 从种到销，AI驱动农业全流程数智升级
echo ===============================================
echo.
echo 此脚本专为Anaconda环境设计
echo.

REM 设置Anaconda路径（用户可能需要根据实际安装路径修改）
set ANACONDA_PATH=%USERPROFILE%\anaconda3
if not exist "%ANACONDA_PATH%" (
    set ANACONDA_PATH=%USERPROFILE%\miniconda3
)
if not exist "%ANACONDA_PATH%" (
    set ANACONDA_PATH=C:\ProgramData\Anaconda3
)

echo 正在初始化Anaconda环境...
call "%ANACONDA_PATH%\Scripts\activate.bat" base

echo 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误：无法在Anaconda环境中找到Python
    echo 请确保Anaconda已正确安装并激活
    pause
    exit /b 1
)

echo.
echo 正在安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 尝试使用conda-forge源安装...
    conda install -c conda-forge streamlit plotly pandas numpy folium matplotlib -y
    pip install streamlit-folium streamlit-option-menu
    if %errorlevel% neq 0 (
        echo 依赖包安装失败，请手动安装
        pause
        exit /b 1
    )
)

echo.
echo 正在启动智播农链系统...
echo 系统将在浏览器中打开：http://localhost:8501
echo 按Ctrl+C可停止系统运行
echo.

streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --theme.base=light --theme.primaryColor=#2196F3 --theme.backgroundColor=#F5F5F5 --theme.secondaryBackgroundColor=#FAFAFA

pause 