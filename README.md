## 📌 项目简介
一个基于Python FastAPI搭建的后端服务，正在向RAG（检索增强生成）智能文档问答系统演进。
## 🛠️ 技术栈
Python | FastAPI | Uvicorn | Swagger
## 🚀 核心功能
1. **文件上传**：实现 `POST /upload` 接口，使用 `async/await` 异步处理文件流。
2. **安全防护**：
   - 文件大小限制（5MB）
   - MIME类型白名单校验（防恶意文件）
   - UUID 随机重命名（防路径穿越漏洞）
3. **接口调试**：使用 FastAPI 自动生成的 Swagger UI 进行测试，成功跑通 HTTP 200 与 400 状态码。
## 📅 当前进度
- [x] 基础环境搭建与Hello World接口
- [x] 文件上传与安全存储
- [ ] 接入MySQL数据库解析文档
- [ ] 接入大模型API完成RAG问答闭环