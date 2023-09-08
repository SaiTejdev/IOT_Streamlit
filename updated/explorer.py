from Utility import get_schemas,get_databases,get_tables,get_columns,execute_query,get_views,get_dynamic_tables,get_dynamic_columns
import streamlit as st
import pandas as pd
from gloabl import roles
from css import get_custom_css
from datetime import datetime
st.cache_data
def explore_snowflake_data():
    st.markdown('<h1 style="color: #013147; font-size: 60px;">Snowflake Explorer</h1>', unsafe_allow_html=True)
    st.sidebar.title("Data")
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    role = st.sidebar.selectbox("Switch Role", roles)
    if role != st.session_state.conn_params.get('role'):
        st.session_state.conn_params['role'] = role
        st.info(f"Role switched to {role}")

    databases = get_databases()
    selected_database = st.sidebar.selectbox("Select Database", databases)

    if selected_database:
        schemas = get_schemas(selected_database)
        selected_schema = st.sidebar.selectbox("Select Schema", schemas)

        if selected_schema:
            data_source_type = st.sidebar.radio("Choose Data Source Type", ["Table", "View", "Dynamic Tables"])
            if data_source_type == "Table":
                items = get_tables(selected_database, selected_schema)
            elif data_source_type == "View":
                items = get_views(selected_database, selected_schema)
            elif data_source_type == "Dynamic Tables":
                items = get_dynamic_tables(selected_database, selected_schema)     

            selected_item = st.sidebar.selectbox(f"Select {data_source_type}", items)
            if selected_item :
                if data_source_type == "Dynamic Tables":
                    columns = get_dynamic_columns(selected_database, selected_schema, selected_item)
                    selected_columns = st.sidebar.multiselect("Select Columns", columns, default=columns)
                else:    
                    columns = get_columns(selected_database, selected_schema, selected_item)
                    selected_columns = st.sidebar.multiselect("Select Columns", columns, default=columns)
            
                where_clause = ""
                join_clause = ""

                if st.sidebar.checkbox("Operator Filtering?"):
                    filter_column = st.sidebar.selectbox("Filter by Column", ["None"] + columns)
                    conditions = ["=", ">", "<", "LIKE", "ALIKE", "BETWEEN"]
                    condition = st.sidebar.selectbox("Condition", conditions)
                    if condition == "BETWEEN":
                        lower_value = st.sidebar.text_input("Lower Value")
                        upper_value = st.sidebar.text_input("Upper Value")
                        if filter_column != "None" and lower_value and upper_value:
                            where_clause = f'WHERE "{filter_column}" BETWEEN \'{lower_value}\' AND \'{upper_value}\''
                    else:
                        filter_value = st.sidebar.text_input("Filter Value")
                        if filter_column != "None" and filter_value:
                            where_clause = f'WHERE "{filter_column}" {condition} \'{filter_value}\''

                if st.sidebar.checkbox("Date-Time Filtering?"):
                    ultra_filter_columns = st.sidebar.multiselect("Select Columns for Ultra Filtering", columns)
                    if ultra_filter_columns:
                        for col in ultra_filter_columns:
                            max_min_query = f'SELECT MAX("{col}"), MIN("{col}") FROM "{selected_database}"."{selected_schema}"."{selected_item}"'
                            max_min_result = execute_query(max_min_query)
                            if max_min_result and len(max_min_result) > 0:
                                max_time, min_time = max_min_result[0]
                                st.sidebar.text(f"Max for {col}: {max_time}")
                                st.sidebar.text(f"Min for {col}: {min_time}")         
                        ultra_start_date = st.sidebar.date_input("Start Date")
                        ultra_end_date = st.sidebar.date_input("End Date")
                        time_choices = [f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}" for h in range(24) for m in range(60) for s in range(60)]
                        ultra_start_time_str = st.sidebar.selectbox("Select Start Time", options=time_choices)
                        ultra_end_time_str = st.sidebar.selectbox("Select End Time", options=time_choices)
                        ultra_start_time = datetime.strptime(ultra_start_time_str, "%H:%M:%S").time()
                        ultra_end_time = datetime.strptime(ultra_end_time_str, "%H:%M:%S").time()
                        ultra_start_datetime = datetime.combine(ultra_start_date, ultra_start_time)
                        ultra_end_datetime = datetime.combine(ultra_end_date, ultra_end_time)
                        ultra_start_str = ultra_start_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                        ultra_end_str = ultra_end_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
                        ultra_time_conditions = [f'"{col}" BETWEEN \'{ultra_start_str}\' AND \'{ultra_end_str}\'' for col in ultra_filter_columns]
                        ultra_where_clause = " AND ".join(ultra_time_conditions)
                        if where_clause:
                            where_clause = f"{where_clause} AND {ultra_where_clause}"
                        else:
                            where_clause = f"WHERE {ultra_where_clause}"

                if st.sidebar.checkbox("Column Based Filters?"):
                    Column_Based_Filters = st.sidebar.multiselect("Select Columns for Column Based Filters?", columns)
                    column_filter_clauses = []
                    for filter_col in Column_Based_Filters:
                        unique_values_query = f'SELECT DISTINCT "{filter_col}" FROM "{selected_database}"."{selected_schema}"."{selected_item}"'
                        unique_values_result = execute_query(unique_values_query)

                        if unique_values_result:
                            unique_values = [row[0] for row in unique_values_result]
                            selected_value = st.sidebar.selectbox(f"Select unique value for {filter_col}", unique_values)
                            column_filter_clauses.append(f'"{filter_col}" = \'{selected_value}\'')
                    if column_filter_clauses:
                        column_filter_where_clause = " AND ".join(column_filter_clauses)
                        if where_clause:
                            where_clause = f"{where_clause} AND ({column_filter_where_clause})"
                        else:
                            where_clause = f"WHERE {column_filter_where_clause}"  

                if st.sidebar.checkbox("Join Filters?"):
                    join_databases = get_databases()
                    join_database = st.sidebar.selectbox("Join Database", join_databases)
                    join_schemas = get_schemas(join_database)
                    join_schema = st.sidebar.selectbox("Join Schema", join_schemas)
                    join_tables_views = get_tables(join_database, join_schema) + get_views(join_database, join_schema)
                    join_table_view = st.sidebar.selectbox("Join with Table/View", join_tables_views)
                    join_types = ['INNER JOIN', 'LEFT OUTER JOIN', 'RIGHT OUTER JOIN', 'FULL OUTER JOIN']
                    join_type = st.sidebar.selectbox("Join Type", join_types)
                    join_column_self = st.sidebar.selectbox("Join on this column from your table/view", columns)
                    join_column_other = st.sidebar.selectbox("Join on this column from the other table/view", get_columns(join_database, join_schema, join_table_view))
                    join_clause = f'{join_type} "{join_database}"."{join_schema}"."{join_table_view}" ON "{selected_database}"."{selected_schema}"."{selected_item}"."{join_column_self}" = "{join_database}"."{join_schema}"."{join_table_view}"."{join_column_other}"'     

                sanitized_database = selected_database.replace('"', '""')
                sanitized_schema = selected_schema.replace('"', '""')
                sanitized_item = selected_item.replace('"', '""')

                filtered_row_count_query = f'SELECT COUNT(*) FROM "{sanitized_database}"."{sanitized_schema}"."{sanitized_item}" {join_clause} {where_clause}'

                result = execute_query(filtered_row_count_query)
                
                if result is None or len(result) == 0:
                    st.error("There was an issue executing the row count query. Please check your database configuration or selected parameters.")
                    return

                filtered_row_count = result[0][0]

                if filtered_row_count == 1:
                    st.sidebar.text("Only 1 row available.")
                    row_limit = 1
                else:
                    row_limit = st.sidebar.slider("Row Limit", min_value=1, max_value=filtered_row_count, value=min(110, filtered_row_count), step=1)
                
                columns_to_query = ', '.join([f'"{sanitized_item}"."{col}"' for col in selected_columns])
                query = f'SELECT {columns_to_query} FROM "{sanitized_database}"."{sanitized_schema}"."{sanitized_item}" {join_clause} {where_clause} LIMIT {row_limit}'
                result = execute_query(query)

                if result is None or len(result) == 0:
                    st.error("No data found for the selected query.")
                    return

                df = pd.DataFrame(result, columns=selected_columns)
                st.dataframe(df)

                default_query1 = f'SELECT * FROM "{sanitized_database}"."{sanitized_schema}"."{sanitized_item}"'
                user_query = st.text_area("Write your SQL query here:", value=default_query1)

                if st.button("Execute Custom Query"):
                    result = execute_query(user_query)
                    if result and len(result) > 0:
                        df = pd.DataFrame(result)
                        st.dataframe(df)
                    else:
                        st.write("No results returned.")
