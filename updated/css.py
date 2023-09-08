import streamlit as st
@st.cache_data
def get_custom_css():
    return """ <style>
    /* Global Settings */
    body {
        background: white;
        font-family: 'Helvetica', 'Arial', sans-serif;
        margin-top: 0px !important;
        padding-top: 0px !important;
    }
    /* Adjusting the form container */
    
    .sidebar {
    color: #f0f0f0; /* Adjust as needed */
    }
    div.stTextInput > div > div > input {
    margin-top: 0px !important;
    }
    .stApp {
        background-color:#bddbcc;
        border-radius: 5px;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.01);
        margin: 2.9% 2.3% ;
        padding: 4%;
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: a28ad1 !important;
        font-size: 18px;
        color: white;
        padding: 2%;
        transition: background-color 0.3s;
    }

    .sidebar .sidebar-content:hover {
        background-color: #a28ad1 !important;
    }

    /* Table styling */
    table {
        border-collapse: collapse;
        border: 3px solid black;
        width: 100%;
        box-shadow: 0 5px 5px rgba(0, 0, 0, 0.1);
        color: black;
    }

    table th, table td {
        border: 3px solid black;
        padding: 6px;
        background: linear-gradient(to bottom right, #FF61D2, #FE9090);
        color: black;
    }

    /* Button Styling */
    button {
        background: #63b4b7;
        color: white;
        border: none;
        border-radius: 7px;
        padding: 12px 24px;
        cursor: pointer;
        transition: transform 0.0s, box-shadow 0.3s;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    h1 {
    font-size: 1;
    font-weight: bold;
    color: #013147;
    margin-bottom: 0px
    margin-up: 0px;
    }
    .stText {
    font-size: 3;
    color: #555;
    line-height: 1.4;
}
.stButton>button {
    margin-bottom: 0px;
    background-color:#75d1cf;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
    transition-duration: 0.4s;
}

.stButton>button:hover {
    background-color: white;
    color:#7597d1;
    border: 2px solid #7597d1;
}

.stTextInput > div > div > input {
    border: 3px solid #0084a6 ;
    padding: 10px;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition-duration: 0.4s;
    font-size: 16px;
}

.stTextInput > div > div > input:focus {
    border-color: #FFC312;
    box-shadow: 0 0 10px #FFC312;
}

.stSelectbox {
    background-color: #bddbcc;
    border: 0;
    padding: 5px 10px;
    width: 100%;
    border-radius: 0px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.6);
}
table {
    width: 100%;
    border-collapse: collapse;
}
table, th, td {
    border: 1px solid #ddd;
}
th, td {
    padding: 8px;
    text-align: left;
}
tr:nth-child(even) {
    background-color: #f2f2f2;
}
th {
    background-color:#7597d1;
    color: white;
}
</style>"""
