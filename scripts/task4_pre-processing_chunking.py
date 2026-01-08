import os, re, csv, argparse, json
import pandas as pd

INPUT_ROOT_DEFAULT = "raw-data/Fintech-data-main"
OUTPUT_DIR_DEFAULT = "output"

ROLE_MAP = {
    "finance": "Finance",
    "marketing": "Marketing",
    "hr": "HR",
    "engineering": "Engineering",
    "c-level": "C-Level",
    "general": "Employees",
    "employees": "Employees",
}
DEFAULT_ROLE = "Employees"

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def read_markdown(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    text = clean_text(raw)
    m = re.search(r"(?:^|\n)#{1,6}\s*(.+?)(?:\n|$)", raw)
    title = m.group(1).strip() if m else os.path.basename(path)
    return text, title

def read_csv_doc(path: str):
    df = pd.read_csv(path, encoding="utf-8", dtype=str).fillna("")
    header = " | ".join(df.columns)
    rows = [" | ".join(map(str, row)) for row in df.values]
    return clean_text("\n".join([header] + rows)), os.path.basename(path)

def infer_role(dirpath: str) -> str:
    for part in dirpath.split(os.sep):
        if part.lower() in ROLE_MAP:
            return ROLE_MAP[part.lower()]
    return DEFAULT_ROLE

def chunk_words(words, min_size=300, max_size=512, overlap=64):
    chunks, start = [], 0
    step = max(max_size - overlap, 1)
    n = len(words)
    while start < n:
        end = min(start + max_size, n)
        chunk = words[start:end]
        if len(chunk) < min_size and end < n:
            end = min(start + min_size, n)
            chunk = words[start:end]
        chunks.append(chunk)
        if end >= n:
            break
        start += step
    return chunks

def pad3(i: int) -> str:
    return str(i).zfill(3)

def run_chunking(input_root: str, output_dir: str, sample: bool=False):
    os.makedirs(output_dir, exist_ok=True)
    chunks_csv = os.path.join(output_dir, "chunks.csv")
    sample_json = os.path.join(output_dir, "sample_chunks.json")

    all_rows = []
    with open(chunks_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "chunk_id","doc_id","filename","title","role",
                "chunk_index","chunk_count","text"
            ],
        )
        writer.writeheader()

        for dirpath, _, files in os.walk(input_root):
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                if ext not in [".md", ".markdown", ".csv"]:
                    continue

                path = os.path.join(dirpath, fname)
                role = infer_role(dirpath)

                if ext in [".md", ".markdown"]:
                    text, title = read_markdown(path)
                else:
                    text, title = read_csv_doc(path)

                words = re.findall(r"\S+", text)
                chunks = chunk_words(words, 300, 512, 64)

                stem = os.path.splitext(fname)[0]
                doc_id = os.path.relpath(path, input_root).replace("\\", "/")

                for i, chunk in enumerate(chunks, start=1):
                    row = {
                        "chunk_id": f"{stem}_{pad3(i)}",
                        "doc_id": doc_id,
                        "filename": fname,
                        "title": title,
                        "role": role,
                        "chunk_index": i,
                        "chunk_count": len(chunks),
                        "text": " ".join(chunk),
                    }
                    writer.writerow(row)
                    all_rows.append(row)

                if sample:
                    print(f"\nFile: {fname} → {len(chunks)} chunks")
                    for i, chunk in enumerate(chunks[:3], start=1):
                        preview = " ".join(chunk[:50])
                        print(f"--- Sample {pad3(i)} ({len(chunk)} tokens) ---\n{preview}...\n")

    print(f"Chunks written to {chunks_csv}")

    samples = []
    if all_rows:
        filenames_ordered = []
        seen = set()
        for row in all_rows:
            fn = row["filename"]
            if fn not in seen:
                seen.add(fn)
                filenames_ordered.append(fn)

        for fname in filenames_ordered[:2]:  # first 2 files
            doc_rows = [r for r in all_rows if r["filename"] == fname][:3]  # first 3 chunks
            for row in doc_rows:
                samples.append({
                    "chunk_id": row["chunk_id"],
                    "filename": row["filename"],
                    "title": row["title"],
                    "role": row["role"],
                    "chunk_size_tokens": len(row["text"].split()),
                    "text": row["text"]  # full chunk text here
                })

    with open(sample_json, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2, ensure_ascii=False)
    print(f"Sample chunks JSON written to {sample_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=INPUT_ROOT_DEFAULT, help="Input documents root folder")
    parser.add_argument("--out", default=OUTPUT_DIR_DEFAULT, help="Output folder")
    parser.add_argument("--sample", action="store_true", help="Print sample chunks to console")
    args = parser.parse_args()
    run_chunking(args.root, args.out, sample=args.sample)