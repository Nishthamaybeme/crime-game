import streamlit as st
import pandas as pd
import sqlite3

# Function to load the datasets
def load_data():
    criminals_df = pd.read_csv('criminals.csv')
    crimes_df = pd.read_csv('crimes.csv')
    victim_df = pd.read_csv('victim.csv')
    return criminals_df, crimes_df, victim_df

# Function to create a SQLite database from a DataFrame
def create_db_from_df(df, table_name, conn):
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Function to display the title and introduction
def display_intro():
    st.title("Mystery: The Case of the Sorted Crimes")
    st.image("Murder_Scene_v3-copy_800.png", use_column_width=True)
    st.header("Welcome to our mystery adventure! Explore the sorted crime data and unravel the clues.")
    st.write("""
    A crime has occurred, and the detective requires your assistance. Unfortunately, the crime scene report was soaked when your subordinate accidentally spilled water on it. However, you recall it involves a kidnapping of an adult woman, in a parking lot on 12/08/2023 midnight. Your task is to retrieve this specific crime scene report from the extensive database maintained by the police department.

    All the clues necessary to solve this mystery are contained within this comprehensive database. Utilize SQL to navigate through the data and locate the pertinent crime scene report. This endeavor requires adapting SQL commands to meticulously explore and uncover critical details, regardless of the initial mishap with the report.
    """)
    st.header("Entity Relationship Diagram (ERD)")
    st.write("""
    ERD, which stands for Entity Relationship Diagram, is a visual representation of the relationships among all relevant tables within a database. 
    The diagram shows that each table has a name (top of the box, in bold), a list of column names (on the left) and their corresponding data types (on the right). 
    There is a key icon and a gray line on the ERD. A key indicates that the column is the ​primary key​ of the corresponding table.
    The gray line connects the foreign key of both tables.

    **Primary Key**: a unique identifier for each row in a table.  
    **Foreign Key**: used to reference data in one table to those in another table.  
    If two tables are related, the matching columns, i.e., the common identifiers of the two tables, are connected by a gray line in the diagram.
    """)
    st.image("drawSQL-image-export-2024-07-10.png", caption="ERD for the Mystery Database", width=600)
    st.header("What is a query?")
    st.write("""
    If you were to look at the data in this database, you would see that the tables are huge! There are so many data points; it simply isn’t possible to go through the tables row by row to find the information we need. What are we supposed to do?

    This is where queries come in. Queries are statements we construct to get data from the database. Queries read like natural English (for the most part). Let's try a few queries against our database. For each of the boxes below, click the "run" to "execute" the query in the box. You can edit the queries right here on the page to explore further. (Note that SQL commands are not case-sensitive, but it's conventional to capitalize them for readability. You can also use new lines and white space as you like to format the command for readability. Most database systems require you to end a query with a semicolon (';') although the system for running them in this web page is more forgiving.)
    """)

