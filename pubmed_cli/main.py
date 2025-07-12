import argparse
from Bio import Entrez
from Bio import Medline
import pandas as pd
import re

Entrez.email = "aarushgoel2004@gmail.com"

def search_pubmed(query: str, max_results: int = 1) -> list:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = ["university", "college", "institute", "school", "hospital", "department", "lab"]
    return not any(keyword in affiliation.lower() for keyword in academic_keywords)

def extract_email(affiliation_field) -> str:
    if isinstance(affiliation_field, list):
        text = " ".join(affiliation_field)
    elif isinstance(affiliation_field, str):
        text = affiliation_field
    else:
        return "N/A"

    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group() if match else "N/A"

def fetch_metadata(pubmed_ids: list) -> list:
    handle = Entrez.efetch(db="pubmed", id=",".join(pubmed_ids), rettype="medline", retmode="text")
    records = Medline.parse(handle)

    results = []

    for record in records:
        affiliations = record.get("AD", [])
        authors = record.get("FAU", [])
        if isinstance(affiliations, str):
            affiliations = [affiliations]

        non_academic_authors = []
        company_affiliations = []

        for author, affil in zip(authors, affiliations):
            if is_non_academic(affil):
                non_academic_authors.append(author)
                company_affiliations.append(affil)

        # Only include paper if at least one non-academic author exists
        if non_academic_authors:
            results.append({
                "PMID": record.get("PMID", ""),
                "Title": record.get("TI", "N/A"),
                "Publication Date": record.get("DP", "N/A"),
                "Non-academic Authors": ", ".join(non_academic_authors),
                "Company Affiliations": "; ".join(company_affiliations),
                "Corresponding Author Email": extract_email(record.get("AD", ""))
            })

    return results

def main():
    parser = argparse.ArgumentParser(
        description="🔍 PubMed Search CLI Tool — Fetch research papers with industry authors and save as CSV"
    )

    parser.add_argument(
    "--debug",
    action="store_true",
    help="Print debug information during execution"
    )

    parser.add_argument(
        "query",
        type=str,
        help="Search term for PubMed (e.g. 'cancer AND Pfizer')"
    )

    parser.add_argument(
        "--max_result",
        type=int,
        default=5,
        help="Number of papers to fetch (default: 5)"
    )

    parser.add_argument(
        "--filename",
        type=str,
        default="pubmed_results.csv",
        help="Output CSV filename (default: 'pubmed_results.csv')"
    )

    args = parser.parse_args()

    print(f"\n🔍 Searching PubMed for: {args.query}")
    ids = search_pubmed(args.query, max_results=args.max_result)

    if args.debug:
        print("[DEBUG] Search results:", ids)

    if not ids:
        print("❌ No papers found. Please try a different query.")
        exit()

    print("📄 Paper IDs:", ids)

    papers = fetch_metadata(ids)

    if args.debug:
      print(f"[DEBUG] Found {len(papers)} papers with non-academic authors")

    if not papers:
        print("❌ No non-academic authors found in the results.")
        exit()

    # Show papers in terminal
    for p in papers:
        print("\n📝 Title:", p["Title"])
        print("🆔 PMID:", p["PMID"])
        print("📅 Publication Date:", p["Publication Date"])
        print("👨‍💼 Non-academic Authors:", p["Non-academic Authors"])
        print("🏢 Company Affiliations:", p["Company Affiliations"])
        print("📧 Email:", p["Corresponding Author Email"])

    # Save to CSV
    df = pd.DataFrame(papers)
    df.to_csv(args.filename, index=False, encoding="utf-8")

    print(f"\n✅ Results saved to '{args.filename}'\n")
