#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智播农链启动脚本
"""

import subprocess
import sys
import os

def install_requirements():
    """安装依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖包安装完成！")
    except subprocess.CalledProcessError:
        print("依赖包安装失败，请手动安装：pip install -r requirements.txt")
        return False
    return True

def run_streamlit():
    """运行Streamlit应用"""
    print("正在启动智播农链系统...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--theme.base=light",
            "--theme.primaryColor=#2196F3",
            "--theme.backgroundColor=#F5F5F5",
            "--theme.secondaryBackgroundColor=#FAFAFA"
        ])
    except KeyboardInterrupt:
        print("\n系统已停止运行")
    except Exception as e:
        print(f"启动失败：{e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🌾 智播农链 - 保定阜平智慧农业管理平台")
    print("从种到销，AI驱动农业全流程数智升级")
    print("=" * 50)
    
    # 检查requirements.txt是否存在
    if not os.path.exists("requirements.txt"):
        print("未找到requirements.txt文件！")
        sys.exit(1)
    
    # 安装依赖包
    if install_requirements():
        # 运行应用
        run_streamlit()
    else:
        print("请先安装依赖包后再运行")
        sys.exit(1) 