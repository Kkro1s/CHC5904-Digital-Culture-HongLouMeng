# Streamlit应用部署指南

本指南介绍如何将薛寶釵社交网络分析应用部署到线上。

## 方法一：Streamlit Cloud（推荐，最简单）

Streamlit Cloud是Streamlit官方提供的免费托管服务，最简单快捷。

### 步骤：

1. **准备GitHub仓库**
   - 将代码推送到GitHub仓库
   - 确保包含以下文件：
     - `4_streamlit_app.py`
     - `requirements.txt`
     - `data/` 目录（包含所有数据文件）

2. **登录Streamlit Cloud**
   - 访问 https://share.streamlit.io/
   - 使用GitHub账号登录

3. **部署应用**
   - 点击 "New app"
   - 选择你的GitHub仓库
   - 设置：
     - **Main file path**: `4_streamlit_app.py`
     - **Python version**: 3.9 或更高
   - 点击 "Deploy"

4. **等待部署完成**
   - 首次部署可能需要几分钟
   - 部署完成后会获得一个公开URL，例如：`https://your-app-name.streamlit.app`

### 注意事项：
- 免费版支持公开仓库
- 数据文件需要包含在仓库中（如果文件很大，考虑使用Git LFS）
- 每次推送到main分支会自动重新部署

---

## 方法二：Heroku

### 步骤：

1. **创建Procfile**
   ```
   web: streamlit run 4_streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **创建setup.sh**（可选，用于安装系统依赖）
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = \$PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **安装Heroku CLI并登录**
   ```bash
   heroku login
   ```

4. **创建应用**
   ```bash
   heroku create your-app-name
   ```

5. **部署**
   ```bash
   git push heroku main
   ```

---

## 方法三：Docker部署（适用于任何云平台）

### 步骤：

1. **创建Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

   ENTRYPOINT ["streamlit", "run", "4_streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **构建和运行**
   ```bash
   docker build -t hongloumeng-app .
   docker run -p 8501:8501 hongloumeng-app
   ```

3. **部署到云平台**
   - AWS ECS/EC2
   - Google Cloud Run
   - Azure Container Instances
   - DigitalOcean App Platform

---

## 方法四：使用PythonAnywhere（免费）

### 步骤：

1. 注册 https://www.pythonanywhere.com/
2. 上传代码文件
3. 在Web标签页创建新的Web应用
4. 配置WSGI文件指向Streamlit应用

---

## 数据文件处理建议

如果数据文件很大，建议：

1. **使用Git LFS**（Large File Storage）
   ```bash
   git lfs install
   git lfs track "data/**/*.csv"
   git lfs track "data/**/*.json"
   git add .gitattributes
   ```

2. **或使用云存储**
   - 将数据文件上传到AWS S3、Google Cloud Storage等
   - 修改代码从云存储加载数据

---

## 推荐方案

**对于本项目，推荐使用Streamlit Cloud**，因为：
- ✅ 完全免费
- ✅ 设置简单
- ✅ 自动部署
- ✅ 无需服务器管理
- ✅ 官方支持

---

## 快速开始（Streamlit Cloud）

1. 确保代码在GitHub上
2. 访问 https://share.streamlit.io/
3. 连接GitHub仓库
4. 部署！

部署完成后，你的应用将有一个公开的URL，可以分享给任何人访问。



