import snowflake.connector
import streamlit as st
from dashboard import display_dashboard
from explorer import explore_snowflake_data
from gloabl import roles
from css import get_custom_css

if "connections" not in st.session_state:
    st.session_state.connections = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = "Hi There"

if 'conn_params' not in st.session_state:
    st.session_state.conn_params = {} 

if 'conn_params' in st.session_state:
    conn_parameters = st.session_state.conn_params
else:
    st.warning("Connection parameters are not set!")
def snowflake_connection():
    custom_css = get_custom_css()
    st.markdown(custom_css, unsafe_allow_html=True)
    st.sidebar.markdown('<h2 style="color: black; font-size: 24px;">🔐 Logged Accounts</h2>', unsafe_allow_html=True)
    st.title("Snowflake Account Setup ")
    with st.form(key="connection_form"):
        account_name = st.text_input("Name this Connection (e.g. Work Account, Personal Account):")
        account_url = st.text_input("Snowflake Account URL (without https://):")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        role = st.selectbox("Choose a Role", roles)
        account_parts = account_url.split('.') if account_url else []
        snowflake_account = account_parts[0] if len(account_parts) > 0 else ""
        region = account_parts[1] if len(account_parts) > 1 else ""

        conn_params = {
            "user": username,
            "password": password,
            "account": snowflake_account,
            "region": region,
            "role": role, 
        }

        if st.form_submit_button("Connect"):
            try:
                with snowflake.connector.connect(**conn_params):
                    st.session_state.connections[account_name] = conn_params
                    st.session_state.current_page = account_name
                    st.success(f"🔗 Connected to {account_name}!")
            except snowflake.connector.errors.DatabaseError as e:
                st.error(f"🚫 Connection failed. Error: {e}")

def main():
    custom_css = get_custom_css()
    st.markdown(custom_css, unsafe_allow_html=True)
    st.sidebar.markdown('<h2 style="color: black; font-size: 24px;">🔐 Logged Accounts</h2>', unsafe_allow_html=True)

    for connection_name in list(st.session_state.connections.keys()):
        col1, col2 = st.sidebar.columns(2)

        if col1.button(f"🔓 Access {connection_name}", key=f"access_{connection_name}"):
            st.session_state.current_page = connection_name

        if col2.button(f"❌ Remove {connection_name}", key=f"remove_{connection_name}"):
            del st.session_state.connections[connection_name]
            if st.session_state.current_page == connection_name:
                st.session_state.current_page = "Hi There"

    if len(st.session_state.connections) > 0:  
        if st.sidebar.button("🔗 Add Another Account"):
            st.session_state.current_page = "Hi There"

    if st.sidebar.button("📊 Dashboard"):
        st.session_state.current_page = "Dashboard"   
    st.sidebar.markdown("---")

    if st.session_state.current_page == "Hi There":
        snowflake_connection()
    elif st.session_state.current_page == "Dashboard":
        display_dashboard()
        if st.button("⬅️ Back to Accounts"):
            st.session_state.current_page = "Hi There"     
    elif st.session_state.current_page in st.session_state.connections:
        st.session_state.conn_params = st.session_state.connections[st.session_state.current_page]
        explore_snowflake_data()
    else:
        st.warning("Invalid page selection 🤷‍♂️.")

if __name__ == "__main__":
    main()

