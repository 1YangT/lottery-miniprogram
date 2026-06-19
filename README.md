# 随机抽签系统

基于 Streamlit 框架开发的随机抽签 Web 应用，支持单次抽取、批量抽取，抽中人员不可重复。

## 技术栈

- Python 3.10+
- Streamlit 1.28+

## 功能特点

- 🎯 **单次抽取** - 一键随机抽取一人
- 📦 **批量抽取** - 自定义抽取人数
- 📋 **名单管理** - 支持手动输入和文件上传
- 🔄 **重置功能** - 重置抽签池或清空全部
- 💾 **本地保存** - 名单自动保存到本地
- 🎨 **美观界面** - 渐变背景、脉冲动画效果

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
streamlit run main.py
```

### 访问地址

- 本地访问：http://localhost:8501

## 项目结构

```
.
├── main.py                   # 主程序文件
├── requirements.txt          # 依赖包列表
├── .gitignore               # Git 忽略文件
├── config/
│   └── settings.py          # 配置文件
├── utils/
│   └── common.py            # 工具函数
├── src/
│   └── draw_logic.py        # 抽签逻辑
├── data/
│   └── names.txt            # 示例名单
└── assets/
    └── style.css            # 样式文件
```

## 部署到 Streamlit Community Cloud

1. 登录 [Streamlit Community Cloud](https://share.streamlit.io/)
2. 点击 "New app"
3. 选择 GitHub 仓库：`1YangT/lottery-miniprogram`
4. 分支：`main`
5. 主文件路径：`main.py`
6. 点击 "Deploy"

## 许可证

MIT License
