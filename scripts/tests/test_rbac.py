from scripts.rbac.rbac_filter import filter_chunks_by_rbac


def test_rbac():
    search_results = [
        {
            "chunk_text": "HR leave policy details",
            "department": "HR",
            "allowed_roles": ["Department Staff", "C-Level"]
        },
        {
            "chunk_text": "Finance salary data",
            "department": "Finance",
            "allowed_roles": ["C-Level"]
        }
    ]

    user_role = "Department Staff"
    user_department = "HR"

    filtered = filter_chunks_by_rbac(
        search_results,
        user_role,
        user_department
    )

    print("Authorized results:")
    for item in filtered:
        print(item["chunk_text"])


if __name__ == "__main__":
    test_rbac()

