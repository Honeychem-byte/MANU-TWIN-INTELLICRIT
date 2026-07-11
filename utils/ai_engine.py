import pandas as pd
import os
from tabulate import tabulate
from utils.llm import ask_llm

# Folder containing all Excel workbooks
from pathlib import Path

WORKBOOK_PATH = Path("workbooks")


class AIPlantEngineer:

    def __init__(self):
        """Initialize the AI Plant Engineer."""
        self.loaded_files = {}
        self.load_all_workbooks()

        print("\nLoaded Workbooks:")
        for file in self.loaded_files.keys():
            print(f" - {file}")

    def load_all_workbooks(self):
        """
        Load every Excel workbook inside the workbooks folder.
        """

        if not WORKBOOK_PATH.exists():
            print("Workbook folder not found.")
            return

        for workbook in WORKBOOK_PATH.glob("*.xlsx"):
            try:
                sheets = pd.read_excel(workbook, sheet_name=None)
                self.loaded_files[workbook.name] = sheets
                print(f"Loaded: {workbook.name}")
            except Exception as e:
                print(f"Error loading {workbook.name}")
                print(e)

    def extract_keywords(self, question):
        """
        Extract important search words from the user's question.
        """

        stop_words = {
            "what",
            "why",
            "how",
            "when",
            "where",
            "which",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "did",
            "does",
            "do",
            "please",
            "show",
            "tell",
            "give",
            "about",
            "for",
            "of",
            "to",
            "in",
        }

        words = []
        for word in question.lower().split():
            word = word.strip(",.?")
            if len(word) > 2 and word not in stop_words:
                words.append(word)

        return list(dict.fromkeys(words))

    def search_keyword(self, keyword):
        """
        Search every workbook and every sheet for the given keyword.
        """

        results = []
        keyword = keyword.lower()

        for workbook, sheets in self.loaded_files.items():
            for sheet_name, df in sheets.items():
                try:
                    mask = df.astype(str).apply(
                        lambda col: col.str.lower().str.contains(keyword, na=False)
                    )
                    if mask.any().any():
                        rows = df[mask.any(axis=1)]
                        results.append({
                            "workbook": workbook,
                            "sheet": sheet_name,
                            "rows": rows.head(5),
                        })
                except Exception as e:
                    print(f"Search error in {workbook} -> {sheet_name}")
                    print(e)

        return results

    def answer(self, question):
        # Search matching records
        keywords = self.extract_keywords(question)

        results = []
        for word in keywords:
            results.extend(self.search_keyword(word))

        context = ""
        if len(results) > 0:
            for item in results:
                context += f"""
Workbook: {item['workbook']}

Sheet: {item['sheet']}

{item['rows'].to_markdown(index=False)}
"""
        else:
            context = "No matching historian records were found."

        ai_response = ask_llm(question=question, context=context)
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