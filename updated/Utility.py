import decimal
import streamlit as st
import snowflake.connector
from gloabl import storage_cost_per_tb ,cost_per_node_per_hour 

st.cache_data    
def execute_query(query, database=None):
    try:
        with snowflake.connector.connect(**st.session_state.conn_params) as conn:
            with conn.cursor() as cursor:
                # Set the database if provided
                if database:
                    cursor.execute(f"USE DATABASE {database}")
                cursor.execute(query)
                return cursor.fetchall()
    except snowflake.connector.errors.ProgrammingError as e:
        # Displaying more detailed error information
        st.error(f"Error Code: {e.errno}\nError Message: {e.msg}\nSQL State: {e.sqlstate}\nError Class: {e.__class__}\nExecuted Query: {query}")
        if st.button("⬅️ Back to Accounts"):
            st.session_state.current_page = "Hi There"
        return []
    except Exception as e:
        st.error(f"Unexpected error executing query: {e}\nExecuted Query: {query}")
        if st.button("⬅️ Back to Accounts"):
            st.session_state.current_page = "Hi There"
        return []

st.cache_data
def get_storage_used():
    query = 'SELECT USAGE_DATE, STORAGE_BYTES, ROUND(STORAGE_BYTES / 1024 / 1024 / 1024, 2) AS STORAGE_GB FROM SNOWFLAKE.ACCOUNT_USAGE.STORAGE_USAGE ORDER BY USAGE_DATE DESC LIMIT 1;' 
    result = execute_query(query)
    if not result:
        return 0.0
    storage_value = result[0][2]
    if isinstance(storage_value, decimal.Decimal):   
        storage_value = float(storage_value)
    elif not isinstance(storage_value, (int, float)):
        raise ValueError(f"Unexpected data type for storage: {type(storage_value)}, value: {storage_value}")
    return storage_value

st.cache_data
def credits_used():
    query = 'SELECT SUM(CREDITS_USED) FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_HISTORY'
    result = execute_query(query)
    print("Result from get_credits_used:", result)  
    if not result:
        return 0
    credit_value = result[0][0]
    if isinstance(credit_value, decimal.Decimal):
        return float(credit_value)
    if not isinstance(credit_value, (int, float)):
        raise ValueError(f"Unexpected data type for credits: {type(credit_value)}, value: {credit_value}")
    return credit_value

st.cache_data
def calculate_storage_cost(tb_used):
    if not isinstance(tb_used, (int, float)):
        raise ValueError(f"Unexpected data type for tb_used: {type(tb_used)}, value: {tb_used}")
    return tb_used * storage_cost_per_tb

st.cache_data
def calculate_compute_cost(credits):
    if not isinstance(credits, (int, float)):
        raise ValueError(f"Unexpected data type for credits: {type(credits)}, value: {credits}")
    return credits * cost_per_node_per_hour

st.cache_data
def get_accounts(database):
    sanitized_database = database.replace('"', '""')
    result = execute_query(f'SHOW SCHEMAS IN DATABASE "{sanitized_database}"')
    return [account[0] for account in result if isinstance(account, tuple) and len(account) > 0]

st.cache_data
def get_warehouses():
    query = 'SHOW WAREHOUSES'
    results = execute_query(query)
    return [warehouse[0] for warehouse in results if isinstance(warehouse, tuple) and len(warehouse) > 0]

st.cache_data
def get_databases():
    query = 'SHOW DATABASES'
    results = execute_query(query)
    return [database[1] for database in results if isinstance(database, tuple) and len(database) > 1]

st.cache_data
def get_schemas(database):
    sanitized_database = database.replace('"', '""') 
    result = execute_query(f'SHOW SCHEMAS IN DATABASE "{sanitized_database}"')
    return [schema[1] for schema in result if isinstance(schema, tuple) and len(schema) > 1]

st.cache_data
def get_tables(database, schema):
    sanitized_database = database.replace('"', '""')
    sanitized_schema = schema.replace('"', '""')
    tables_result = execute_query(f'SHOW TABLES IN "{sanitized_database}"."{sanitized_schema}"')
    return [table[1] for table in tables_result if isinstance(table, tuple) and len(table) > 1]

def get_dynamic_tables(database, schema):
    sanitized_database = database.replace('"', '""')
    sanitized_schema = schema.replace('"', '""')
    DYNAMIC_TABLES_result = execute_query(f'SHOW DYNAMIC TABLES IN "{sanitized_database}"."{sanitized_schema}"')
    return [DYNAMIC_TABLES[1] for DYNAMIC_TABLES in DYNAMIC_TABLES_result if isinstance(DYNAMIC_TABLES, tuple) and len(DYNAMIC_TABLES) > 1]

def get_dynamic_columns(database, schema, dynamic_tables):
    sanitized_database = database.replace('"', '""')
    sanitized_schema = schema.replace('"', '""')
    sanitized_table = dynamic_tables.replace('"', '""')
    column_query = f"DESCRIBE DYNAMIC TABLE \"{sanitized_database}\".\"{sanitized_schema}\".\"{sanitized_table}\""
    query_result = execute_query(column_query)    
    columns_result = [row[0] for row in query_result if isinstance(row, tuple) and len(row) > 1]
    return columns_result


st.cache_data
def get_views(database, schema):
    sanitized_database = database.replace('"', '""')
    sanitized_schema = schema.replace('"', '""')
    views_result = execute_query(f'SHOW views IN "{sanitized_database}"."{sanitized_schema}"')
    return [views[1] for views in views_result if isinstance(views, tuple) and len(views) > 1]

st.cache_data
def get_columns(database, schema, table):
    sanitized_database = database.replace('"', '""')
    sanitized_schema = schema.replace('"', '""')
    sanitized_table = table.replace('"', '""')
    column_query = f"SHOW COLUMNS IN TABLE \"{sanitized_database}\".\"{sanitized_schema}\".\"{sanitized_table}\""
    columns_result = execute_query(column_query)
    return [col[2] for col in columns_result if isinstance(col, tuple) and len(col) > 2]
