#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试中文字体配置
"""

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import os

# 复制4_streamlit_app.py中的字体设置函数
def setup_chinese_font():
    """设置中文字体，优先使用系统中可用的字体"""
    chinese_fonts = [
        'Arial Unicode MS',  # macOS
        'SimHei',  # Windows
        'Microsoft YaHei',  # Windows
        'WenQuanYi Micro Hei',  # Linux
        'WenQuanYi Zen Hei',  # Linux
        'Noto Sans CJK SC',  # Linux/通用
        'Noto Sans CJK TC',  # Linux/通用
        'Source Han Sans CN',  # Linux/通用
        'STHeiti',  # macOS备用
        'Lantinghei SC',  # macOS备用
        'DejaVu Sans',  # 回退字体
    ]
    
    try:
        available_fonts = [f.name for f in fm.fontManager.ttflist]
    except:
        available_fonts = []
    
    font_found = None
    font_path = None
    
    for font in chinese_fonts:
        if font in available_fonts:
            font_found = font
            try:
                for font_file in fm.fontManager.ttflist:
                    if font_file.name == font:
                        font_path = font_file.fname
                        break
            except:
                pass
            break
    
    if font_found is None:
        try:
            for font_file in fm.fontManager.ttflist:
                font_name = font_file.name
                if any(keyword in font_name.lower() for keyword in ['cjk', 'chinese', 'han', 'hei', 'song', 'lanting', 'st']):
                    font_found = font_name
                    font_path = font_file.fname
                    break
        except:
            pass
    
    if font_found:
        matplotlib.rcParams['font.sans-serif'] = [font_found] + chinese_fonts
    else:
        matplotlib.rcParams['font.sans-serif'] = chinese_fonts
    
    matplotlib.rcParams['axes.unicode_minus'] = False
    
    font_prop = None
    if font_found:
        try:
            if font_path and os.path.exists(font_path):
                font_prop = fm.FontProperties(fname=font_path)
            else:
                font_prop = fm.FontProperties(family=font_found)
        except Exception as e:
            try:
                font_prop = fm.FontProperties(family=font_found)
            except:
                pass
    
    return font_found, font_prop

# 测试字体配置
print("=" * 60)
print("中文字体配置测试")
print("=" * 60)

font_name, font_prop = setup_chinese_font()

print(f"\n检测到的中文字体: {font_name if font_name else '未找到'}")
if font_prop:
    print(f"FontProperties创建成功: {font_prop.get_name()}")
else:
    print("FontProperties创建失败")

# 测试中文显示
print("\n测试中文显示...")
fig, ax = plt.subplots(figsize=(10, 6))

# 测试数据
test_labels = ['对话', '行为', '共同出现']
test_values = [100, 50, 30]

bars = ax.bar(test_labels, test_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])

# 设置字体
if font_prop:
    ax.set_xticks(range(len(test_labels)))
    ax.set_xticklabels(test_labels, fontproperties=font_prop)
    ax.set_title('中文字体测试 - Interaction Type Distribution', fontproperties=font_prop, fontsize=14)
else:
    ax.set_xticks(range(len(test_labels)))
    ax.set_xticklabels(test_labels)
    ax.set_title('中文字体测试 - Interaction Type Distribution', fontsize=14)

ax.set_ylabel('Frequency', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# 保存测试图片
output_file = 'font_test.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"\n✅ 测试图表已保存: {output_file}")
print("\n请检查图片中的中文是否正常显示：")
print("  - x轴标签：对话、行为、共同出现")
print("  - 标题：中文字体测试")

plt.close()

# 列出所有可用的中文字体
print("\n" + "=" * 60)
print("系统中可用的中文字体（前10个）：")
print("=" * 60)
chinese_fonts_found = []
for font_file in fm.fontManager.ttflist:
    font_name = font_file.name
    if any(keyword in font_name.lower() for keyword in ['cjk', 'chinese', 'han', 'hei', 'song', 'lanting', 'st']):
        if font_name not in chinese_fonts_found:
            chinese_fonts_found.append(font_name)
            if len(chinese_fonts_found) <= 10:
                print(f"  - {font_name}")

print(f"\n总共找到 {len(chinese_fonts_found)} 个中文字体")

