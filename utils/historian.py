import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import streamlit as st

WORKBOOK_FOLDER = Path("workbooks")


def load_historian():

    workbook = None

    for file in WORKBOOK_FOLDER.glob("*.xlsx"):

        if "Historian" in file.name:

            workbook = file
            break

    if workbook is None:
        return None

    sheets = pd.read_excel(
        workbook,
        sheet_name=None
    )

    return sheets