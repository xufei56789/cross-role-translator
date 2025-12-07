# Cross Role Translator

跨角色翻译器 - 一个基于 AI 的智能翻译工具，帮助不同角色（产品经理、开发者、设计师、运营、高管）之间进行内容转换和翻译。

## 项目简介

本项目旨在解决不同角色之间沟通的障碍，通过 AI 技术将内容从一种角色视角转换为另一种角色视角，同时提供场景检测、信息补全建议和风险提示等功能。

## 技术栈

### 后端
- **FastAPI** -  Python Web 框架
- **LangGraph** - 用于构建 AI 工作流
- **LangChain** - AI 应用开发框架
- **豆包 API** - 大语言模型服务
- **Uvicorn** - ASGI 服务器

### 前端
- **Vue 3** - 前端框架
- **Vite** - 前端构建工具

## 项目结构

```
cross-role-translator/
├── cross-role-translator-server/    # 后端服务
│   └── app/
│       ├── main.py                  # FastAPI 应用入口
│       ├── graph.py                 # LangGraph 工作流定义
│       ├── schemas.py               # 数据模型定义
│       └── prompts.py               # AI 提示词
├── cross-role-translator-vue/       # 前端应用
│   └── src/
│       ├── App.vue                  # 主应用组件
│       └── components/              # Vue 组件
└── README.md                        # 项目说明文档
```

## 快速开始

### 前期准备

1. **获取豆包 API Key**
   - 访问豆包开放平台获取 API Key

2. **配置环境变量**
   ```shell
   cd cross-role-translator-server/app
   vim .env
   ```
   
   在 `.env` 文件中添加：
   ```env
   DOUBAO_API_KEY="your-api-key-here"
   ```

### 启动服务端

1. **创建并激活 Conda 环境**
   ```shell
   cd cross-role-translator-server
   conda create -n cross-role-translator-server -y python=3.12
   conda activate cross-role-translator-server
   ```

2. **安装依赖**
   ```shell
   pip install -r requirements.txt
   ```

3. **启动服务**
   ```shell
   uvicorn app.main:app --reload --port 8000
   ```

   服务启动后，API 文档可访问：http://localhost:8000/docs

### 启动前端

**环境要求：** Node.js v22.12.0

1. **安装依赖**
   ```shell
   cd cross-role-translator-vue
   npm install
   ```

2. **启动开发服务器**
   ```shell
   npm run dev
   ```

   前端应用将在 http://localhost:5173 运行（Vite 默认端口）

## API 接口

### 健康检查
- **GET** `/health`
- 返回服务状态

### 翻译接口
- **POST** `/api/translate`
- 请求体：
  ```json
  {
    "source_role": "product_manager",
    "target_role": "developer",
    "content": "需要实现一个用户登录功能"
  }
  ```
- 响应体：
  ```json
  {
    "detected_scene": "功能需求",
    "translated_message": "需要开发用户认证模块...",
    "info_completion": [...],
    "risk_alerts": [...],
    "suggestion_for_source": "..."
  }
  ```

## 支持的角色类型

- `product_manager` - 产品经理
- `developer` - 开发者
- `designer` - 设计师
- `operator` - 运营
- `executive` - 高管


