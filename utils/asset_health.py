import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def asset_health_chart():

    try:

        df = pd.read_excel(
            "workbooks/Workbook_5_Digital_Twin_AI_Mapped.xlsx",
            sheet_name="Asset Health Ranking",
            header=1
        )

        df.columns = [
            "Rank",
            "Equipment",
            "Health Score",
            "Priority",
            "Recommendation",
            "Extra"
        ]

        df = df[df["Rank"] != "Rank"]

        df["Health Score"] = pd.to_numeric(
            df["Health Score"],
            errors="coerce"
        )

        healthy = (df["Health Score"] >= 85).sum()

        warning = (
            (df["Health Score"] >= 70) &
            (df["Health Score"] < 85)
        ).sum()

        critical = (
            df["Health Score"] < 70
        ).sum()

        fig = go.Figure()

        fig.add_trace(

            go.Pie(

                labels=[
                    "Healthy",
                    "Warning",
                    "Critical"
                ],

                values=[
                    healthy,
                    warning,
                    critical
                ],

                hole=0.65,

                textinfo="label+percent"

            )

        )

        fig.update_layout(

            title="Equipment Health Distribution",

            height=420,

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=20
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.metric(
            "Overall Asset Health",
            f"{df['Health Score'].mean():.1f}%"
        )

        return df

    except Exception as e:

        st.error(
            f"Unable to load Asset Health Chart\n\n{e}"
        )

        return None