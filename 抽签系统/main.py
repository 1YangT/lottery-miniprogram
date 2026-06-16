"""
抽签系统主程序
包含完整的 Streamlit 界面和交互功能
"""

import streamlit as st
from config.settings import PAGE_CONFIG
from utils.common import (
    load_names_from_file,
    save_names_to_file,
    load_draw_history,
    parse_names_from_text
)
from src.draw_logic import DrawSystem


def main():
    # 页面配置
    st.set_page_config(**PAGE_CONFIG)
    
    # 加载自定义样式
    with open("assets/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # 初始化状态
    if "draw_system" not in st.session_state:
        # 尝试加载历史数据
        history = load_draw_history()
        if history["remaining"]:
            st.session_state.draw_system = DrawSystem(
                history["remaining"], history["drawn"]
            )
        else:
            # 如果没有历史数据，加载默认名单
            default_names = load_names_from_file()
            st.session_state.draw_system = DrawSystem(default_names, [])
    
    if "last_winners" not in st.session_state:
        st.session_state.last_winners = []
    
    draw_system = st.session_state.draw_system
    
    # 页面标题
    st.title("🎲 智能抽签系统")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("📊 状态管理")
        
        # 状态显示
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("剩余人数", f"{draw_system.get_remaining_count()}")
        with col2:
            st.metric("已抽人数", f"{draw_system.get_drawn_count()}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 已抽名单
        st.subheader("📋 已抽名单")
        if draw_system.drawn:
            st.markdown('<div class="drawn-list">', unsafe_allow_html=True)
            for i, name in enumerate(draw_system.drawn, 1):
                st.write(f"{i}. {name}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("暂无已抽人员")
        
        st.markdown("---")
        
        # 重置按钮
        if st.button("🔄 重置抽签池", type="primary"):
            draw_system.reset()
            st.session_state.last_winners = []
            st.success("抽签池已重置！")
            st.rerun()
        
        # 清空按钮
        if st.button("🗑️ 清空所有数据"):
            draw_system.clear_all()
            st.session_state.last_winners = []
            st.warning("所有数据已清空！")
            st.rerun()
    
    # 主内容区
    # 1. 名单管理
    with st.expander("📝 名单管理", expanded=False):
        st.subheader("导入名单")
        
        # 方式一：文件上传
        uploaded_file = st.file_uploader(
            "上传文本文件（每行一个名字）",
            type=["txt"]
        )
        
        if uploaded_file is not None:
            try:
                content = uploaded_file.getvalue().decode("utf-8")
                names = parse_names_from_text(content)
                if st.button("✅ 确认导入文件名单"):
                    draw_system.set_names(names)
                    st.session_state.last_winners = []
                    st.success(f"成功导入 {len(names)} 人！")
                    st.rerun()
            except Exception as e:
                st.error(f"导入失败：{e}")
        
        st.markdown("---")
        
        # 方式二：手动输入
        st.subheader("手动输入名单")
        manual_input = st.text_area(
            "输入名字（支持换行、逗号分隔）",
            height=200,
            placeholder="张三\n李四\n王五\n赵六"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 确认使用手动名单"):
                if manual_input.strip():
                    names = parse_names_from_text(manual_input)
                    draw_system.set_names(names)
                    st.session_state.last_winners = []
                    st.success(f"成功设置 {len(names)} 人！")
                    st.rerun()
                else:
                    st.warning("请输入名字！")
        
        with col2:
            if st.button("📄 加载默认名单"):
                default_names = load_names_from_file()
                if default_names:
                    draw_system.set_names(default_names)
                    st.session_state.last_winners = []
                    st.success(f"成功加载默认名单 {len(default_names)} 人！")
                    st.rerun()
                else:
                    st.error("默认名单文件不存在！")
    
    st.markdown("---")
    
    # 2. 抽签操作
    st.header("🎯 抽签操作")
    
    # 检查是否有剩余人员
    if draw_system.get_remaining_count() == 0:
        st.warning("⚠️ 没有剩余人员！请先导入名单！")
    else:
        # 单次抽取
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("单次抽取")
            if st.button("🎲 抽取 1 人", key="draw_one", use_container_width=True):
                try:
                    winner = draw_system.draw_one()
                    st.session_state.last_winners = [winner]
                    st.balloons()
                except ValueError as e:
                    st.error(str(e))
        
        with col2:
            st.subheader("批量抽取")
            draw_count = st.number_input(
                "抽取人数",
                min_value=1,
                max_value=max(1, draw_system.get_remaining_count()),
                value=1
            )
            if st.button(f"🎲 批量抽取", key="draw_multiple", use_container_width=True):
                try:
                    winners = draw_system.draw_multiple(draw_count)
                    st.session_state.last_winners = winners
                    st.balloons()
                except ValueError as e:
                    st.error(str(e))
        
        st.markdown("---")
        
        # 3. 结果展示
        if st.session_state.last_winners:
            st.header("🎉 中签结果")
            
            if len(st.session_state.last_winners) == 1:
                # 单人展示
                st.markdown('<div class="draw-result">', unsafe_allow_html=True)
                st.markdown(f'<div class="winner-name">{st.session_state.last_winners[0]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # 多人展示
                for i, winner in enumerate(st.session_state.last_winners, 1):
                    st.markdown(f'<div class="draw-result" style="margin: 10px 0; padding: 20px;">', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size: 2rem; font-weight: 800; color: #dc2626;">{i}. {winner}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # 剩余人员预览
    if draw_system.get_remaining_count() > 0:
        with st.expander("👥 查看剩余名单", expanded=False):
            st.write(f"剩余 {draw_system.get_remaining_count()} 人：")
            for i, name in enumerate(draw_system.remaining, 1):
                st.write(f"{i}. {name}")


if __name__ == "__main__":
    main()
