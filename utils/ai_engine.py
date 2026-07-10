import pandas as pd
import os
from tabulate import tabulate
from utils.llm import ask_llm

# Folder containing all Excel workbooks
WORKBOOK_PATH = r"C:\Users\LENOVO\Desktop\Open hack"


class AIPlantEngineer:

    def __init__(self):
        """Initialize the AI Plant Engineer."""
        self.loaded_files = {}
        self.load_all_workbooks()

        print("\nLoaded Workbooks:")
        for file in self.loaded_files.keys():
            print(f" - {file}")

    def load_all_workbooks(self):
        """Load all Excel workbooks from the specified folder."""

        if not os.path.exists(WORKBOOK_PATH):
            print(f"Folder not found: {WORKBOOK_PATH}")
            return

        for file in os.listdir(WORKBOOK_PATH):

            if file.endswith(".xlsx"):

                file_path = os.path.join(WORKBOOK_PATH, file)

                try:
                    sheets = pd.read_excel(
                        file_path,
                        sheet_name=None
                    )

                    self.loaded_files[file] = sheets
                    print(f"Loaded: {file}")

                except Exception as e:
                    print(f"Could not load {file}")
                    print(e)

    def search_keyword(self, keyword):
        """
        Search every workbook and every sheet
        for the given keyword.
        """

        results = []
        keyword = keyword.lower()

        for workbook, sheets in self.loaded_files.items():

            for sheet_name, df in sheets.items():

                try:
                    mask = df.astype(str).apply(
                        lambda col: col.str.lower().str.contains(
                            keyword,
                            na=False
                        )
                    )

                    if mask.any().any():

                        rows = df[mask.any(axis=1)]

                        results.append({
                            "workbook": workbook,
                            "sheet": sheet_name,
                            "rows": rows.head(5)
                        })

                except Exception as e:
                    print(f"Search error in {workbook} -> {sheet_name}")
                    print(e)

        return results

    def answer(self, question):

        # Search matching records
        results = self.search_keyword(question)

        context = ""

        # Build context from Excel data
        if len(results) > 0:

            for item in results:

                context += f"""

Workbook: {item['workbook']}

Sheet: {item['sheet']}

{item['rows'].to_markdown(index=False)}

"""

        else:

            context = "No matching historian records were found."

        # Send context + question to GPT
        ai_response = ask_llm(
            question=question,
            context=context
        )

        return ai_response

# ----------------------------------------------------------
# Test the class
# ----------------------------------------------------------

if __name__ == "__main__":

    engineer = AIPlantEngineer()

    print("\nAI Plant Engineer Ready!")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("Ask your question: ")

        if question.lower() == "exit":
            break

        answer = engineer.answer(question)

        print("\n" + "=" * 80)
        print(answer)
        print("=" * 80 + "\n")