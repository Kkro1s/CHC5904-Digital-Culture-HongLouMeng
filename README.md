# 红楼梦人物社交网络分析项目
## 研究对象：薛寶釵（选中20章）

## 项目结构

```
HongLouMeng/
├── Chapter 10- 20/          # 原始文本文件（1-50章）
├── data/                     # 处理后的数据
│   ├── cleaned_texts/       # 清理后的文本（选中20章）
│   ├── results/             # 分析结果
│   ├── character_dictionary.json
│   ├── character_mapping.json
│   ├── interactions.csv
│   ├── selected_chapters.json  # 选中的章节列表
│   └── ...
├── 0_chapter_selection.py   # 章节选择脚本
├── 1_data_preparation.py    # 阶段一：数据准备
├── 2_interaction_extraction.py  # 阶段二：互动关系识别
├── 3_network_analysis.py    # 阶段三：网络分析
├── 4_advanced_network_analysis.py  # 高级网络分析
├── 4_streamlit_app.py       # 阶段四：Streamlit应用
├── requirements.txt         # Python依赖
└── README.md               # 本文件
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行步骤

### 1. 数据准备
```bash
python3 1_data_preparation.py
```

### 2. 互动关系识别
```bash
python3 2_interaction_extraction.py
```

### 3. 网络分析
```bash
python3 3_network_analysis.py
```

### 4. 启动Streamlit应用
```bash
streamlit run 4_streamlit_app.py
```

应用将在浏览器中自动打开，默认地址：http://localhost:8501

## 数据说明

### 输入数据
- **Chapter 10- 20/**: 从ctext.org提取的1-50章文本文件
- **选中章节**: 根据薛寶釵出现频率选择的20章（7, 8, 22, 25, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 42, 45, 48, 49, 50）

### 输出数据
- **data/interactions.csv**: 互动关系表
- **data/results/centrality_metrics.csv**: 中心性指标表
- **data/results/network.gml**: 网络数据（可用于Gephi）
- **data/results/network_visualization.png**: 网络可视化图
- **data/results/interactive_network.html**: 交互式网络图

## 主要发现

### 薛寶釵的社交网络特点（选中20章）

1. **互动人物**: 19个
2. **总互动次数**: 316次
3. **最频繁的互动**:
   - 賈寶玉: 59次
   - 林黛玉: 58次
   - 賈母: 30次
   - 王夫人: 30次

4. **中心性指标**:
   - 度中心性: 1.0000（最高）
   - 总度数: 19
   - 加权度: 316
   - Hub分数: 1.0000（完美枢纽节点）

## 工具使用

- **数据来源**: ctext.org
- **分析工具**: Python + NetworkX
- **可视化**: Matplotlib, Pyvis
- **展示平台**: Streamlit

## 注意事项

- 所有文本数据来自ctext.org
- 互动关系基于句子级别的共现分析
- 网络分析使用有向图（Directed Graph）

## 作者

CHC5904 Digital Studies of Chinese Culture - Assignment 2

