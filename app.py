# pylint: disable=missing-module-docstring
import logging
import os
import subprocess
import duckdb
import streamlit as st
import sys
from streamlit.logger import get_logger
from datetime import date, timedelta

app_logger = get_logger(__name__)
app_logger.setLevel(logging.INFO)

if "data" not in os.listdir():
    # logging.error(os.listdir())
    # logging.error("creating folder data")
    app_logger.info(os.listdir())
    app_logger.info("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    # exec(open("init_db.py").read())
    app_logger.info("Create Database and tables")
    subprocess.run([sys.executable, "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Checks that user SQL query is correct b:
    1: checking the columns
    2: checking the values
    :param user_query: a string containing the input query by the user
    :return: None
    """
    global e
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct !")
            st.balloons()
    except KeyError as e:
        st.write("Some columns are missing")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )


with st.sidebar:
    available_themes_df = con.execute(f"SELECT DISTINCT theme FROM memory_state ").df()
    theme = st.selectbox(
        "What would you like to review",
        # ("cross_joins", "GroupBy", "Windows Functions"),
        available_themes_df["theme"].tolist(),
        index=None,
        placeholder="Select a theme...",
    )
    try:
        st.write("You selected:", theme)

        exercise = (
            con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ")
            .df()
            .sort_values("last_reviewed")
        )
        st.write(exercise)

        exercise_name = exercise.iloc[0]["exercise_name"]
        with open(f"answers/{exercise_name}.sql", "r") as f:
            answer = f.read()

        solution_df = con.execute(answer).df()
    except Exception as e:
        st.write("")

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    check_users_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

if st.button("Reset"):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    try:
        # exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
        exercise_tables = exercise.iloc[0]["tables"]
        for table in exercise_tables:
            st.write(f"table: {table}")
            df_table = con.execute(f"SELECT * FROM '{table}'").df()
            st.dataframe(df_table)

    except Exception as e:
        st.write("")

with tab3:
    try:
        st.text(answer)

    except Exception as e:
        st.write("")
