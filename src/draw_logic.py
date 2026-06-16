"""
抽签逻辑模块
包含随机抽取核心逻辑
"""

import random
from typing import List, Tuple, Optional
from utils.common import save_draw_history, load_draw_history


class DrawSystem:
    """
    抽签系统类
    管理名单、已抽人员和抽取逻辑
    """
    
    def __init__(self, names: List[str]):
        """
        初始化抽签系统
        
        Args:
            names: 初始名单
        """
        self.all_names = names.copy()
        self.available_names = names.copy()
        self.drawn_names = []
        self.history = load_draw_history()
    
    def add_names(self, names: List[str]):
        """
        添加名单
        
        Args:
            names: 要添加的名单列表
        """
        for name in names:
            if name.strip() and name not in self.all_names:
                self.all_names.append(name)
                self.available_names.append(name)
    
    def remove_name(self, name: str):
        """
        移除名单
        
        Args:
            name: 要移除的名字
        """
        if name in self.all_names:
            self.all_names.remove(name)
            if name in self.available_names:
                self.available_names.remove(name)
            if name in self.drawn_names:
                self.drawn_names.remove(name)
    
    def draw_single(self) -> Optional[str]:
        """
        单次抽取
        
        Returns:
            抽中的名字，如果没有可抽人员则返回 None
        """
        if not self.available_names:
            return None
        
        name = random.choice(self.available_names)
        self.available_names.remove(name)
        self.drawn_names.append(name)
        
        # 记录到历史
        self.history.append({
            "type": "single",
            "names": [name],
            "remaining": len(self.available_names)
        })
        save_draw_history(self.history)
        
        return name
    
    def draw_batch(self, count: int) -> List[str]:
        """
        批量抽取
        
        Args:
            count: 抽取数量
            
        Returns:
            抽中的名字列表
        """
        if not self.available_names:
            return []
        
        # 实际抽取数量不能超过剩余人数
        actual_count = min(count, len(self.available_names))
        
        drawn = random.sample(self.available_names, actual_count)
        
        for name in drawn:
            self.available_names.remove(name)
            self.drawn_names.append(name)
        
        # 记录到历史
        self.history.append({
            "type": "batch",
            "count": count,
            "names": drawn,
            "remaining": len(self.available_names)
        })
        save_draw_history(self.history)
        
        return drawn
    
    def reset(self):
        """重置抽签池"""
        self.available_names = self.all_names.copy()
        self.drawn_names = []
    
    def reset_all(self):
        """完全重置（清空所有数据）"""
        self.all_names = []
        self.available_names = []
        self.drawn_names = []
        self.history = []
        save_draw_history(self.history)
    
    def get_available_count(self) -> int:
        """
        获取剩余可抽人数
        
        Returns:
            剩余人数
        """
        return len(self.available_names)
    
    def get_drawn_count(self) -> int:
        """
        获取已抽人数
        
        Returns:
            已抽人数
        """
        return len(self.drawn_names)
    
    def get_total_count(self) -> int:
        """
        获取总人数
        
        Returns:
            总人数
        """
        return len(self.all_names)
