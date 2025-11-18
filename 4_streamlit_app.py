#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 4: Create Streamlit Interactive Application
Display social network analysis results for Xue Baochai (薛寶釵)
"""

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.font_manager as fm
import json
import os

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Xue Baochai Social Network Analysis",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try importing pyvis, use alternative if failed
try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    PYVIS_AVAILABLE = False
    # Store error for debugging (won't display until after set_page_config)
    _pyvis_error = str(e)

# 配置中文字体 - 兼容Streamlit Cloud
def setup_chinese_font():
    """设置中文字体，优先使用系统中可用的字体"""
    # 尝试查找可用的中文字体
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
    
    # 获取系统中所有可用字体
    try:
        available_fonts = [f.name for f in fm.fontManager.ttflist]
    except:
        available_fonts = []
    
    # 查找第一个可用的中文字体
    font_found = None
    font_path = None
    
    for font in chinese_fonts:
        if font in available_fonts:
            font_found = font
            # 查找字体文件路径
            try:
                for font_file in fm.fontManager.ttflist:
                    if font_file.name == font:
                        font_path = font_file.fname
                        break
            except:
                pass
            break
    
    # 如果找不到，尝试查找包含'CJK'或'Chinese'的字体
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
    
    # 设置matplotlib全局字体
    if font_found:
        matplotlib.rcParams['font.sans-serif'] = [font_found] + chinese_fonts
    else:
        # 如果找不到中文字体，使用默认字体列表
        matplotlib.rcParams['font.sans-serif'] = chinese_fonts
    
    matplotlib.rcParams['axes.unicode_minus'] = False
    
    # 创建FontProperties对象用于networkx
    font_prop = None
    if font_found:
        try:
            if font_path and os.path.exists(font_path):
                font_prop = fm.FontProperties(fname=font_path)
            else:
                font_prop = fm.FontProperties(family=font_found)
        except Exception as e:
            # 如果创建FontProperties失败，尝试使用字体名称
            try:
                font_prop = fm.FontProperties(family=font_found)
            except:
                pass
    
    return font_found, font_prop

# 初始化字体配置
CHINESE_FONT, CHINESE_FONT_PROP = setup_chinese_font()

# Configuration
OUTPUT_DIR = "data"
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results")
TARGET_CHARACTER = "薛寶釵"

@st.cache_data
def load_data():
    """Load all data"""
    # Load interaction data
    df_interactions = pd.read_csv(os.path.join(OUTPUT_DIR, "interactions.csv"))
    
    # Load centrality metrics
    df_metrics = pd.read_csv(os.path.join(RESULTS_DIR, "centrality_metrics.csv"))
    
    # Load detailed metrics
    with open(os.path.join(RESULTS_DIR, f"{TARGET_CHARACTER}_metrics.json"), 'r', encoding='utf-8') as f:
        target_metrics = json.load(f)
    
    # Build network
    G = nx.DiGraph()
    for _, row in df_interactions.iterrows():
        if G.has_edge(row['Source'], row['Target']):
            G[row['Source']][row['Target']]['weight'] += row['Frequency']
        else:
            G.add_edge(row['Source'], row['Target'], weight=row['Frequency'])
    
    return df_interactions, df_metrics, target_metrics, G

def create_interactive_network(G, target_char):
    """Create interactive network graph (using pyvis)"""
    # Use CDN for better compatibility in Streamlit
    net = Network(
        height="600px", 
        width="100%", 
        bgcolor="#ffffff",  # Changed to white background for better visibility
        font_color="black",  # Changed to black text for better visibility
        cdn_resources="remote"  # Use CDN instead of local files
    )
    net.set_options("""
    {
      "nodes": {
        "font": {"size": 14, "color": "black"},
        "scaling": {"min": 10, "max": 30},
        "borderWidth": 2,
        "borderColor": "#2B7CE9"
      },
      "edges": {
        "arrows": {"to": {"enabled": true, "scaleFactor": 1.2}},
        "smooth": {"type": "continuous"},
        "color": {"color": "#848484", "highlight": "#848484"}
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "centralGravity": 0.1,
          "springLength": 200,
          "springConstant": 0.04,
          "damping": 0.09
        },
        "stabilization": {"iterations": 100}
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "hideEdgesOnDrag": false
      }
    }
    """)
    
    # Add nodes
    for node in G.nodes():
        if node == target_char:
            net.add_node(node, label=node, color="#ff0000", size=30, 
                        title=f"{node}<br>Target Character<br>Degree: {G.degree(node)}")
        else:
            degree = G.degree(node)
            net.add_node(node, label=node, color="#87CEEB", size=10 + degree * 2, 
                        title=f"{node}<br>Degree: {degree}")
    
    # Add edges
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1)
        net.add_edge(u, v, value=weight, title=f"{u} → {v}: {weight} times")
    
    return net

def main():
    # Title
    st.title("📚 Xue Baochai Social Network Analysis")
    st.markdown("---")
    
    # Load selected chapters info
    try:
        with open(os.path.join(OUTPUT_DIR, "selected_chapters.json"), 'r', encoding='utf-8') as f:
            chapters_info = json.load(f)
        selected_chapters = chapters_info['selected_chapters']
        chapters_str = ", ".join(map(str, selected_chapters))
        st.markdown(f"**Research Scope:** 20 selected chapters from Dream of the Red Chamber (Chapters 1-50)")
        st.markdown(f"**Selected Chapters:** {chapters_str}")
        st.markdown("**Research Subject:** Xue Baochai (薛寶釵)")
    except:
        st.markdown("**Research Scope:** 20 selected chapters from Dream of the Red Chamber (Chapters 1-50)")
        st.markdown("**Research Subject:** Xue Baochai (薛寶釵)")
    
    # Load data
    try:
        df_interactions, df_metrics, target_metrics, G = load_data()
    except Exception as e:
        st.error(f"Data loading failed: {e}")
        st.stop()
    
    # Sidebar
    st.sidebar.header("📊 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Overview", "Network Visualization", "Centrality Analysis", "Interaction Details", "Data Download"]
    )
    
    if page == "Overview":
        st.header("📈 Research Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Interacting Characters", len(df_interactions))
        
        with col2:
            st.metric("Total Interactions", int(df_interactions['Frequency'].sum()))
        
        with col3:
            st.metric("Network Nodes", G.number_of_nodes())
        
        with col4:
            st.metric("Network Edges", G.number_of_edges())
        
        st.markdown("---")
        
        # Key findings
        st.subheader("🔍 Key Findings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Most Frequent Interactions")
            top_interactions = df_interactions.nlargest(5, 'Frequency')[['Target', 'Frequency', 'Chapters']]
            for idx, row in top_interactions.iterrows():
                st.markdown(f"**{row['Target']}**: {int(row['Frequency'])} times (Chapters: {row['Chapters']})")
        
        with col2:
            st.markdown("### Xue Baochai's Centrality Metrics")
            st.markdown(f"- **Degree Centrality**: {target_metrics['degree_centrality']:.4f}")
            st.markdown(f"- **Total Degree**: {target_metrics['total_degree']}")
            st.markdown(f"- **Weighted Degree**: {target_metrics['weighted_degree']}")
            st.markdown(f"- **Betweenness Centrality**: {target_metrics['betweenness_centrality']:.4f}")
            st.markdown(f"- **PageRank**: {target_metrics['pagerank']:.4f}")
        
        # Interaction type distribution
        st.subheader("📊 Interaction Type Distribution")
        interaction_types = []
        for _, row in df_interactions.iterrows():
            types_str = row['Interaction_Types']
            for type_info in types_str.split('、'):
                if '(' in type_info:
                    type_name = type_info.split('(')[0]
                    count = int(type_info.split('(')[1].split(')')[0])
                    interaction_types.extend([type_name] * count)
        
        type_df = pd.DataFrame({'Type': interaction_types})
        type_counts = type_df['Type'].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        type_counts.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        
        # 设置字体属性，确保中文正常显示
        font_prop = {'fontsize': 12}
        if CHINESE_FONT:
            font_prop['fontfamily'] = CHINESE_FONT
        
        ax.set_xlabel('Interaction Type', **font_prop)
        ax.set_ylabel('Frequency', **font_prop)
        title_prop = {'fontsize': 14}
        if CHINESE_FONT:
            title_prop['fontfamily'] = CHINESE_FONT
        ax.set_title('Interaction Type Distribution', **title_prop)
        
        # 设置x轴标签字体，确保中文正常显示
        ax.set_xticklabels(type_counts.index, rotation=45, ha='right', **font_prop)
        plt.tight_layout()
        st.pyplot(fig)
    
    elif page == "Network Visualization":
        st.header("🕸️ Network Visualization")
        
        st.markdown("### Interactive Network Graph")
        st.markdown("Click nodes to view details, drag nodes to adjust layout")
        
        if PYVIS_AVAILABLE:
            try:
                # Create interactive network
                net = create_interactive_network(G, TARGET_CHARACTER)
                
                # Save HTML file
                html_file = os.path.join(RESULTS_DIR, "interactive_network.html")
                net.save_graph(html_file)
                
                # Get absolute path
                abs_html_path = os.path.abspath(html_file)
                
                # Provide download button and direct link
                st.info("💡 **Note**: For best experience, please open the interactive network graph in a new browser tab.")
                
                col1, col2 = st.columns(2)
                with col1:
                    # Read HTML file for download
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    st.download_button(
                        label="📥 Download Interactive Network Graph",
                        data=html_content,
                        file_name="interactive_network.html",
                        mime="text/html"
                    )
                
                with col2:
                    # Try to display in Streamlit (may not work perfectly)
                    st.markdown(f"""
                    <a href="file://{abs_html_path}" target="_blank" style="
                        display: inline-block;
                        padding: 10px 20px;
                        background-color: #FF4B4B;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                    ">🔗 Open in New Tab</a>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("**Preview (embedded view - may have limitations):**")
                
                # Try to display in Streamlit with improved HTML
                html_str = net.generate_html()
                
                # Ensure HTML is properly formatted for Streamlit
                # Add a wrapper div to ensure proper rendering
                html_wrapped = f"""
                <div style="width: 100%; height: 700px; overflow: hidden;">
                {html_str}
                </div>
                """
                
                st.components.v1.html(html_wrapped, height=700, scrolling=False)
                
            except Exception as e:
                st.error(f"Error creating interactive network: {e}")
                import traceback
                with st.expander("Error Details (click to view)"):
                    st.code(traceback.format_exc())
                st.info("Falling back to static network graph.")
                st.markdown("Below is the static network graph:")
        else:
            st.info("Interactive network graph requires pyvis library. Please run: `pip install pyvis` and restart the Streamlit app.")
            st.markdown("Below is the static network graph:")
        
        st.markdown("---")
        
        # Static network graph
        st.markdown("### Static Network Graph")
        fig, ax = plt.subplots(figsize=(14, 10))
        
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        node_colors = ['red' if node == TARGET_CHARACTER else 'lightblue' for node in G.nodes()]
        node_sizes = [G.degree(node) * 500 + 500 for node in G.nodes()]
        edge_widths = [G[u][v].get('weight', 1) * 2 for u, v in G.edges()]
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, ax=ax, alpha=0.7)
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, edge_color='gray', 
                             ax=ax, arrows=True, arrowsize=20)
        # 使用配置的中文字体 - networkx只支持font_family参数（字符串）
        # 由于已经设置了matplotlib的全局字体，使用'sans-serif'会自动使用配置的中文字体
        label_font = CHINESE_FONT if CHINESE_FONT else 'sans-serif'
        nx.draw_networkx_labels(G, pos, font_size=10, ax=ax, font_family=label_font)
        
        # Add edge labels
        edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax, font_size=8)
        
        # 设置标题字体
        network_title_prop = {'fontsize': 16}
        if CHINESE_FONT:
            network_title_prop['fontfamily'] = CHINESE_FONT
        ax.set_title('Xue Baochai Social Network Graph', **network_title_prop)
        ax.axis('off')
        
        st.pyplot(fig)
    
    elif page == "Centrality Analysis":
        st.header("📊 Centrality Analysis")
        
        st.markdown("### Interaction Frequency Comparison")
        st.markdown("*Shows the frequency of interactions with Xue Baochai (薛寶釵)*")
        
        # Use interaction frequency instead of degree for comparison
        # Merge interaction data with metrics to get frequency
        df_with_freq = df_metrics.merge(
            df_interactions[['Target', 'Frequency']].rename(columns={'Target': 'character'}),
            on='character',
            how='left'
        )
        # For Xue Baochai, use weighted_degree as total frequency
        df_with_freq.loc[df_with_freq['character'] == TARGET_CHARACTER, 'Frequency'] = \
            df_with_freq.loc[df_with_freq['character'] == TARGET_CHARACTER, 'weighted_degree']
        # Fill NaN with 0
        df_with_freq['Frequency'] = df_with_freq['Frequency'].fillna(0)
        
        # Sort by frequency (excluding Xue Baochai for comparison chart)
        df_others = df_with_freq[df_with_freq['character'] != TARGET_CHARACTER].copy()
        df_sorted = df_others.sort_values('Frequency', ascending=False)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        colors = ['#FF6B6B' if freq >= 20 else '#4ECDC4' if freq >= 10 else '#95E1D3' 
                 for freq in df_sorted['Frequency']]
        bars = ax.barh(range(len(df_sorted)), df_sorted['Frequency'], color=colors, alpha=0.8)
        ax.set_yticks(range(len(df_sorted)))
        
        # 设置字体属性，确保中文人物名称正常显示
        freq_font_prop = {'fontsize': 10}
        if CHINESE_FONT:
            freq_font_prop['fontfamily'] = CHINESE_FONT
        ax.set_yticklabels(df_sorted['character'], **freq_font_prop)
        
        label_prop = {'fontsize': 12}
        title_prop = {'fontsize': 14}
        if CHINESE_FONT:
            label_prop['fontfamily'] = CHINESE_FONT
            title_prop['fontfamily'] = CHINESE_FONT
        
        ax.set_xlabel('Interaction Frequency (times)', **label_prop)
        ax.set_title('Interaction Frequency with Xue Baochai', **title_prop)
        ax.grid(axis='x', alpha=0.3)
        
        # 设置数值标签字体
        text_prop = {'fontsize': 9}
        if CHINESE_FONT:
            text_prop['fontfamily'] = CHINESE_FONT
        for i, (char, freq) in enumerate(zip(df_sorted['character'], df_sorted['Frequency'])):
            ax.text(freq + 1, i, str(int(freq)), va='center', **text_prop)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Show Xue Baochai's total interactions separately
        xue_total = df_with_freq[df_with_freq['character'] == TARGET_CHARACTER]['Frequency'].values[0]
        st.info(f"**Xue Baochai (薛寶釵) Total Interactions:** {int(xue_total)} times with {len(df_others)} characters")
        
        st.markdown("---")
        
        # Centrality metrics table
        st.markdown("### Detailed Centrality Metrics")
        
        # Merge with interaction frequency data
        df_display = df_metrics.merge(
            df_interactions[['Target', 'Frequency']].rename(columns={'Target': 'character'}),
            on='character',
            how='left'
        )
        # For Xue Baochai, use weighted_degree as total frequency
        df_display.loc[df_display['character'] == TARGET_CHARACTER, 'Frequency'] = \
            df_display.loc[df_display['character'] == TARGET_CHARACTER, 'weighted_degree']
        df_display['Frequency'] = df_display['Frequency'].fillna(0).astype(int)
        
        # Select columns to display (prioritize meaningful metrics)
        display_cols = ['character', 'Frequency', 'degree', 'in_degree', 'out_degree']
        if 'degree_centrality' in df_display.columns:
            display_cols.extend(['degree_centrality', 'betweenness_centrality', 'closeness_centrality'])
        
        df_display = df_display[display_cols].copy()
        
        # Sort by frequency (descending)
        df_display = df_display.sort_values('Frequency', ascending=False)
        
        # Rename columns for display
        column_mapping = {
            'character': 'Character',
            'Frequency': 'Interaction Frequency',
            'degree': 'Degree',
            'in_degree': 'In-Degree',
            'out_degree': 'Out-Degree',
            'degree_centrality': 'Degree Centrality',
            'betweenness_centrality': 'Betweenness Centrality',
            'closeness_centrality': 'Closeness Centrality'
        }
        df_display.columns = [column_mapping.get(col, col) for col in df_display.columns]
        
        # Format the dataframe for better display
        styled_df = df_display.style.format({
            'Interaction Frequency': '{:.0f}',
            'Degree': '{:.0f}',
            'In-Degree': '{:.0f}',
            'Out-Degree': '{:.0f}',
            'Degree Centrality': '{:.4f}',
            'Betweenness Centrality': '{:.4f}',
            'Closeness Centrality': '{:.4f}'
        })
        
        # Highlight maximum values (excluding Character column)
        numeric_cols = [col for col in df_display.columns if col != 'Character']
        styled_df = styled_df.highlight_max(axis=0, subset=numeric_cols, color='#ffcccc')
        
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # Add explanation
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; margin-top: 10px;'>
        <strong>Note:</strong>
        <ul style='margin: 5px 0; padding-left: 20px;'>
            <li><strong>Interaction Frequency</strong>: Number of interactions with Xue Baochai (most meaningful metric for this network)</li>
            <li><strong>Degree</strong>: Number of connections (all characters except Xue Baochai have degree=1 in this star network)</li>
            <li><strong>In-Degree</strong>: Number of incoming connections (all characters except Xue Baochai have in-degree=1)</li>
            <li><strong>Out-Degree</strong>: Number of outgoing connections (only Xue Baochai has out-degree>0)</li>
            <li><strong>Degree Centrality</strong>: Normalized degree centrality (0-1 scale)</li>
            <li><strong>Betweenness Centrality</strong>: Measures how often a node appears on shortest paths</li>
            <li><strong>Closeness Centrality</strong>: Measures average distance to all other nodes</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    elif page == "Interaction Details":
        st.header("📝 Interaction Details")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            selected_chars = st.multiselect(
                "Select Characters",
                options=df_interactions['Target'].unique(),
                default=df_interactions['Target'].tolist()
            )
        
        with col2:
            min_freq = st.slider("Minimum Interaction Frequency", 1, int(df_interactions['Frequency'].max()), 1)
        
        # Filter data
        filtered_df = df_interactions[
            (df_interactions['Target'].isin(selected_chars)) & 
            (df_interactions['Frequency'] >= min_freq)
        ].sort_values('Frequency', ascending=False)
        
        st.markdown(f"### Displaying {len(filtered_df)} interaction records")
        
        # Display interaction table
        display_cols = ['Target', 'Frequency', 'Interaction_Types', 'Chapters', 
                       'Context_1', 'Context_2']
        st.dataframe(
            filtered_df[display_cols].rename(columns={
                'Target': 'Target Character',
                'Frequency': 'Frequency',
                'Interaction_Types': 'Interaction Types',
                'Chapters': 'Chapters',
                'Context_1': 'Context 1',
                'Context_2': 'Context 2'
            }),
            use_container_width=True,
            height=400
        )
        
        # Detailed context
        st.markdown("### Detailed Context")
        selected_interaction = st.selectbox(
            "Select interaction relationship to view detailed context",
            options=[f"{row['Target']} ({row['Frequency']} times)" 
                   for _, row in filtered_df.iterrows()]
        )
        
        if selected_interaction:
            target_name = selected_interaction.split(' (')[0]
            interaction_row = filtered_df[filtered_df['Target'] == target_name].iloc[0]
            
            st.markdown(f"**{TARGET_CHARACTER} ↔ {target_name}**")
            st.markdown(f"- **Frequency**: {interaction_row['Frequency']} times")
            st.markdown(f"- **Types**: {interaction_row['Interaction_Types']}")
            st.markdown(f"- **Chapters**: {interaction_row['Chapters']}")
            
            if pd.notna(interaction_row['Context_1']):
                st.markdown("**Context 1:**")
                st.text(interaction_row['Context_1'])
            if pd.notna(interaction_row['Context_2']):
                st.markdown("**Context 2:**")
                st.text(interaction_row['Context_2'])
    
    elif page == "Data Download":
        st.header("💾 Data Download")
        
        st.markdown("### Download Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="Download Interactions Table (CSV)",
                data=df_interactions.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
                file_name="interactions.csv",
                mime="text/csv"
            )
        
        with col2:
            st.download_button(
                label="Download Centrality Metrics (CSV)",
                data=df_metrics.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
                file_name="centrality_metrics.csv",
                mime="text/csv"
            )
        
        with col3:
            metrics_json = json.dumps(target_metrics, ensure_ascii=False, indent=2)
            st.download_button(
                label="Download Xue Baochai Detailed Metrics (JSON)",
                data=metrics_json.encode('utf-8'),
                file_name="baochai_metrics.json",
                mime="application/json"
            )
        
        st.markdown("---")
        st.markdown("### Data Description")
        st.markdown("""
        - **interactions.csv**: Contains detailed information of all interaction relationships
        - **centrality_metrics.csv**: Contains centrality metrics for all characters
        - **baochai_metrics.json**: Detailed centrality metrics for Xue Baochai (JSON format)
        """)
    
    # Footer
    st.markdown("---")
    # Footer with correct research scope
    try:
        with open(os.path.join(OUTPUT_DIR, "selected_chapters.json"), 'r', encoding='utf-8') as f:
            chapters_info = json.load(f)
        selected_chapters = chapters_info['selected_chapters']
        chapters_str = ", ".join(map(str, selected_chapters))
        footer_text = f"Dream of the Red Chamber Character Social Network Analysis | Data Source: ctext.org | Research Scope: 20 selected chapters from Chapters 1-50 ({chapters_str})"
    except:
        footer_text = "Dream of the Red Chamber Character Social Network Analysis | Data Source: ctext.org | Research Scope: 20 selected chapters from Chapters 1-50"
    
    st.markdown(f"""
    <div style='text-align: center; color: gray;'>
    <p>{footer_text}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

