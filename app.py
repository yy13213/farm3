import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import st_folium

# 页面配置
st.set_page_config(
    page_title="智播农链 - 保定阜平智慧农业管理平台",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 主题色彩 */
    :root {
        --primary-blue: #2196F3;
        --light-blue: #E3F2FD;
        --dark-blue: #1976D2;
        --success-green: #4CAF50;
        --warning-orange: #FF9800;
        --error-red: #F44336;
        --neutral-gray: #9E9E9E;
        --main-bg: #F5F5F5;
        --card-bg: #FFFFFF;
        --panel-bg: #FAFAFA;
    }
    
    /* 隐藏默认样式 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 主容器样式 */
    .main > div {
        padding: 1rem;
        background-color: var(--main-bg);
    }
    
    /* 顶部导航栏 */
    .top-header {
        background: linear-gradient(90deg, var(--dark-blue) 0%, var(--primary-blue) 100%);
        color: white;
        padding: 1rem 2rem;
        margin: -1rem -1rem 1rem -1rem;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-size: 24px;
        font-weight: bold;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        font-size: 14px;
        opacity: 0.9;
        text-align: center;
        margin-top: 5px;
    }
    
    /* 卡片样式 */
    .metric-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #E0E0E0;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-blue);
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--neutral-gray);
        margin-top: 0.5rem;
    }
    
    /* 状态指示器 */
    .status-healthy { color: var(--success-green); }
    .status-warning { color: var(--warning-orange); }
    .status-error { color: var(--error-red); }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background-color: var(--panel-bg);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: var(--primary-blue);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: var(--dark-blue);
        border: none;
    }
    
    /* 数据表格样式 */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* 图表容器 */
    .chart-container {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 数据生成函数
@st.cache_data
def generate_demo_data():
    """生成演示数据"""
    # 地块数据
    fields = []
    for i in range(50):
        field = {
            "field_id": f"FP{i+1:03d}",
            "field_name": f"阜平{i+1}号地块",
            "latitude": random.uniform(38.8, 39.0),
            "longitude": random.uniform(113.8, 114.2),
            "area": round(random.uniform(5, 50), 1),
            "crop_type": random.choice(["玉米", "小麦", "大豆", "红薯", "花生", "苹果", "核桃", "枣树", "蔬菜", "中药材"]),
            "status": random.choices(["健康", "预警", "异常"], weights=[0.7, 0.2, 0.1])[0],
            "owner": f"农户{i+1}",
            "soil_type": random.choice(["壤土", "砂壤土", "黏壤土", "砂土", "黏土"])
        }
        fields.append(field)
    
    # 传感器数据
    sensor_data = []
    for i in range(30):  # 最近30天
        date = datetime.now() - timedelta(days=i)
        sensor_data.append({
            "date": date,
            "temperature": round(random.uniform(15, 35), 1),
            "humidity": round(random.uniform(40, 80), 1),
            "ph": round(random.uniform(6.0, 8.0), 1),
            "soil_moisture": round(random.uniform(30, 70), 1),
            "nitrogen": round(random.uniform(50, 200), 1),
            "phosphorus": round(random.uniform(10, 50), 1),
            "potassium": round(random.uniform(80, 300), 1)
        })
    
    # 农机数据
    machines = []
    machine_types = ["拖拉机", "植保机", "收割机", "播种机", "施肥机"]
    statuses = ["工作中", "空闲", "维修", "故障"]
    
    for i in range(20):
        machine = {
            "machine_id": f"M{i+1:03d}",
            "machine_name": f"{random.choice(machine_types)}{i+1}号",
            "machine_type": random.choice(machine_types),
            "status": random.choices(statuses, weights=[0.3, 0.5, 0.15, 0.05])[0],
            "latitude": random.uniform(38.8, 39.0),
            "longitude": random.uniform(113.8, 114.2),
            "fuel_level": round(random.uniform(20, 100), 1),
            "working_hours": round(random.uniform(100, 2000), 1),
            "efficiency": round(random.uniform(70, 95), 1)
        }
        machines.append(machine)
    
    # 市场价格数据
    crops = ["玉米", "小麦", "大豆", "红薯", "花生"]
    price_data = []
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        for crop in crops:
            base_price = {"玉米": 2.7, "小麦": 3.2, "大豆": 5.8, "红薯": 1.8, "花生": 8.5}[crop]
            price = base_price + random.uniform(-0.3, 0.3)
            price_data.append({
                "date": date,
                "crop_type": crop,
                "price": round(price, 2),
                "change": round(random.uniform(-5, 5), 2)
            })
    
    return {
        "fields": pd.DataFrame(fields),
        "sensor_data": pd.DataFrame(sensor_data),
        "machines": pd.DataFrame(machines),
        "price_data": pd.DataFrame(price_data)
    }

# 加载数据
data = generate_demo_data()

# 顶部导航栏
st.markdown("""
<div class="top-header">
    <div class="header-title">🌾 智播农链 - 保定阜平智慧农业管理平台</div>
    <div class="header-subtitle">从种到销，AI驱动农业全流程数智升级</div>
</div>
""", unsafe_allow_html=True)

# 侧边栏导航
with st.sidebar:
    st.markdown("### 🗂️ 功能导航")
    selected = option_menu(
        menu_title=None,
        options=["数字孪生大屏", "智能微区管理", "数字孪生决策", "农机调度", "AI专家顾问", "数据统计"],
        icons=["globe", "geo-alt", "graph-up", "truck", "robot", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#2196F3", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#E3F2FD"},
            "nav-link-selected": {"background-color": "#2196F3"},
        }
    )

# 主内容区域
if selected == "数字孪生大屏":
    st.markdown("## 🗺️ 数字孪生大屏")
    
    # 关键指标
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">1,245</div>
            <div class="metric-label">总耕地面积(亩)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">42</div>
            <div class="metric-label">地块数量</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">18</div>
            <div class="metric-label">在线农机</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">156</div>
            <div class="metric-label">传感器数量</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">92%</div>
            <div class="metric-label">系统健康度</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 主要内容区域
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_left:
        st.markdown("### 📊 产量统计")
        
        # 作物产量分布饼图
        crop_counts = data["fields"]["crop_type"].value_counts()
        fig_pie = px.pie(
            values=crop_counts.values,
            names=crop_counts.index,
            title="作物种植分布",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(
            height=300,
            showlegend=True,
            font=dict(size=12)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # 地块状态统计
        st.markdown("### 🏥 地块健康状态")
        status_counts = data["fields"]["status"].value_counts()
        for status, count in status_counts.items():
            color_class = {
                "健康": "status-healthy",
                "预警": "status-warning", 
                "异常": "status-error"
            }.get(status, "")
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span class="{color_class}">● {status}</span>
                <span><strong>{count}</strong></span>
            </div>
            """, unsafe_allow_html=True)
    
    with col_center:
        st.markdown("### 🗺️ 地块分布地图")
        
        # 创建地图
        center_lat = data["fields"]["latitude"].mean()
        center_lon = data["fields"]["longitude"].mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles="OpenStreetMap"
        )
        
        # 添加地块标记
        for idx, row in data["fields"].iterrows():
            color = {
                "健康": "green",
                "预警": "orange",
                "异常": "red"
            }.get(row["status"], "blue")
            
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=8,
                popup=f"""
                <b>{row['field_name']}</b><br>
                作物：{row['crop_type']}<br>
                面积：{row['area']}亩<br>
                状态：{row['status']}<br>
                负责人：{row['owner']}
                """,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(m)
        
        # 添加农机标记
        for idx, row in data["machines"].iterrows():
            if row["status"] == "工作中":
                folium.Marker(
                    location=[row["latitude"], row["longitude"]],
                    popup=f"""
                    <b>{row['machine_name']}</b><br>
                    类型：{row['machine_type']}<br>
                    状态：{row['status']}<br>
                    燃料：{row['fuel_level']}%
                    """,
                    icon=folium.Icon(color="blue", icon="cog")
                ).add_to(m)
        
        # 显示地图
        map_data = st_folium(m, width=700, height=400)
    
    with col_right:
        st.markdown("### 💰 市场价格")
        
        # 今日价格
        today_prices = data["price_data"][data["price_data"]["date"].dt.date == datetime.now().date()]
        if not today_prices.empty:
            for _, row in today_prices.iterrows():
                change_color = "green" if row["change"] >= 0 else "red"
                change_symbol = "↑" if row["change"] >= 0 else "↓"
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                    <span>{row['crop_type']}</span>
                    <div>
                        <span style="font-weight: bold;">{row['price']}元/kg</span>
                        <span style="color: {change_color}; margin-left: 0.5rem;">
                            {change_symbol}{abs(row['change']):.1f}%
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("### 🌡️ 实时环境")
        
        # 最新传感器数据
        latest_sensor = data["sensor_data"].iloc[0]
        
        metrics = [
            ("温度", f"{latest_sensor['temperature']}°C", "🌡️"),
            ("湿度", f"{latest_sensor['humidity']}%", "💧"),
            ("土壤湿度", f"{latest_sensor['soil_moisture']}%", "🌱"),
            ("pH值", f"{latest_sensor['ph']}", "⚗️")
        ]
        
        for label, value, icon in metrics:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0;">
                <span>{icon} {label}</span>
                <span style="font-weight: bold;">{value}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # 底部趋势图
    st.markdown("### 📈 趋势分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 温度趋势
        fig_temp = px.line(
            data["sensor_data"],
            x="date",
            y="temperature",
            title="温度趋势",
            labels={"temperature": "温度(°C)", "date": "日期"}
        )
        fig_temp.update_layout(height=300)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # 价格趋势
        corn_prices = data["price_data"][data["price_data"]["crop_type"] == "玉米"]
        fig_price = px.line(
            corn_prices,
            x="date",
            y="price",
            title="玉米价格趋势",
            labels={"price": "价格(元/kg)", "date": "日期"}
        )
        fig_price.update_layout(height=300)
        st.plotly_chart(fig_price, use_container_width=True)

elif selected == "智能微区管理":
    st.markdown("## 🌱 智能微区精细种植管理")
    
    # 创建全屏地图布局
    st.markdown("""
    <style>
    .map-container {
        height: 80vh;
        width: 100%;
        position: relative;
        background-color: #f0f0f0;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .control-panel {
        position: absolute;
        top: 20px;
        left: 20px;
        width: 300px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        max-height: 70vh;
        overflow-y: auto;
    }
    
    .data-panel {
        position: absolute;
        top: 20px;
        right: 20px;
        width: 280px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        max-height: 70vh;
        overflow-y: auto;
    }
    
    .status-bar {
        position: absolute;
        bottom: 20px;
        left: 20px;
        right: 20px;
        height: 60px;
        background: rgba(33, 150, 243, 0.9);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: space-around;
        color: white;
        font-weight: bold;
        z-index: 1000;
    }
    
    .metric-item {
        text-align: center;
        padding: 5px 10px;
    }
    
    .metric-value {
        font-size: 18px;
        font-weight: bold;
    }
    
    .metric-label {
        font-size: 12px;
        opacity: 0.9;
    }
    
    .field-item {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .field-item:hover {
        background: #e3f2fd;
        border-color: #2196F3;
    }
    
    .field-item.selected {
        background: #e3f2fd;
        border-color: #2196F3;
        border-width: 2px;
    }
    
    .sensor-data {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #eee;
    }
    
    .sensor-value {
        font-weight: bold;
        color: #2196F3;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 创建地图容器
    map_container = st.container()
    
    with map_container:
        # 创建主地图
        center_lat = data["fields"]["latitude"].mean()
        center_lon = data["fields"]["longitude"].mean()
        
        # 创建更大的地图
        main_map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=13,
            tiles="OpenStreetMap",
            width="100%",
            height="80vh"
        )
        
        # 添加地块标记（更详细的信息）
        for idx, row in data["fields"].iterrows():
            # 根据状态确定颜色
            status_colors = {
                "健康": "#4CAF50",
                "预警": "#FF9800", 
                "异常": "#F44336"
            }
            color = status_colors.get(row["status"], "#2196F3")
            
            # 创建详细的弹窗信息
            popup_html = f"""
            <div style="width: 250px; font-family: Arial, sans-serif;">
                <h4 style="color: {color}; margin: 0 0 10px 0;">{row['field_name']}</h4>
                <table style="width: 100%; font-size: 12px;">
                    <tr><td><strong>地块编号:</strong></td><td>{row['field_id']}</td></tr>
                    <tr><td><strong>作物类型:</strong></td><td>{row['crop_type']}</td></tr>
                    <tr><td><strong>种植面积:</strong></td><td>{row['area']}亩</td></tr>
                    <tr><td><strong>健康状态:</strong></td><td style="color: {color};">{row['status']}</td></tr>
                    <tr><td><strong>负责人:</strong></td><td>{row['owner']}</td></tr>
                    <tr><td><strong>土壤类型:</strong></td><td>{row['soil_type']}</td></tr>
                </table>
                <div style="margin-top: 10px; padding: 8px; background: #f0f0f0; border-radius: 4px;">
                    <strong>实时数据:</strong><br>
                    温度: {data['sensor_data'].iloc[0]['temperature']}°C<br>
                    湿度: {data['sensor_data'].iloc[0]['humidity']}%<br>
                    土壤湿度: {data['sensor_data'].iloc[0]['soil_moisture']}%
                </div>
            </div>
            """
            
            # 添加地块标记
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=12,
                popup=folium.Popup(popup_html, max_width=300),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.8,
                weight=2
            ).add_to(main_map)
            
            # 添加地块标签
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                icon=folium.DivIcon(
                    html=f'<div style="color: {color}; font-weight: bold; font-size: 10px; text-shadow: 1px 1px 2px white;">{row["field_id"]}</div>',
                    icon_size=(50, 20),
                    icon_anchor=(25, 10)
                )
            ).add_to(main_map)
        
        # 添加农机位置
        for idx, row in data["machines"].iterrows():
            if row["status"] == "工作中":
                machine_icon = {
                    "拖拉机": "🚜",
                    "植保机": "🚁", 
                    "收割机": "🌾",
                    "播种机": "🌱",
                    "施肥机": "💧"
                }.get(row["machine_type"], "🚜")
                
                folium.Marker(
                    location=[row["latitude"], row["longitude"]],
                    popup=f"""
                    <div style="font-family: Arial, sans-serif;">
                        <h4>{machine_icon} {row['machine_name']}</h4>
                        <p><strong>类型:</strong> {row['machine_type']}</p>
                        <p><strong>状态:</strong> <span style="color: green;">{row['status']}</span></p>
                        <p><strong>燃料:</strong> {row['fuel_level']}%</p>
                        <p><strong>工作时长:</strong> {row['working_hours']}小时</p>
                        <p><strong>效率:</strong> {row['efficiency']}%</p>
                    </div>
                    """,
                    icon=folium.Icon(color="blue", icon="cog", prefix="fa")
                ).add_to(main_map)
        
        # 显示地图
        map_data = st_folium(main_map, width="100%", height=600, returned_objects=["last_object_clicked"])
    
    # 左侧控制面板
    with st.sidebar:
        st.markdown("### 🎛️ 控制面板")
        
        # 地块筛选
        st.markdown("#### 地块筛选")
        crop_filter = st.multiselect(
            "作物类型",
            options=data["fields"]["crop_type"].unique(),
            default=data["fields"]["crop_type"].unique()[:3]
        )
        
        status_filter = st.multiselect(
            "健康状态",
            options=["健康", "预警", "异常"],
            default=["健康", "预警", "异常"]
        )
        
        # 筛选数据
        filtered_fields = data["fields"][
            (data["fields"]["crop_type"].isin(crop_filter)) & 
            (data["fields"]["status"].isin(status_filter))
        ]
        
        st.markdown("#### 地块列表")
        for idx, row in filtered_fields.iterrows():
            status_color = {
                "健康": "#4CAF50",
                "预警": "#FF9800",
                "异常": "#F44336"
            }.get(row["status"], "#666")
            
            with st.expander(f"{row['field_name']} ({row['crop_type']})"):
                st.markdown(f"""
                **地块编号:** {row['field_id']}  
                **面积:** {row['area']}亩  
                **状态:** <span style="color: {status_color};">●</span> {row['status']}  
                **负责人:** {row['owner']}  
                **土壤类型:** {row['soil_type']}
                """, unsafe_allow_html=True)
                
                if st.button(f"查看详情", key=f"detail_{idx}"):
                    st.info(f"已选择地块: {row['field_name']}")
        
        st.markdown("#### 操作控制")
        
        # 农机调度
        st.markdown("**农机调度**")
        available_machines = data["machines"][data["machines"]["status"] == "空闲"]
        if not available_machines.empty:
            selected_machine = st.selectbox(
                "选择农机",
                options=available_machines["machine_name"].tolist()
            )
            
            if st.button("派遣农机"):
                st.success(f"已派遣 {selected_machine} 到选定地块")
        else:
            st.info("暂无空闲农机")
        
        # 灌溉控制
        st.markdown("**灌溉控制**")
        irrigation_zones = [f"灌溉区域{i+1}" for i in range(5)]
        selected_zone = st.selectbox("选择灌溉区域", irrigation_zones)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("开启灌溉"):
                st.success(f"已开启{selected_zone}灌溉")
        with col2:
            if st.button("关闭灌溉"):
                st.info(f"已关闭{selected_zone}灌溉")
        
        # 施肥控制
        st.markdown("**施肥控制**")
        fertilizer_type = st.selectbox(
            "肥料类型",
            ["氮肥", "磷肥", "钾肥", "复合肥", "有机肥"]
        )
        
        amount = st.slider("施肥量 (kg/亩)", 5, 50, 20)
        
        if st.button("开始施肥"):
            st.success(f"已开始施用{fertilizer_type}，用量{amount}kg/亩")
    
    # 右侧数据面板（使用主界面右侧空间）
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown("### 📊 实时监控")
            
            # 环境数据
            latest_sensor = data["sensor_data"].iloc[0]
            
            # 温度
            temp_color = "green" if 20 <= latest_sensor['temperature'] <= 30 else "orange"
            st.metric(
                "温度",
                f"{latest_sensor['temperature']}°C",
                delta=f"{random.uniform(-2, 2):.1f}°C"
            )
            
            # 湿度
            humidity_color = "green" if 50 <= latest_sensor['humidity'] <= 70 else "orange"
            st.metric(
                "空气湿度",
                f"{latest_sensor['humidity']}%",
                delta=f"{random.uniform(-5, 5):.1f}%"
            )
            
            # 土壤湿度
            soil_color = "green" if 40 <= latest_sensor['soil_moisture'] <= 60 else "orange"
            st.metric(
                "土壤湿度",
                f"{latest_sensor['soil_moisture']}%",
                delta=f"{random.uniform(-3, 3):.1f}%"
            )
            
            # pH值
            ph_color = "green" if 6.5 <= latest_sensor['ph'] <= 7.5 else "orange"
            st.metric(
                "土壤pH",
                f"{latest_sensor['ph']:.1f}",
                delta=f"{random.uniform(-0.2, 0.2):.2f}"
            )
        
        with col2:
            st.markdown("### 🚜 农机状态")
            
            # 农机状态统计
            machine_status = data["machines"]["status"].value_counts()
            
            for status, count in machine_status.items():
                color = {
                    "工作中": "🟢",
                    "空闲": "🟡",
                    "维修": "🟠",
                    "故障": "🔴"
                }.get(status, "⚪")
                
                st.markdown(f"{color} **{status}**: {count}台")
            
            st.markdown("### 🌱 作物状态")
            
            # 作物健康状态
            crop_status = data["fields"]["status"].value_counts()
            
            for status, count in crop_status.items():
                color = {
                    "健康": "🟢",
                    "预警": "🟡", 
                    "异常": "🔴"
                }.get(status, "⚪")
                
                st.markdown(f"{color} **{status}**: {count}个地块")
            
            # 作物分布
            st.markdown("### 📈 作物分布")
            crop_counts = data["fields"]["crop_type"].value_counts().head(5)
            
            for crop, count in crop_counts.items():
                st.markdown(f"🌾 **{crop}**: {count}个地块")
        
        with col3:
            st.markdown("### ⚡ 系统状态")
            
            # 系统指标
            st.metric("在线传感器", "156/160", "97.5%")
            st.metric("数据更新", "正常", "实时")
            st.metric("网络状态", "良好", "98ms")
            st.metric("存储使用", "68%", "正常")
            
            st.markdown("### 📅 今日任务")
            
            tasks = [
                "🌾 收割3号地块玉米",
                "💧 检查灌溉系统",
                "🚜 农机定期保养",
                "🌱 播种新品种试验",
                "📊 数据备份"
            ]
            
            for i, task in enumerate(tasks):
                if st.checkbox(task, key=f"task_{i}"):
                    st.success("任务已完成")
    
    # 底部状态栏
    st.markdown("---")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 18px; font-weight: bold; color: #2196F3;">
                {len(filtered_fields)}
            </div>
            <div style="font-size: 12px; color: #666;">
                活跃地块
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        working_machines = len(data["machines"][data["machines"]["status"] == "工作中"])
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 18px; font-weight: bold; color: #4CAF50;">
                {working_machines}
            </div>
            <div style="font-size: 12px; color: #666;">
                工作农机
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 18px; font-weight: bold; color: #FF9800;">
                {latest_sensor['temperature']}°C
            </div>
            <div style="font-size: 12px; color: #666;">
                当前温度
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 18px; font-weight: bold; color: #03A9F4;">
                {latest_sensor['humidity']}%
            </div>
            <div style="font-size: 12px; color: #666;">
                空气湿度
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        healthy_fields = len(data["fields"][data["fields"]["status"] == "健康"])
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 18px; font-weight: bold; color: #4CAF50;">
                {healthy_fields}
            </div>
            <div style="font-size: 12px; color: #666;">
                健康地块
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 18px; font-weight: bold; color: #9C27B0;">
                98.5%
            </div>
            <div style="font-size: 12px; color: #666;">
                系统效率
            </div>
        </div>
        """, unsafe_allow_html=True)

elif selected == "数字孪生决策":
    st.markdown("## 🔮 农业数字孪生与可视化决策")
    st.info("此功能正在开发中，敬请期待...")

elif selected == "农机调度":
    st.markdown("## 🚜 农机自动驾驶与共享调度")
    st.info("此功能正在开发中，敬请期待...")

elif selected == "AI专家顾问":
    st.markdown("## 🤖 农业知识大模型/AI专家顾问")
    st.info("此功能正在开发中，敬请期待...")

elif selected == "数据统计":
    st.markdown("## 📊 数据统计与报表")
    st.info("此功能正在开发中，敬请期待...")

# 底部状态栏
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>© 2024 智播农链 - 保定阜平智慧农业管理平台 | 技术支持：AI驱动农业全流程数智升级</p>
    <p>最后更新：{} | 系统状态：正常运行</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True) 