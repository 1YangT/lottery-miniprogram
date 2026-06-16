"""
配置文件
包含页面设置和应用配置
"""

# 页面配置
PAGE_CONFIG = {
    "page_title": "随机抽签系统",
    "page_icon": "🎲",
    "layout": "centered",
    "initial_sidebar_state": "expanded"
}

# 应用配置
APP_CONFIG = {
    "app_name": "随机抽签系统",
    "app_description": "支持单次抽取、批量抽取，抽中人员不可重复",
    "default_names_file": "data/names.txt"
}

# 主题颜色
THEME_COLORS = {
    "primary": "#8b5cf6",
    "secondary": "#6d28d9",
    "success": "#22c55e",
    "warning": "#eab308",
    "danger": "#ef4444",
    "bg": "#f5f3ff",
    "card": "#ffffff"
}
