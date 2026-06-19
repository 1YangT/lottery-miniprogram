"""
随机抽签系统主程序
包含完整的 Streamlit 界面和抽签功能
"""

import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from config.settings import PAGE_CONFIG, APP_CONFIG, THEME_COLORS
from utils.common import load_names, save_names, parse_names
from src.draw_logic import DrawSystem


def main():
    # 页面配置
    st.set_page_config(**PAGE_CONFIG)
    
    # 加载自定义样式
    css_path = os.path.join(current_dir, "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # 加载初始名单
    initial_names = load_names()
    
    # 初始化会话状态
    if "draw_system" not in st.session_state:
        st.session_state.draw_system = DrawSystem(initial_names)
    if "last_drawn" not in st.session_state:
        st.session_state.last_drawn = []
    
    draw_system = st.session_state.draw_system
    
    # 侧边栏
    show_sidebar(draw_system)
    
    # 主界面容器
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 标题
    st.title(f"🎲 {APP_CONFIG['app_name']}")
    st.markdown(f"<p style='text-align: center; color: #6b7280;'>{APP_CONFIG['app_description']}</p>", unsafe_allow_html=True)
    
    # 统计信息
    show_statistics(draw_system)
    
    # 抽签按钮
    show_draw_buttons(draw_system)
    
    # 抽中结果
    show_draw_result()
    
    # 添加名单
    show_add_names(draw_system)
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_sidebar(draw_system: DrawSystem):
    """显示侧边栏"""
    with st.sidebar:
        st.header("📋 名单管理")
        
        # 已抽名单
        st.subheader("已抽名单")
        if draw_system.drawn_names:
            for name in draw_system.drawn_names:
                st.markdown(f"<div class='name-item drawn'><span class='name-text'>{name}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #9ca3af;'>暂无已抽人员</p>", unsafe_allow_html=True)
        
        # 操作按钮
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 重置抽签池", use_container_width=True):
                draw_system.reset()
                st.session_state.last_drawn = []
                st.rerun()
        
        with col2:
            if st.button("🗑️ 清空全部", use_container_width=True):
                draw_system.reset_all()
                save_names([])
                st.session_state.last_drawn = []
                st.rerun()
        
        # 保存名单
        if st.button("💾 保存名单", use_container_width=True):
            save_names(draw_system.all_names)
            st.success("名单已保存！")


def show_statistics(draw_system: DrawSystem):
    """显示统计信息"""
    total = draw_system.get_total_count()
    available = draw_system.get_available_count()
    drawn = draw_system.get_drawn_count()
    
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number">{total}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-label">总人数</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number" style="color: #22c55e;">{available}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-label">剩余可抽</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-number" style="color: #ef4444;">{drawn}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-label">已抽人数</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 进度条
    if total > 0:
        percentage = (drawn / total) * 100
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        st.markdown('<div class="progress-bar">', unsafe_allow_html=True)
        st.markdown(f'<div class="progress-fill" style="width: {percentage}%;"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 0.9rem; color: #6b7280;'>已完成 {percentage:.1f}%</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def show_draw_buttons(draw_system: DrawSystem):
    """显示抽签按钮"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎲 开始抽签")
    
    if draw_system.get_available_count() == 0:
        st.warning("所有人员已抽取完毕！请重置抽签池。")
        return
    
    # 单次抽取
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 单次抽取", use_container_width=True, type="primary"):
            name = draw_system.draw_single()
            if name:
                st.session_state.last_drawn = [name]
                st.rerun()
    
    # 批量抽取
    with col2:
        batch_count = st.number_input("批量抽取人数", min_value=1, max_value=draw_system.get_available_count(), value=3, key="batch_count")
    
    if st.button(f"📦 批量抽取 {batch_count} 人", use_container_width=True):
        names = draw_system.draw_batch(batch_count)
        if names:
            st.session_state.last_drawn = names
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_draw_result():
    """显示抽中结果"""
    if st.session_state.last_drawn:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        if len(st.session_state.last_drawn) == 1:
            st.markdown(f'<div class="result-name">{st.session_state.last_drawn[0]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="result-badge">🎉 恭喜抽中！</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">🎉 恭喜以下人员抽中！</div>', unsafe_allow_html=True)
            for name in st.session_state.last_drawn:
                st.markdown(f'<div style="font-size: 2rem; font-weight: 600; margin-bottom: 0.5rem;">{name}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


def show_add_names(draw_system: DrawSystem):
    """显示添加名单区域"""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("➕ 添加名单")
    
    # 手动输入
    text_input = st.text_area("输入名单（每行一个名字，支持逗号、空格分隔）", key="name_input")
    
    # 文件上传
    uploaded_file = st.file_uploader("或上传名单文件 (.txt)", type="txt")
    
    # 添加按钮
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("添加名单", use_container_width=True):
            if text_input.strip():
                names = parse_names(text_input)
                if names:
                    draw_system.add_names(names)
                    save_names(draw_system.all_names)
                    st.session_state.name_input = ""
                    st.success(f"成功添加 {len(names)} 人！")
                    st.rerun()
                else:
                    st.warning("请输入有效名单！")
    
    with col2:
        if uploaded_file is not None:
            if st.button("上传文件", use_container_width=True):
                try:
                    content = uploaded_file.read().decode("utf-8")
                    names = parse_names(content)
                    if names:
                        draw_system.add_names(names)
                        save_names(draw_system.all_names)
                        st.success(f"成功导入 {len(names)} 人！")
                        st.rerun()
                    else:
                        st.warning("文件内容为空或无效！")
                except Exception as e:
                    st.error(f"文件读取失败: {e}")
    
    # 显示当前名单
    if draw_system.all_names:
        st.markdown("---")
        st.subheader("📝 当前名单")
        st.markdown('<div class="name-list">', unsafe_allow_html=True)
        for name in draw_system.all_names:
            status_class = "drawn" if name in draw_system.drawn_names else ""
            st.markdown(f"<div class='name-item {status_class}'><span class='name-text'>{name}</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
