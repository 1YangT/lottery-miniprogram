"""
工具函数模块
包含文件读写、数据处理等通用功能
"""

import json
import os
from typing import List, Tuple
from config.settings import DATA_FILE, SAVED_DATA_FILE


def load_names_from_file(file_path: str = DATA_FILE) -> List[str]:
    """
    从文本文件加载名单
    
    Args:
        file_path: 文件路径
    
    Returns:
        名单列表
    """
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            names = [line.strip() for line in f.readlines() if line.strip()]
        return names
    except Exception as e:
        print(f"加载文件出错: {e}")
        return []


def save_names_to_file(names: List[str], file_path: str = DATA_FILE) -> bool:
    """
    保存名单到文本文件
    
    Args:
        names: 名单列表
        file_path: 文件路径
    
    Returns:
        是否保存成功
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for name in names:
                f.write(f"{name}\n")
        return True
    except Exception as e:
        print(f"保存文件出错: {e}")
        return False


def load_draw_history() -> dict:
    """
    加载抽签历史记录
    
    Returns:
        历史记录字典
    """
    if not os.path.exists(SAVED_DATA_FILE):
        return {
            "remaining": [],
            "drawn": []
        }
    
    try:
        with open(SAVED_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载历史记录出错: {e}")
        return {
            "remaining": [],
            "drawn": []
        }


def save_draw_history(remaining: List[str], drawn: List[str]) -> bool:
    """
    保存抽签历史记录
    
    Args:
        remaining: 剩余名单
        drawn: 已抽名单
    
    Returns:
        是否保存成功
    """
    try:
        data = {
            "remaining": remaining,
            "drawn": drawn
        }
        with open(SAVED_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存历史记录出错: {e}")
        return False


def parse_names_from_text(text: str) -> List[str]:
    """
    从文本解析名单
    
    Args:
        text: 输入文本
    
    Returns:
        名单列表
    """
    # 支持逗号、换行、空格分隔
    names = []
    # 先按换行分割
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            # 尝试按逗号分割
            parts = line.replace('，', ',').split(',')
            for part in parts:
                part = part.strip()
                if part:
                    names.append(part)
    return names
