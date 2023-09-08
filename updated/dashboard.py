from Utility import get_storage_used,credits_used,calculate_storage_cost,calculate_compute_cost
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from gloabl import roles
from css import get_custom_css
st.cache_data
def display_dashboard():
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    connection_names = list(st.session_state.connections.keys())
    selected_connection = st.sidebar.selectbox("Select Connection", connection_names)
    if selected_connection in st.session_state.connections:
        st.session_state.conn_params = st.session_state.connections[selected_connection]
    st.title("📊 Cost Monitoring Dashboard 📊")
    role = st.sidebar.selectbox("Switch Role", roles)
    if role != st.session_state.conn_params.get('role'):
        st.session_state.conn_params['role'] = role
        st.info(f"Role switched to {role}")
    tb_used = get_storage_used()
    credits = credits_used()
    storage_cost = calculate_storage_cost(tb_used)
    compute_cost = calculate_compute_cost(credits)
    data = {
        'Metric': ['Storage Used (MB)', 'Compute Credits Used', 'Total Storage Cost ($)', 'Total Compute Cost ($)'],
        'Value': [tb_used * 1000000, credits, storage_cost, compute_cost]
    }
    df = pd.DataFrame(data)
    st.table(df)
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    threshold = 0.05 * df['Value'].sum()
    mask = df['Value'] > threshold
    tail = df.loc[~mask]
    df_pie = df[mask].copy()
    if tail.shape[0] > 0:
        others_df = pd.DataFrame({
        'Metric': ['Others'],
        'Value': [tail['Value'].sum()]
        })
        df_pie = pd.concat([df_pie, others_df], ignore_index=True)
    ax1.pie(df_pie['Value'], labels=df_pie['Metric'], autopct='%1.1f%%', startangle=90)
    ax1.set_title('Pie Chart: Cost Metrics Distribution')
    st.pyplot(fig1)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['Metric'], df['Value'])
    plt.title('Bar Graph: Metrics')
    plt.xlabel('Metrics')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    for bar in bars:
        yval = bar.get_height()
        if yval > max(df['Value']) * 0.05:
            position = yval - (0.02 * max(df['Value']))
            va = 'top'
        else:
            position = yval + (0.02 * max(df['Value']))
            va = 'bottom'
        plt.text(bar.get_x() + bar.get_width()/2, position, round(yval, 2), ha='center', va=va)
    st.pyplot(fig)