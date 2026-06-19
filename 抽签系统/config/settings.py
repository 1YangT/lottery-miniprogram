"""
配置文件
包含抽签系统的页面配置和主题设置
"""

# 页面配置
PAGE_CONFIG = {
    "page_title": "🎲 抽签系统",
    "page_icon": "🎲",
    "layout": "centered",
    "initial_sidebar_state": "expanded"
}

# 数据文件路径
DATA_FILE = "data/names.txt"
SAVED_DATA_FILE = "data/draw_history.json"

# 主题颜色
COLORS = {
    "primary": "#10b981",
    "success": "#34d399",
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "highlight": "#fef3c7"
}
