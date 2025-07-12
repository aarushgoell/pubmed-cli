# 🔬 PubMed CLI Tool — Aganitha Backend Take-Home

This is a command-line tool that queries the PubMed API and extracts research papers authored by **non-academic (biotech/pharma)** contributors. It filters out academic affiliations using custom logic and exports the results as a CSV.

---

## 📦 Tools & Libraries Used

- [Python 3.10+](https://www.python.org/)
- [Poetry](https://python-poetry.org/) — for dependency and packaging
- [Biopython](https://biopython.org/) — to interact with PubMed API (Entrez + Medline)
- [pandas](https://pandas.pydata.org/) — for tabular data handling and CSV output
- [argparse](https://docs.python.org/3/library/argparse.html) — for CLI interface
- [regex](https://docs.python.org/3/library/re.html) — for email extraction

---

## 🛠️ Installation

### Install via Poetry (recommended)

````
git clone https://github.com/<your-username>/pubmed-cli.git
cd pubmed-cli
poetry install


🚀 How to Use the Tool

Run the CLI using:
poetry run get-papers-list "QUERY" --max_result 10 --filename results.csv --debug


✅ Arguments:

  Flag	           Description
  query	           PubMed search query (quoted)
--max_result	   Number of papers to fetch (default: 5)
--filename	     Output CSV filename (default: pubmed_results.csv)
--debug	          Print debug info to console

⚙️ How It Works

Takes a PubMed query using Entrez.esearch

Fetches article metadata using Entrez.efetch in Medline format

Parses:

Title, PMID, Abstract, Authors, Affiliation, Email

Applies non-academic author filter

Exports qualifying results to a CSV file

🧠 Filtering Logic (Non-Academic Author Detection):

The tool considers an affiliation to be non-academic if it does NOT contain any of these keywords (case-insensitive):
["university", "college", "institute", "school", "hospital", "department", "lab"]
If any author in the paper has a non-academic affiliation, the paper is included.

📤 Example Commands

poetry run get-papers-list "Pfizer AND cancer" --max_result 5 --filename pfizer_papers.csv --debug

poetry run get-papers-list "machine learning and 2024" --filename ml_output.csv

📄 Example Output CSV
PMID	Title	Publication Date	Non-academic Authors	Company Affiliations	Corresponding Author Email
123456	COVID Vaccine Trial	2024-06-01	John Smith	Pfizer, Inc.	john.smith@pfizer.com

❗ Assumptions Made
A paper is included if at least one author is non-academic.

Affiliation is matched by keyword heuristics (basic substring check).

Email is extracted using regex from the affiliation field.

📂 Project Structure

pubmed-cli/
├── pubmed_cli/
│   ├── __init__.py
│   └── main.py           # CLI logic and core functions
├── pyproject.toml        # Poetry config and entry point
├── README.md             # You're reading it!
└── .gitignore

🧪 Testing
To test:


poetry run get-papers-list "Novartis AND oncology" --max_result 3 --debug


👨‍💻 Author
Aarush Goel
Email: aarushgoel2004@gmail.com
GitHub: github.com/aarushgoell
````
