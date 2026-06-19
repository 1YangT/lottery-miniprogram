"""
工具函数模块
包含文件读写、数据处理等通用功能
"""

import json
import os
from typing import List

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_names(file_path: str = None) -> List[str]:
    """
    加载名单数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        名单列表
    """
    if file_path is None:
        file_path = os.path.join(current_dir, "data", "names.txt")
    
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            names = [line.strip() for line in f if line.strip()]
        return names
    except Exception as e:
        print(f"加载名单失败: {e}")
        return []


def save_names(names: List[str], file_path: str = None) -> bool:
    """
    保存名单数据
    
    Args:
        names: 名单列表
        file_path: 文件路径
        
    Returns:
        是否保存成功
    """
    if file_path is None:
        file_path = os.path.join(current_dir, "data", "names.txt")
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for name in names:
                f.write(name + "\n")
        return True
    except Exception as e:
        print(f"保存名单失败: {e}")
        return False


def save_draw_history(history: List[dict], file_path: str = None) -> bool:
    """
    保存抽签历史记录
    
    Args:
        history: 抽签历史列表
        file_path: 文件路径
        
    Returns:
        是否保存成功
    """
    if file_path is None:
        file_path = os.path.join(current_dir, "data", "draw_history.json")
    
    try:
        data = {"history": history}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存抽签历史失败: {e}")
        return False


def load_draw_history(file_path: str = None) -> List[dict]:
    """
    加载抽签历史记录
    
    Args:
        file_path: 文件路径
        
    Returns:
        抽签历史列表
    """
    if file_path is None:
        file_path = os.path.join(current_dir, "data", "draw_history.json")
    
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("history", [])
    except Exception as e:
        print(f"加载抽签历史失败: {e}")
        return []


def parse_names(text: str) -> List[str]:
    """
    解析手动输入的名单
    
    Args:
        text: 输入文本
        
    Returns:
        名单列表
    """
    names = []
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            # 支持逗号、空格、分号分隔
            parts = line.replace('，', ',').replace('；', ';').replace(' ', ',')
            for part in parts.split(','):
                part = part.strip()
                if part:
                    names.append(part)
    return names
