#!/bin/bash
echo "智播农链销售平台启动中..."
echo ""
echo "正在检查Python环境..."
python3 --version
echo ""
echo "正在安装依赖包..."
pip3 install -r requirements.txt
echo ""
echo "启动Streamlit应用..."
streamlit run main.py 