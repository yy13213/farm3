@echo off
chcp 65001 > nul
echo ===============================================
echo 🌾 智播农链 - 保定阜平智慧农业管理平台
echo 从种到销，AI驱动农业全流程数智升级
echo ===============================================
echo.

echo 正在检查Python环境...

REM 尝试不同的Python命令
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 找到Python，使用python命令
    set PYTHON_CMD=python
    goto :install_deps
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 找到Python，使用py命令
    set PYTHON_CMD=py
    goto :install_deps
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo 找到Python，使用python3命令
    set PYTHON_CMD=python3
    goto :install_deps
)

REM 检查是否在conda环境中
where conda >nul 2>&1
if %errorlevel% equ 0 (
    echo 检测到Conda环境，尝试激活Python...
    call conda activate base >nul 2>&1
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo 在Conda环境中找到Python
        set PYTHON_CMD=python
        goto :install_deps
    )
)

echo 错误：未找到Python！
echo.
echo 请尝试以下解决方案：
echo 1. 安装Python：https://www.python.org/downloads/
echo 2. 确保Python已添加到系统PATH
echo 3. 如果使用Anaconda，请在Anaconda Prompt中运行此脚本
echo 4. 或者手动运行：pip install -r requirements.txt 然后 streamlit run app.py
echo.
pause
exit /b 1

:install_deps
echo.
echo 正在安装依赖包...
%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 依赖包安装失败，尝试使用清华源...
    %PYTHON_CMD% -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
    if %errorlevel% neq 0 (
        echo 依赖包安装失败，请检查网络连接或手动安装
        echo 可以尝试运行：%PYTHON_CMD% -m pip install streamlit plotly pandas numpy folium streamlit-folium streamlit-option-menu matplotlib
        pause
        exit /b 1
    )
)

echo.
echo 正在启动智播农链系统...
echo 系统将在浏览器中打开：http://localhost:8501
echo 按Ctrl+C可停止系统运行
echo.

%PYTHON_CMD% -m streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --theme.base=light --theme.primaryColor=#2196F3 --theme.backgroundColor=#F5F5F5 --theme.secondaryBackgroundColor=#FAFAFA

pause 