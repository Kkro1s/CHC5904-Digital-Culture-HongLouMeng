# 数据文件说明

## 原始数据
- **Chapter 10- 20/**: 从ctext.org提取的10-20章文本文件

## 处理后的数据

### 文本数据
- **cleaned_texts/**: 清理后的文本文件（移除标题、统一格式）

### 人物词典
- **character_dictionary.json**: 人物名称词典（标准名称和变体）
- **character_dictionary.csv**: 人物词典CSV格式（便于查看）
- **character_mapping.json**: 人物名称到标准名称的映射

### 互动关系数据
- **interactions.csv**: 互动关系表
  - Source: 源人物（薛寶釵）
  - Target: 目标人物
  - Frequency: 互动频率
  - Interaction_Types: 互动类型分布
  - Chapters: 出现的章节
  - Context_1/2/3: 上下文示例

- **interactions_detailed.json**: 详细的互动数据（JSON格式）

### 网络分析结果
- **results/network.gml**: 网络数据（GML格式，可用于Gephi）
- **results/centrality_metrics.csv**: 所有人物的中心性指标
- **results/薛寶釵_metrics.json**: 薛寶釵的详细中心性指标
- **results/network_visualization.png**: 网络可视化图
- **results/centrality_comparison.png**: 中心性对比图
- **results/interactive_network.html**: 交互式网络图（HTML）

## 数据使用说明

1. **interactions.csv**: 可用于进一步分析或导入其他工具
2. **network.gml**: 可在Gephi中打开进行可视化
3. **所有CSV文件**: 可用Excel或其他数据分析工具打开

## 数据来源

所有文本数据来自：https://ctext.org/hongloumeng

