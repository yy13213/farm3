# 智播农链销售平台配置文件

# 页面配置
PAGE_CONFIG = {
    "page_title": "智播农链销售平台",
    "page_icon": "🌾",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# 主题色彩配置
THEME_COLORS = {
    "primary": "#F5DEB3",      # 浅黄色
    "secondary": "#DEB887",    # 深浅黄色
    "accent": "#FFF8DC",       # 象牙白
    "success": "#90EE90",      # 浅绿色
    "warning": "#FFD700",      # 金色
    "error": "#FF6B6B",        # 浅红色
    "info": "#87CEEB",         # 天蓝色
    "text": "#2F4F4F",         # 深灰绿色
    "background": "#FFFEF7"    # 淡黄白色
}

# 平台基本信息
PLATFORM_INFO = {
    "name": "智播农链销售平台",
    "subtitle": "从种到销，AI驱动农业全流程数智升级",
    "location": "保定阜平",
    "version": "v1.0.0",
    "copyright": "© 2024 智播农链. 保留所有权利.",
    "support": "技术支持：AI农业科技团队"
}

# 导航菜单配置
NAVIGATION_MENU = {
    "首页仪表板": "🏠",
    "数字人直播": "🎭",
    "产品管理": "📦",
    "AI客服": "🤖",
    "订单管理": "📋",
    "数据分析": "📊",
    "系统设置": "⚙️"
}

# 数字人形象配置
DIGITAL_AVATARS = {
    "小王": {
        "name": "小王",
        "gender": "男性",
        "age": "青年",
        "description": "年轻农民形象，穿着朴素，亲切自然",
        "speciality": "蔬菜种植专家",
        "voice": "保定方言"
    },
    "小李": {
        "name": "小李",
        "gender": "女性", 
        "age": "中年",
        "description": "中年农妇形象，经验丰富，热情介绍",
        "speciality": "果树种植专家",
        "voice": "普通话"
    },
    "小张": {
        "name": "小张",
        "gender": "男性",
        "age": "中年",
        "description": "农技专家形象，专业权威，知识丰富",
        "speciality": "农业技术顾问",
        "voice": "标准普通话"
    }
}

# 农产品分类
PRODUCT_CATEGORIES = [
    "特色干果",
    "有机杂粮", 
    "山区蜂蜜",
    "时令水果",
    "绿色蔬菜",
    "农家特产"
]

# 订单状态
ORDER_STATUS = {
    "pending": "待确认",
    "confirmed": "已确认",
    "processing": "备货中",
    "shipped": "已发货",
    "delivered": "已送达",
    "completed": "已完成",
    "cancelled": "已取消"
}

# 数据刷新间隔（秒）
REFRESH_INTERVAL = 30

# 分页配置
PAGINATION = {
    "page_size": 10,
    "max_pages": 100
} 