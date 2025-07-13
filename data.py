# 智播农链销售平台演示数据

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# 农产品演示数据
PRODUCTS_DATA = [
    {
        "id": "P001",
        "name": "阜平大枣",
        "category": "特色干果",
        "description": "阜平特产大枣，肉厚核小，营养丰富，是滋补佳品",
        "origin": "河北保定阜平",
        "specification": "500g/袋",
        "original_price": 38.0,
        "current_price": 28.0,
        "stock": 156,
        "sales": 89,
        "rating": 4.8,
        "image": "🍯",
        "features": ["有机种植", "无添加", "传统工艺"],
        "nutrition": "富含维生素C、铁、钙等营养成分"
    },
    {
        "id": "P002", 
        "name": "阜平核桃",
        "category": "特色干果",
        "description": "薄皮核桃，易剥壳，核桃仁饱满，香脆可口",
        "origin": "河北保定阜平",
        "specification": "250g/袋",
        "original_price": 45.0,
        "current_price": 35.0,
        "stock": 203,
        "sales": 156,
        "rating": 4.9,
        "image": "🥜",
        "features": ["薄皮易剥", "营养丰富", "山区特产"],
        "nutrition": "富含蛋白质、不饱和脂肪酸、维生素E"
    },
    {
        "id": "P003",
        "name": "山区蜂蜜",
        "category": "山区蜂蜜", 
        "description": "纯天然蜂蜜，来自阜平山区，无污染环境",
        "origin": "河北保定阜平",
        "specification": "500ml/瓶",
        "original_price": 68.0,
        "current_price": 58.0,
        "stock": 78,
        "sales": 234,
        "rating": 4.7,
        "image": "🍯",
        "features": ["纯天然", "无添加", "山花蜜"],
        "nutrition": "含有多种维生素、矿物质和酶类"
    },
    {
        "id": "P004",
        "name": "有机小米",
        "category": "有机杂粮",
        "description": "富硒小米，有机种植，营养价值高",
        "origin": "河北保定阜平",
        "specification": "1kg/袋",
        "original_price": 32.0,
        "current_price": 26.0,
        "stock": 312,
        "sales": 178,
        "rating": 4.6,
        "image": "🌾",
        "features": ["有机认证", "富硒", "传统品种"],
        "nutrition": "富含蛋白质、维生素B、硒等营养元素"
    },
    {
        "id": "P005",
        "name": "山地苹果",
        "category": "时令水果",
        "description": "高山苹果，昼夜温差大，口感清脆香甜",
        "origin": "河北保定阜平",
        "specification": "2.5kg/箱",
        "original_price": 36.0,
        "current_price": 30.0,
        "stock": 89,
        "sales": 267,
        "rating": 4.8,
        "image": "🍎",
        "features": ["高山种植", "自然成熟", "口感佳"],
        "nutrition": "富含维生素C、膳食纤维、钾等营养成分"
    }
]

# 销售数据
def generate_sales_data():
    """生成销售数据"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    sales_data = []
    
    for date in dates:
        daily_sales = random.randint(3000, 15000)
        orders = random.randint(20, 80)
        customers = random.randint(15, 60)
        
        sales_data.append({
            'date': date,
            'sales_amount': daily_sales,
            'orders': orders,
            'customers': customers,
            'avg_order_value': round(daily_sales / orders, 2)
        })
    
    return pd.DataFrame(sales_data)

# 直播数据
LIVE_STREAMING_DATA = {
    "active_rooms": 3,
    "total_viewers": 1256,
    "today_sales": 8960,
    "month_sales": 156780,
    "total_sales": 1234567,
    "live_rooms": [
        {
            "id": "L001",
            "title": "阜平大枣直播间",
            "avatar": "小王",
            "viewers": 456,
            "sales": 3240,
            "status": "直播中",
            "start_time": "09:00",
            "products": ["阜平大枣", "山区蜂蜜"]
        },
        {
            "id": "L002", 
            "title": "核桃专场直播",
            "avatar": "小李",
            "viewers": 389,
            "sales": 2890,
            "status": "直播中",
            "start_time": "10:30",
            "products": ["阜平核桃", "有机小米"]
        },
        {
            "id": "L003",
            "title": "山地水果直播",
            "avatar": "小张",
            "viewers": 411,
            "sales": 2830,
            "status": "直播中", 
            "start_time": "14:00",
            "products": ["山地苹果"]
        }
    ]
}

# 订单数据
def generate_orders_data():
    """生成订单数据"""
    orders = []
    order_statuses = ["pending", "confirmed", "processing", "shipped", "delivered", "completed"]
    
    for i in range(50):
        order_id = f"ORD{str(i+1).zfill(6)}"
        customer_name = f"客户{i+1}"
        product = random.choice(PRODUCTS_DATA)
        quantity = random.randint(1, 5)
        total_amount = product["current_price"] * quantity
        status = random.choice(order_statuses)
        order_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        orders.append({
            "order_id": order_id,
            "customer_name": customer_name,
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": product["current_price"],
            "total_amount": total_amount,
            "status": status,
            "order_date": order_date,
            "phone": f"138****{random.randint(1000, 9999)}",
            "address": f"保定市阜平县{random.choice(['城关镇', '平阳镇', '王林口镇'])}",
        })
    
    return orders

# 客服问答数据
FAQ_DATA = [
    {
        "question": "阜平大枣的保质期是多久？",
        "answer": "阜平大枣在密封干燥环境下可保存12个月，开封后建议在3个月内食用完毕。",
        "category": "产品咨询"
    },
    {
        "question": "核桃如何保存？",
        "answer": "核桃应存放在阴凉干燥处，避免阳光直射，可冷藏保存延长保质期。",
        "category": "产品咨询"
    },
    {
        "question": "蜂蜜结晶了还能吃吗？",
        "answer": "蜂蜜结晶是正常现象，不影响品质和营养，可隔水加热恢复液态。",
        "category": "产品咨询"
    },
    {
        "question": "如何申请退换货？",
        "answer": "收货后7天内如有质量问题可申请退换货，请联系客服提供订单号和问题照片。",
        "category": "售后服务"
    },
    {
        "question": "配送范围和时间？",
        "answer": "全国包邮，一般3-5个工作日到达，偏远地区可能需要7-10天。",
        "category": "物流配送"
    }
]

# 公告数据
ANNOUNCEMENTS = [
    {
        "title": "🎉 双十一特惠活动开始啦！",
        "content": "全场农产品8折优惠，满100元再减20元！",
        "date": "2024-11-01",
        "type": "promotion"
    },
    {
        "title": "📢 新品上架通知",
        "content": "阜平特产柿饼新鲜上架，限量供应！",
        "date": "2024-10-28",
        "type": "product"
    },
    {
        "title": "🚚 物流升级公告",
        "content": "与顺丰快递合作，配送时效再提升！",
        "date": "2024-10-25",
        "type": "service"
    }
]

# 获取数据的函数
def get_products_data():
    """获取产品数据"""
    return PRODUCTS_DATA

def get_sales_data():
    """获取销售数据"""
    return generate_sales_data()

def get_live_data():
    """获取直播数据"""
    return LIVE_STREAMING_DATA

def get_orders_data():
    """获取订单数据"""
    return generate_orders_data()

def get_faq_data():
    """获取FAQ数据"""
    return FAQ_DATA

def get_announcements():
    """获取公告数据"""
    return ANNOUNCEMENTS 