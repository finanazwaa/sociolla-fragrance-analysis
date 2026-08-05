import pandas as pd
import re
from bs4 import BeautifulSoup

# Load the products data (assumes this script is run from the project root)
DF_PATH = "data/products.csv"
df = pd.read_csv(DF_PATH)


def clean_html(text: str) -> str:
    """Strip HTML tags from a string, returning a plain‑text representation.
    Empty/NaN values are converted to an empty string.
    """
    if pd.isna(text):
        return ""
    soup = BeautifulSoup(text, "html.parser")
    # Use a space as separator to keep words separated
    return soup.get_text(separator=" ")


def extract_notes(description: str) -> list[dict[str, str]]:
    """Extract perfume notes from a description.

    The function looks for sections such as "Top", "Middle", "Base" (or their synonyms)
    followed by a colon or dash and a comma‑separated list of notes.
    It returns a list of dictionaries ``{"note_name": ..., "note_type": ...}``.
    """
    text = clean_html(description)
    # Regex pattern using verbose flag for readability
    pattern = r"""
        (TOP|MIDDLE|MID|HEART|BASE|BOTTOM|DRY[\s-]?DOWN)   # note category
        \s*[:\-]\s*                                      # separator
        (.*?)                                            # note list (non‑greedy)
        (?=                                              # look‑ahead for next category or end
            \bTOP\b|\bMIDDLE\b|\bMID\b|\bHEART\b|\bBASE\b|\bBOTTOM\b|\bDRY[\s-]?DOWN\b|$)
    """
    matches = re.findall(pattern, text, flags=re.I | re.X)

    extracted = []
    for note_type, notes in matches:
        note_type = note_type.lower()
        # Normalise the category name
        if note_type in {"mid", "middle", "heart"}:
            note_type = "middle"
        elif note_type in {"base", "bottom", "dry-down"}:
            note_type = "base"
        elif note_type == "top":
            note_type = "top"
        # Split the notes by comma and clean whitespace
        for note in notes.split(","):
            note = note.strip()
            if note:
                extracted.append({"note_name": note, "note_type": note_type})
    return extracted

# ---------------------------------------------------------------------------
# Build the product‑note mapping
# ---------------------------------------------------------------------------
all_product_notes = []
for _, row in df.iterrows():
    notes = extract_notes(row.get("description", ""))
    for note in notes:
        all_product_notes.append({
            "product_id": row["product_id"],
            "note_name": note["note_name"],
            "note_type": note["note_type"],
        })

productnotes_df = pd.DataFrame(all_product_notes)

# ---------------------------------------------------------------------------
# Build a distinct notes table with a generated numeric ID
# ---------------------------------------------------------------------------
notes_df = (
    productnotes_df[["note_name", "note_type"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
notes_df.insert(0, "note_id", range(1, len(notes_df) + 1))

# Merge the IDs back into the product‑note table
productnotes_df = productnotes_df.merge(notes_df, on=["note_name", "note_type"], how="left")
productnotes_df = productnotes_df[["product_id", "note_id", "note_type"]]

# ---------------------------------------------------------------------------
# Persist results
# ---------------------------------------------------------------------------
notes_df.to_csv("NOTES.csv", index=False)
productnotes_df.to_csv("PRODUCTNOTES.csv", index=False)

# Simple sanity check output
success = productnotes_df["product_id"].nunique()
print(f"{success}/{len(df)} products have extracted notes")
