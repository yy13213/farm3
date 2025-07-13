import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# 导入配置和数据
from config import *
from data import *

# 设置页面配置
st.set_page_config(**PAGE_CONFIG)

# 自定义CSS样式
def load_css():
    st.markdown(f"""
    <style>
    .main {{
        background-color: {THEME_COLORS['background']};
    }}
    
    .stApp {{
        background-color: {THEME_COLORS['background']};
    }}
    
    .metric-card {{
        background-color: {THEME_COLORS['accent']};
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid {THEME_COLORS['primary']};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }}
    
    .header-title {{
        color: {THEME_COLORS['text']};
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    
    .header-subtitle {{
        color: {THEME_COLORS['text']};
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .sidebar .sidebar-content {{
        background-color: {THEME_COLORS['primary']};
    }}
    
    .product-card {{
        background-color: {THEME_COLORS['accent']};
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid {THEME_COLORS['secondary']};
        margin-bottom: 1rem;
    }}
    
    .live-room-card {{
        background-color: {THEME_COLORS['success']};
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid {THEME_COLORS['primary']};
    }}
    
    .announcement-card {{
        background-color: {THEME_COLORS['info']};
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }}
    
    .chat-message {{
        background-color: {THEME_COLORS['accent']};
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }}
    
    .user-message {{
        background-color: {THEME_COLORS['primary']};
        margin-left: 2rem;
    }}
    
    .bot-message {{
        background-color: {THEME_COLORS['success']};
        margin-right: 2rem;
    }}
    
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {THEME_COLORS['text']};
        background-color: {THEME_COLORS['primary']};
        margin-top: 3rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# 侧边栏导航
def render_sidebar():
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 1rem; background-color: {THEME_COLORS['primary']}; border-radius: 10px; margin-bottom: 2rem;">
        <h2 style="color: {THEME_COLORS['text']};">🌾 {PLATFORM_INFO['name']}</h2>
        <p style="color: {THEME_COLORS['text']};">{PLATFORM_INFO['location']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 导航菜单
    selected_page = st.sidebar.selectbox(
        "选择功能模块",
        list(NAVIGATION_MENU.keys()),
        format_func=lambda x: f"{NAVIGATION_MENU[x]} {x}"
    )
    
    st.sidebar.markdown("---")
    
    # 快速统计
    live_data = get_live_data()
    st.sidebar.metric("在线直播间", live_data['active_rooms'])
    st.sidebar.metric("今日销售额", f"¥{live_data['today_sales']:,}")
    st.sidebar.metric("总观看人数", f"{live_data['total_viewers']:,}")
    
    return selected_page

# 首页仪表板
def render_dashboard():
    st.markdown(f"""
    <div class="header-title">{PLATFORM_INFO['name']}</div>
    <div class="header-subtitle">{PLATFORM_INFO['subtitle']}</div>
    """, unsafe_allow_html=True)
    
    # 核心指标
    live_data = get_live_data()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("今日销售额", f"¥{live_data['today_sales']:,}", "↗️ 12.5%")
    with col2:
        st.metric("本月销售额", f"¥{live_data['month_sales']:,}", "↗️ 8.3%")
    with col3:
        st.metric("在线直播间", live_data['active_rooms'], "→ 0")
    with col4:
        st.metric("总观看人数", f"{live_data['total_viewers']:,}", "↗️ 156")
    
    # 销售趋势图
    st.subheader("📈 销售趋势分析")
    
    # 生成最近30天的销售数据
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    sales_amounts = [random.randint(5000, 20000) for _ in range(30)]
    
    fig = px.line(
        x=dates, 
        y=sales_amounts,
        title="最近30天销售趋势",
        labels={'x': '日期', 'y': '销售额 (元)'}
    )
    fig.update_layout(
        plot_bgcolor=THEME_COLORS['background'],
        paper_bgcolor=THEME_COLORS['accent']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 产品销售排行
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 热销产品排行")
        products = get_products_data()
        products_df = pd.DataFrame(products)
        products_df = products_df.sort_values('sales', ascending=False)
        
        for i, product in enumerate(products_df.head(5).to_dict('records')):
            st.markdown(f"""
            <div class="product-card">
                <strong>{i+1}. {product['image']} {product['name']}</strong><br>
                销量: {product['sales']} | 评分: {product['rating']}⭐<br>
                价格: <span style="color: red;">¥{product['current_price']}</span>
                <del style="color: gray;">¥{product['original_price']}</del>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🎭 直播间状态")
        for room in live_data['live_rooms']:
            st.markdown(f"""
            <div class="live-room-card">
                <strong>🔴 {room['title']}</strong><br>
                主播: {room['avatar']} | 观众: {room['viewers']}人<br>
                销售额: ¥{room['sales']} | 开始时间: {room['start_time']}
            </div>
            """, unsafe_allow_html=True)
    
    # 公告滚动
    st.subheader("📢 平台公告")
    announcements = get_announcements()
    for announcement in announcements:
        st.markdown(f"""
        <div class="announcement-card">
            <strong>{announcement['title']}</strong><br>
            {announcement['content']}<br>
            <small>{announcement['date']}</small>
        </div>
        """, unsafe_allow_html=True)

# 数字人直播管理
def render_live_streaming():
    st.header("🎭 数字人直播管理")
    
    tab1, tab2, tab3 = st.tabs(["直播间管理", "数字人设置", "直播数据"])
    
    with tab1:
        st.subheader("📺 直播间列表")
        live_data = get_live_data()
        
        for room in live_data['live_rooms']:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="live-room-card">
                    <strong>{room['title']}</strong><br>
                    主播: {room['avatar']} | 状态: {room['status']}<br>
                    观众: {room['viewers']}人 | 销售: ¥{room['sales']}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"进入直播间", key=f"enter_{room['id']}"):
                    st.success(f"正在进入{room['title']}...")
            
            with col3:
                if st.button(f"管理设置", key=f"manage_{room['id']}"):
                    st.info(f"正在打开{room['title']}设置...")
    
    with tab2:
        st.subheader("🤖 数字人形象设置")
        
        selected_avatar = st.selectbox(
            "选择数字人形象",
            list(DIGITAL_AVATARS.keys()),
            format_func=lambda x: f"{DIGITAL_AVATARS[x]['name']} ({DIGITAL_AVATARS[x]['gender']})"
        )
        
        avatar_info = DIGITAL_AVATARS[selected_avatar]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **基本信息:**
            - 姓名: {avatar_info['name']}
            - 性别: {avatar_info['gender']}
            - 年龄: {avatar_info['age']}
            - 专长: {avatar_info['speciality']}
            - 语音: {avatar_info['voice']}
            """)
            
            st.markdown(f"""
            **形象描述:**
            {avatar_info['description']}
            """)
        
        with col2:
            st.markdown("**直播脚本生成**")
            product_name = st.text_input("产品名称", "阜平大枣")
            script_style = st.selectbox("脚本风格", ["亲切自然", "专业权威", "幽默风趣"])
            
            if st.button("生成直播脚本"):
                script = f"""
                大家好！我是{avatar_info['name']}，今天给大家推荐我们阜平的特色产品——{product_name}。
                
                这个{product_name}可是我们阜平的骄傲啊！它生长在我们太行山区，
                那里空气清新，水质纯净，昼夜温差大，特别适合农产品的生长。
                
                我们的{product_name}不仅口感好，营养价值也特别高。
                现在下单还有优惠，机会难得，大家赶紧抢购吧！
                """
                st.text_area("生成的直播脚本", script, height=150)
    
    with tab3:
        st.subheader("📊 直播数据分析")
        
        # 直播数据图表
        rooms = live_data['live_rooms']
        room_names = [room['title'] for room in rooms]
        viewers = [room['viewers'] for room in rooms]
        sales = [room['sales'] for room in rooms]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.bar(
                x=room_names, 
                y=viewers,
                title="各直播间观众数量",
                labels={'x': '直播间', 'y': '观众数量'}
            )
            fig1.update_layout(
                plot_bgcolor=THEME_COLORS['background'],
                paper_bgcolor=THEME_COLORS['accent']
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.pie(
                values=sales,
                names=room_names,
                title="各直播间销售额占比"
            )
            fig2.update_layout(
                plot_bgcolor=THEME_COLORS['background'],
                paper_bgcolor=THEME_COLORS['accent']
            )
            st.plotly_chart(fig2, use_container_width=True)

# 产品管理系统
def render_product_management():
    st.header("📦 产品管理系统")
    
    tab1, tab2, tab3 = st.tabs(["产品列表", "添加产品", "库存管理"])
    
    with tab1:
        st.subheader("📋 产品列表")
        products = get_products_data()
        
        # 搜索和筛选
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("搜索产品", placeholder="输入产品名称...")
        with col2:
            category_filter = st.selectbox("筛选分类", ["全部"] + PRODUCT_CATEGORIES)
        
        # 产品展示
        for product in products:
            if search_term and search_term.lower() not in product['name'].lower():
                continue
            if category_filter != "全部" and product['category'] != category_filter:
                continue
                
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{product['image']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="product-card">
                    <h4>{product['name']}</h4>
                    <p><strong>分类:</strong> {product['category']}</p>
                    <p><strong>规格:</strong> {product['specification']}</p>
                    <p><strong>产地:</strong> {product['origin']}</p>
                    <p><strong>描述:</strong> {product['description']}</p>
                    <p><strong>价格:</strong> <span style="color: red; font-size: 1.2rem;">¥{product['current_price']}</span> 
                       <del style="color: gray;">¥{product['original_price']}</del></p>
                    <p><strong>库存:</strong> {product['stock']} | <strong>销量:</strong> {product['sales']} | <strong>评分:</strong> {product['rating']}⭐</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button(f"编辑", key=f"edit_{product['id']}"):
                    st.info(f"正在编辑{product['name']}...")
                if st.button(f"删除", key=f"delete_{product['id']}"):
                    st.warning(f"确认删除{product['name']}？")
    
    with tab2:
        st.subheader("➕ 添加新产品")
        
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                product_name = st.text_input("产品名称*")
                category = st.selectbox("产品分类*", PRODUCT_CATEGORIES)
                origin = st.text_input("产地*", value="河北保定阜平")
                specification = st.text_input("规格*", placeholder="如：500g/袋")
            
            with col2:
                original_price = st.number_input("原价*", min_value=0.0, step=0.1)
                current_price = st.number_input("现价*", min_value=0.0, step=0.1)
                stock = st.number_input("库存数量*", min_value=0, step=1)
                image_emoji = st.text_input("产品图标", placeholder="输入emoji，如：🍎")
            
            description = st.text_area("产品描述*", height=100)
            nutrition = st.text_area("营养价值", height=80)
            features = st.text_input("产品特色", placeholder="用逗号分隔，如：有机种植,无添加,传统工艺")
            
            submitted = st.form_submit_button("添加产品")
            
            if submitted:
                if product_name and category and original_price and current_price:
                    st.success(f"产品 '{product_name}' 添加成功！")
                    st.balloons()
                else:
                    st.error("请填写所有必填项（标*的字段）")
    
    with tab3:
        st.subheader("📊 库存管理")
        
        products = get_products_data()
        
        # 库存预警
        low_stock_products = [p for p in products if p['stock'] < 100]
        if low_stock_products:
            st.warning(f"⚠️ 有 {len(low_stock_products)} 个产品库存不足100件，请及时补货！")
            
            for product in low_stock_products:
                st.markdown(f"""
                <div style="background-color: {THEME_COLORS['warning']}; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;">
                    <strong>{product['name']}</strong> - 当前库存: {product['stock']} 件
                </div>
                """, unsafe_allow_html=True)
        
        # 库存统计图表
        product_names = [p['name'] for p in products]
        stock_levels = [p['stock'] for p in products]
        
        fig = px.bar(
            x=product_names,
            y=stock_levels,
            title="产品库存水平",
            labels={'x': '产品', 'y': '库存数量'},
            color=stock_levels,
            color_continuous_scale='RdYlGn'
        )
        fig.update_layout(
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['accent']
        )
        st.plotly_chart(fig, use_container_width=True)

# AI客服系统
def render_ai_customer_service():
    st.header("🤖 AI客服系统")
    
    tab1, tab2 = st.tabs(["智能客服", "问答库管理"])
    
    with tab1:
        st.subheader("💬 智能客服对话")
        
        # 初始化聊天历史
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "您好！我是智播农链的AI客服小助手，很高兴为您服务！请问有什么可以帮助您的吗？"}
            ]
        
        # 显示聊天历史
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>您:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 AI客服:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        # 用户输入
        user_input = st.text_input("请输入您的问题:", placeholder="例如：阜平大枣的保质期是多久？")
        
        if st.button("发送") and user_input:
            # 添加用户消息
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # 模拟AI回复
            faq_data = get_faq_data()
            response = "抱歉，我没有找到相关信息。您可以联系人工客服获得更详细的帮助。"
            
            # 简单的关键词匹配
            for faq in faq_data:
                if any(keyword in user_input for keyword in faq["question"].split()):
                    response = faq["answer"]
                    break
            
            # 添加AI回复
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
        
        # 快速问题按钮
        st.subheader("🔍 常见问题快速咨询")
        faq_data = get_faq_data()
        
        col1, col2 = st.columns(2)
        for i, faq in enumerate(faq_data):
            with col1 if i % 2 == 0 else col2:
                if st.button(faq["question"], key=f"faq_{i}"):
                    st.session_state.chat_history.append({"role": "user", "content": faq["question"]})
                    st.session_state.chat_history.append({"role": "assistant", "content": faq["answer"]})
                    st.rerun()
    
    with tab2:
        st.subheader("📚 问答库管理")
        
        faq_data = get_faq_data()
        
        # 按分类显示FAQ
        categories = list(set([faq["category"] for faq in faq_data]))
        
        for category in categories:
            st.markdown(f"### {category}")
            category_faqs = [faq for faq in faq_data if faq["category"] == category]
            
            for faq in category_faqs:
                with st.expander(faq["question"]):
                    st.write(faq["answer"])
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("编辑", key=f"edit_faq_{faq['question'][:10]}"):
                            st.info("编辑功能开发中...")
                    with col2:
                        if st.button("删除", key=f"delete_faq_{faq['question'][:10]}"):
                            st.warning("删除功能开发中...")
        
        # 添加新问答
        st.markdown("### ➕ 添加新问答")
        with st.form("add_faq_form"):
            new_question = st.text_input("问题")
            new_answer = st.text_area("答案")
            new_category = st.selectbox("分类", categories + ["新分类"])
            
            if new_category == "新分类":
                new_category = st.text_input("输入新分类名称")
            
            if st.form_submit_button("添加问答"):
                if new_question and new_answer and new_category:
                    st.success("问答添加成功！")
                else:
                    st.error("请填写所有字段")

# 订单管理系统
def render_order_management():
    st.header("📋 订单管理系统")
    
    tab1, tab2 = st.tabs(["订单列表", "订单统计"])
    
    with tab1:
        st.subheader("📝 订单列表")
        
        orders = get_orders_data()
        
        # 筛选选项
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("订单状态", ["全部"] + list(ORDER_STATUS.values()))
        with col2:
            date_filter = st.date_input("起始日期", datetime.now() - timedelta(days=30))
        with col3:
            search_order = st.text_input("搜索订单号")
        
        # 订单表格
        filtered_orders = orders
        if status_filter != "全部":
            status_key = [k for k, v in ORDER_STATUS.items() if v == status_filter][0]
            filtered_orders = [o for o in orders if o['status'] == status_key]
        
        if search_order:
            filtered_orders = [o for o in filtered_orders if search_order in o['order_id']]
        
        # 显示订单
        for order in filtered_orders[:20]:  # 只显示前20个
            with st.expander(f"订单 {order['order_id']} - {ORDER_STATUS[order['status']]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **订单信息:**
                    - 订单号: {order['order_id']}
                    - 客户: {order['customer_name']}
                    - 电话: {order['phone']}
                    - 地址: {order['address']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **商品信息:**
                    - 商品: {order['product_name']}
                    - 数量: {order['quantity']}
                    - 单价: ¥{order['unit_price']}
                    - 总额: ¥{order['total_amount']}
                    """)
                
                st.markdown(f"**下单时间:** {order['order_date'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                # 操作按钮
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("查看详情", key=f"view_{order['order_id']}"):
                        st.info("查看订单详情...")
                with col2:
                    if st.button("更新状态", key=f"update_{order['order_id']}"):
                        st.info("更新订单状态...")
                with col3:
                    if st.button("联系客户", key=f"contact_{order['order_id']}"):
                        st.info("联系客户...")
    
    with tab2:
        st.subheader("📊 订单统计分析")
        
        orders = get_orders_data()
        
        # 订单状态统计
        status_counts = {}
        for order in orders:
            status = ORDER_STATUS[order['status']]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="订单状态分布"
            )
            fig1.update_layout(
                plot_bgcolor=THEME_COLORS['background'],
                paper_bgcolor=THEME_COLORS['accent']
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # 每日订单统计
            daily_orders = {}
            for order in orders:
                date = order['order_date'].date()
                daily_orders[date] = daily_orders.get(date, 0) + 1
            
            dates = sorted(daily_orders.keys())[-30:]  # 最近30天
            counts = [daily_orders[date] for date in dates]
            
            fig2 = px.line(
                x=dates,
                y=counts,
                title="最近30天订单趋势"
            )
            fig2.update_layout(
                plot_bgcolor=THEME_COLORS['background'],
                paper_bgcolor=THEME_COLORS['accent']
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # 核心指标
        total_orders = len(orders)
        total_amount = sum(order['total_amount'] for order in orders)
        avg_order_value = total_amount / total_orders if total_orders > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总订单数", total_orders)
        with col2:
            st.metric("总销售额", f"¥{total_amount:,.2f}")
        with col3:
            st.metric("平均订单价值", f"¥{avg_order_value:.2f}")

# 数据分析中心
def render_data_analysis():
    st.header("📊 数据分析中心")
    
    tab1, tab2, tab3 = st.tabs(["销售分析", "产品分析", "客户分析"])
    
    with tab1:
        st.subheader("💰 销售数据分析")
        
        # 生成销售数据
        sales_data = get_sales_data()
        recent_data = sales_data.tail(30)
        
        # 销售趋势
        fig1 = px.line(
            recent_data,
            x='date',
            y='sales_amount',
            title='最近30天销售趋势'
        )
        fig1.update_layout(
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['accent']
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # 销售指标
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("月度销售额", f"¥{recent_data['sales_amount'].sum():,}")
        with col2:
            st.metric("月度订单数", f"{recent_data['orders'].sum():,}")
        with col3:
            st.metric("月度客户数", f"{recent_data['customers'].sum():,}")
        with col4:
            st.metric("平均客单价", f"¥{recent_data['avg_order_value'].mean():.2f}")
    
    with tab2:
        st.subheader("📦 产品销售分析")
        
        products = get_products_data()
        
        # 产品销售排行
        products_df = pd.DataFrame(products)
        products_df = products_df.sort_values('sales', ascending=False)
        
        fig2 = px.bar(
            products_df,
            x='name',
            y='sales',
            title='产品销售排行',
            color='sales',
            color_continuous_scale='viridis'
        )
        fig2.update_layout(
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['accent']
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # 产品评分分析
        fig3 = px.scatter(
            products_df,
            x='current_price',
            y='rating',
            size='sales',
            color='category',
            title='产品价格vs评分关系',
            hover_data=['name']
        )
        fig3.update_layout(
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['accent']
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.subheader("👥 客户行为分析")
        
        # 模拟客户数据
        orders = get_orders_data()
        
        # 客户地区分布
        regions = [order['address'].split('县')[1] if '县' in order['address'] else '其他' for order in orders]
        region_counts = pd.Series(regions).value_counts()
        
        fig4 = px.pie(
            values=region_counts.values,
            names=region_counts.index,
            title='客户地区分布'
        )
        fig4.update_layout(
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['accent']
        )
        st.plotly_chart(fig4, use_container_width=True)
        
        # 客户购买力分析
        customer_spending = {}
        for order in orders:
            customer = order['customer_name']
            customer_spending[customer] = customer_spending.get(customer, 0) + order['total_amount']
        
        spending_ranges = {'0-50': 0, '50-100': 0, '100-200': 0, '200+': 0}
        for spending in customer_spending.values():
            if spending < 50:
                spending_ranges['0-50'] += 1
            elif spending < 100:
                spending_ranges['50-100'] += 1
            elif spending < 200:
                spending_ranges['100-200'] += 1
            else:
                spending_ranges['200+'] += 1
        
        fig5 = px.bar(
            x=list(spending_ranges.keys()),
            y=list(spending_ranges.values()),
            title='客户消费水平分布',
            labels={'x': '消费金额区间(元)', 'y': '客户数量'}
        )
        fig5.update_layout(
            plot_bgcolor=THEME_COLORS['background'],
            paper_bgcolor=THEME_COLORS['accent']
        )
        st.plotly_chart(fig5, use_container_width=True)

# 系统设置
def render_system_settings():
    st.header("⚙️ 系统设置")
    
    tab1, tab2, tab3 = st.tabs(["基本设置", "用户管理", "帮助文档"])
    
    with tab1:
        st.subheader("🔧 基本设置")
        
        with st.form("basic_settings"):
            st.markdown("**平台信息设置**")
            platform_name = st.text_input("平台名称", value=PLATFORM_INFO['name'])
            platform_location = st.text_input("服务地区", value=PLATFORM_INFO['location'])
            
            st.markdown("**系统参数设置**")
            refresh_interval = st.slider("数据刷新间隔(秒)", 10, 300, REFRESH_INTERVAL)
            page_size = st.slider("每页显示条数", 5, 50, PAGINATION['page_size'])
            
            st.markdown("**通知设置**")
            email_notifications = st.checkbox("启用邮件通知", value=True)
            sms_notifications = st.checkbox("启用短信通知", value=True)
            
            if st.form_submit_button("保存设置"):
                st.success("设置已保存！")
    
    with tab2:
        st.subheader("👤 用户权限管理")
        
        # 模拟用户数据
        users = [
            {"username": "admin", "role": "管理员", "status": "活跃", "last_login": "2024-01-01 10:00"},
            {"username": "operator1", "role": "运营人员", "status": "活跃", "last_login": "2024-01-01 09:30"},
            {"username": "service1", "role": "客服人员", "status": "活跃", "last_login": "2024-01-01 08:45"},
        ]
        
        for user in users:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**{user['username']}**")
            with col2:
                st.write(user['role'])
            with col3:
                st.write(user['status'])
            with col4:
                if st.button(f"管理", key=f"manage_user_{user['username']}"):
                    st.info(f"管理用户 {user['username']}")
        
        st.markdown("---")
        st.subheader("➕ 添加新用户")
        with st.form("add_user"):
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("用户名")
                new_role = st.selectbox("角色", ["管理员", "运营人员", "客服人员"])
            with col2:
                new_password = st.text_input("密码", type="password")
                new_email = st.text_input("邮箱")
            
            if st.form_submit_button("添加用户"):
                if new_username and new_password:
                    st.success(f"用户 {new_username} 添加成功！")
                else:
                    st.error("请填写用户名和密码")
    
    with tab3:
        st.subheader("📖 帮助文档")
        
        help_sections = [
            {
                "title": "🏠 首页仪表板使用指南",
                "content": """
                首页仪表板是平台的核心控制中心，提供以下功能：
                - 实时查看销售数据和关键指标
                - 监控直播间状态和观众数据
                - 查看热销产品排行榜
                - 浏览平台最新公告和活动信息
                """
            },
            {
                "title": "🎭 数字人直播管理",
                "content": """
                数字人直播功能帮助农户轻松开展直播带货：
                - 选择合适的数字人形象和语音
                - 自动生成产品介绍脚本
                - 设置直播间背景和商品展示
                - 实时监控直播数据和销售情况
                """
            },
            {
                "title": "📦 产品管理系统",
                "content": """
                产品管理系统提供完整的商品管理功能：
                - 添加、编辑、删除产品信息
                - 管理产品图片和详细描述
                - 设置价格策略和库存管理
                - 查看产品销售数据和用户评价
                """
            },
            {
                "title": "🤖 AI客服系统",
                "content": """
                AI客服系统提供24小时智能客服支持：
                - 自动回答常见问题
                - 支持多轮对话和上下文理解
                - 管理问答知识库
                - 无法解答时转接人工客服
                """
            }
        ]
        
        for section in help_sections:
            with st.expander(section["title"]):
                st.markdown(section["content"])
        
        st.markdown("---")
        st.markdown(f"""
        **技术支持联系方式:**
        - 客服热线: 400-123-4567
        - 邮箱: support@zhibonongchain.com
        - 工作时间: 9:00-18:00 (周一至周五)
        
        **平台版本:** {PLATFORM_INFO['version']}
        """)

# 页面底部
def render_footer():
    st.markdown(f"""
    <div class="footer">
        <p>{PLATFORM_INFO['copyright']}</p>
        <p>{PLATFORM_INFO['support']}</p>
        <p>版本: {PLATFORM_INFO['version']} | 服务地区: {PLATFORM_INFO['location']}</p>
    </div>
    """, unsafe_allow_html=True)

# 主函数
def main():
    # 加载CSS样式
    load_css()
    
    # 渲染侧边栏
    selected_page = render_sidebar()
    
    # 根据选择的页面渲染内容
    if selected_page == "首页仪表板":
        render_dashboard()
    elif selected_page == "数字人直播":
        render_live_streaming()
    elif selected_page == "产品管理":
        render_product_management()
    elif selected_page == "AI客服":
        render_ai_customer_service()
    elif selected_page == "订单管理":
        render_order_management()
    elif selected_page == "数据分析":
        render_data_analysis()
    elif selected_page == "系统设置":
        render_system_settings()
    
    # 渲染页面底部
    render_footer()

if __name__ == "__main__":
    main() 