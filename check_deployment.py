#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署前检查脚本
检查项目是否准备好部署到Streamlit Cloud
"""

import os
import sys

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} 缺失: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """检查目录是否存在"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        file_count = len([f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))])
        print(f"✅ {description}: {dirpath} ({file_count} 个文件)")
        return True
    else:
        print(f"❌ {description} 缺失: {dirpath}")
        return False

def check_requirements():
    """检查requirements.txt中的依赖"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt 文件不存在")
        return False
    
    print("\n📦 检查依赖包:")
    with open("requirements.txt", "r", encoding="utf-8") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        for pkg in packages:
            print(f"  - {pkg}")
    
    return True

def main():
    """主检查函数"""
    print("=" * 60)
    print("🚀 Streamlit Cloud 部署前检查")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # 检查必要文件
    print("📄 检查必要文件:")
    all_ok &= check_file_exists("4_streamlit_app.py", "Streamlit应用主文件")
    all_ok &= check_file_exists("requirements.txt", "Python依赖文件")
    all_ok &= check_file_exists("README.md", "项目说明文件")
    
    print()
    
    # 检查数据目录
    print("📁 检查数据目录:")
    all_ok &= check_directory_exists("data", "数据目录")
    all_ok &= check_file_exists("data/interactions.csv", "互动关系数据")
    all_ok &= check_directory_exists("data/results", "分析结果目录")
    all_ok &= check_file_exists("data/results/centrality_metrics.csv", "中心性指标数据")
    all_ok &= check_file_exists("data/results/薛寶釵_metrics.json", "薛寶釵详细指标")
    
    print()
    
    # 检查依赖
    all_ok &= check_requirements()
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("✅ 所有检查通过！项目已准备好部署。")
        print()
        print("📝 下一步:")
        print("1. 确保所有文件已推送到GitHub")
        print("2. 访问 https://share.streamlit.io/")
        print("3. 使用GitHub账号登录")
        print("4. 点击 'New app' 并选择您的仓库")
        print("5. 设置 Main file path 为: 4_streamlit_app.py")
        print("6. 点击 'Deploy' 开始部署")
        print()
        print("📖 详细步骤请参考: 部署指南.md")
    else:
        print("❌ 检查未通过，请修复上述问题后再部署。")
        sys.exit(1)

if __name__ == "__main__":
    main()

