import os, argparse
import pandas as pd

OUTPUT_DIR_DEFAULT = "output"

ROLES = ["Finance","Marketing","HR","Engineering","C-Level","Employees"]

def accessible_roles(role: str):
    if role == "Employees":
        return ["Employees","C-Level"]
    if role in ROLES:
        return [role,"C-Level"]
    return ["C-Level"]

def build_metadata(chunks_csv: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(chunks_csv, dtype=str).fillna("")

    # Compute accessible roles directly from the 'role' column
    df["accessible_roles"] = df["role"].apply(lambda r: ",".join(accessible_roles(r)))

    
    meta = df[["chunk_id","doc_id","filename","title","role","accessible_roles"]]
    meta = meta.sort_values(by=["role","doc_id","chunk_id"])

    out_path = os.path.join(out_dir, "metadata.csv")
    meta.to_csv(out_path, index=False)
    print(f"Metadata written to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunks", default=os.path.join(OUTPUT_DIR_DEFAULT, "chunks.csv"))
    parser.add_argument("--out", default=OUTPUT_DIR_DEFAULT)
    args = parser.parse_args()
    build_metadata(args.chunks, args.out)