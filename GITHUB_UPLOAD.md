# GitHub上传指南

## 快速上传步骤

### 1. 添加文件到Git

运行以下命令添加必要的文件：

```bash
# 添加核心应用文件
git add 4_streamlit_app.py
git add requirements.txt
git add README.md
git add STREAMLIT_README.md
git add DEPLOYMENT_GUIDE.md

# 添加配置文件
git add .gitignore
git add .streamlit/config.toml
git add Dockerfile
git add Procfile
git add setup.sh

# 添加数据文件（重要！）
git add data/

# 可选：添加其他文档
git add *.md
```

### 2. 提交更改

```bash
git commit -m "Initial commit: Xue Baochai social network analysis Streamlit app"
```

### 3. 添加GitHub远程仓库

**请将下面的URL替换为你的GitHub仓库地址：**

```bash
git remote add origin https://github.com/你的用户名/你的仓库名.git
```

例如：
```bash
git remote add origin https://github.com/kkrois/HongLouMeng.git
```

### 4. 推送到GitHub

```bash
git branch -M main
git push -u origin main
```

---

## 完整命令（一键复制）

**请先替换GitHub仓库URL，然后运行：**

```bash
# 添加文件
git add 4_streamlit_app.py requirements.txt README.md STREAMLIT_README.md DEPLOYMENT_GUIDE.md .gitignore .streamlit/ Dockerfile Procfile setup.sh data/ *.md

# 提交
git commit -m "Initial commit: Xue Baochai social network analysis Streamlit app"

# 添加远程仓库（替换为你的GitHub仓库URL）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送
git branch -M main
git push -u origin main
```

---

## 如果远程仓库已存在

如果之前已经添加过远程仓库，使用：

```bash
git remote set-url origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

---

## 注意事项

1. **确保GitHub仓库已创建**（在GitHub网站上创建）
2. **数据文件较大**：首次推送可能需要一些时间
3. **如果推送失败**：检查GitHub仓库URL是否正确
4. **需要认证**：可能需要输入GitHub用户名和密码（或使用Personal Access Token）

---

## 验证上传

上传完成后，访问你的GitHub仓库页面，应该能看到：
- ✅ `4_streamlit_app.py`
- ✅ `requirements.txt`
- ✅ `data/` 目录及其所有文件
- ✅ 其他配置文件

然后就可以在Streamlit Cloud上部署了！