# Function to execute custom SQL queries
def execute_sql_query(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        data = c.fetchall()
        if data:
            df = pd.DataFrame(data, columns=[desc[0] for desc in c.description])
            st.write(df)
        else:
            st.write("No results found. Check your query and try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    # Set page title and configure layout
    st.set_page_config(page_title="Mystery App", layout="wide")
    
    # Load data
    criminals_df, crimes_df, victim_df = load_data()
    
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('example.db')
    
    # Create tables in SQLite from the DataFrames
    create_db_from_df(crimes_df, 'crimes', conn)
    create_db_from_df(criminals_df, 'criminals', conn)
    create_db_from_df(victim_df, 'victim', conn)
    
    # Display title and introduction
    display_intro()
    
    # Execute custom SQL queries
    st.header("Execute Your SQL Queries")
    
    query1 = st.text_area(" ### Try out SQL queries to review the tables in the ERD. You can change 'crimes' to any other table from the ERD to learn how many rows that table has.",
                          """SELECT * FROM crimes;""",)
    if st.button('Execute'):
        execute_sql_query(conn, query1)
    
    query2 = st.text_area("Dig deeper into the location details in the provided clues to find out.This query allows you to dig deeper into the location details by filtering records based on a specified exact location. The 'WHERE' clause is used to specify the condition that must be met for a record to be included in the result set. In this case, you replace 'INSERT_LOCATION' with the actual location you are investigating to view all crimes that occurred there.",
                          """SELECT *
                             FROM crimes c
                             WHERE c.EXACT_LOCATION = 'INSERT_LOCATION';""")
    if st.button('Run'):
        execute_sql_query(conn, query2)
    
    query3 = st.text_area("Query 3: This query further refines the search by filtering crimes based on both the exact location and the type of crime. The AND operator is used in the WHERE clause to combine multiple conditions that must all be true for a record to be included in the result. This allows you to narrow down the dataset to only those crimes that match both specified criteria.",
                          """SELECT  *
                             FROM crimes c
                             WHERE c.EXACT_LOCATION = 'INSERT_LOCATION'
                             AND c.CRIME='SPECIFY_CRIME';""")
    if st.button('Execute Query 3'):
        execute_sql_query(conn, query3)

    # Additional Queries
    query4 = st.text_area("This query combines data from the crimes and criminals tables using an INNER JOIN on the INCIDENT_AREA column. The SELECT DISTINCT statement ensures that only unique records are returned. The query filters results to display information about a kidnapping that occurred in a parking lot on a specific date. This helps you identify relevant details about the crime and the criminal involved.",
                          """SELECT DISTINCT c.INCIDENT_AREA, cr.CRIMINAL_ID, cr.INCIDENT_DATE, C.WEAPON
                             FROM crimes c
                             JOIN criminals cr ON c.INCIDENT_AREA = cr.INCIDENT_AREA
                             WHERE c.EXACT_LOCATION = 'PARKING LOT' AND c.CRIME='KIDNAPPING' AND cr.INCIDENT_DATE='12/08/2023 12:00:00 AM';""")
    if st.button('Execute Query 4'):
        execute_sql_query(conn, query4)
        # User input block
    st.header("Write the location details you found:")
    user_incident_area = st.text_input("""

You've executed the queries and uncovered vital information. Now, it's time to test your detective skills. Enter the exact crime scene location you discovered. This step will help verify your findings and ensure you're on the right track. Input the incident area below to see if your deduction is correct!
                                       **Enter the Crime Scene Location:**""")
  

    # Predefined solution data
    solution_data = {
        "INCIDENT_AREA": "Southwest"
    }

    # Check answer
    if st.button("Check Answer"):
        if (user_incident_area == solution_data["INCIDENT_AREA"] ):
            st.success("Correct! Your input matches the solution.")
        else:
            st.error("Incorrect! Your input does not match the solution.")

    # Show solution
    if st.button("Show Solution"):
        st.write("The correct solution is:")
        st.write(solution_data)
    query5 = st.text_area(""" Now, Let's Connect to More Tables: Join Multiple Tables Together to Get the Criminals' IDs

Explore deeper insights by integrating data from multiple sources. Joining tables allows us to seamlessly merge information, such as criminal IDs, from different datasets. Let's delve into how we can connect these tables to gain a comprehensive view.""",
                          """SELECT DISTINCT cr.CRIMINAL_ID, v.VICTIM_AGE, v.VICTIM_GENDER
                             FROM crimes c
                             JOIN criminals cr ON c.INCIDENT_AREA = cr.INCIDENT_AREA
                             JOIN victim v ON c.INCIDENT_AREA = v.INCIDENT_AREA
                             WHERE c.EXACT_LOCATION = 'PARKING LOT' AND c.CRIME='KIDNAPPING' AND c.INCIDENT_AREA='Southwest' AND cr.INCIDENT_DATE='12/08/2023 12:00:00 AM'; """)
    if st.button('Execute Query 5'):
        execute_sql_query(conn, query5)

    # Additional Query 6
    st.header('"FIND THE KIDNAPPERRRR!!!!!!!!"')
    query6 = st.text_area('',
                          """SELECT DISTINCT cr.CRIMINAL_ID, v.VICTIM_AGE, v.VICTIM_GENDER,C.CRIME,C.INCIDENT_AREA
                             FROM crimes c
                             JOIN criminals cr ON c.INCIDENT_AREA = cr.INCIDENT_AREA
                             JOIN victim v ON c.INCIDENT_AREA = v.INCIDENT_AREA
                             WHERE c.EXACT_LOCATION = 'PARKING LOT' AND c.CRIME='KIDNAPPING' AND c.INCIDENT_AREA='Southwest' AND cr.INCIDENT_DATE='12/08/2023 12:00:00 AM' and v.VICTIM_AGE='18' AND V.VICTIM_GENDER='F'; """)
    if st.button('Execute Query 6'):
        execute_sql_query(conn, query6)
    


    # Close the connection
    conn.close()

# Run the main function
if __name__ == '__main__':
    main()
