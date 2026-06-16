"""
抽签逻辑模块
包含随机抽取、名单管理等核心功能
"""

import random
from typing import List, Tuple
from utils.common import save_draw_history


class DrawSystem:
    """抽签系统类"""
    
    def __init__(self, remaining: List[str] = None, drawn: List[str] = None):
        """
        初始化抽签系统
        
        Args:
            remaining: 剩余名单
            drawn: 已抽名单
        """
        self.remaining = remaining.copy() if remaining else []
        self.drawn = drawn.copy() if drawn else []
    
    def set_names(self, names: List[str]):
        """
        设置抽签名单
        
        Args:
            names: 新的名单列表
        """
        self.remaining = names.copy()
        self.drawn = []
        self._save()
    
    def draw_one(self) -> str:
        """
        抽取一个人
        
        Returns:
            抽中的名字
        
        Raises:
            ValueError: 当没有剩余人员时
        """
        if not self.remaining:
            raise ValueError("没有剩余人员可供抽取！")
        
        # 随机抽取
        index = random.randint(0, len(self.remaining) - 1)
        name = self.remaining.pop(index)
        self.drawn.append(name)
        self._save()
        return name
    
    def draw_multiple(self, count: int) -> List[str]:
        """
        批量抽取多人
        
        Args:
            count: 抽取数量
        
        Returns:
            抽中的名字列表
        
        Raises:
            ValueError: 当抽取数量超过剩余人数时
        """
        if count <= 0:
            raise ValueError("抽取数量必须大于0！")
        
        if count > len(self.remaining):
            raise ValueError(f"抽取数量({count})超过剩余人数({len(self.remaining)})！")
        
        # 随机打乱后抽取
        random.shuffle(self.remaining)
        selected = self.remaining[:count]
        self.remaining = self.remaining[count:]
        self.drawn.extend(selected)
        self._save()
        return selected
    
    def reset(self):
        """重置抽签池"""
        self.remaining.extend(self.drawn)
        self.drawn = []
        self._save()
    
    def clear_all(self):
        """清空所有数据"""
        self.remaining = []
        self.drawn = []
        self._save()
    
    def get_remaining_count(self) -> int:
        """获取剩余人数"""
        return len(self.remaining)
    
    def get_drawn_count(self) -> int:
        """获取已抽人数"""
        return len(self.drawn)
    
    def _save(self):
        """保存当前状态"""
        save_draw_history(self.remaining, self.drawn)
