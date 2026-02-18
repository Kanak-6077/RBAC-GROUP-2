from scripts.rbac.role_config import ROLE_HIERARCHY


def is_role_allowed(user_role: str, allowed_roles: list) -> bool:
    user_level = ROLE_HIERARCHY.get(user_role, 0)

    for role in allowed_roles:
        if ROLE_HIERARCHY.get(role, 0) <= user_level:
            return True

    return False


def filter_chunks_by_rbac(search_results: list, user_role: str, user_department: str):
    authorized_results = []

    for chunk in search_results:
        chunk_department = chunk.get("department")

        # Department check - C-Level and admin can access all departments
        if chunk_department != user_department and user_role not in ["C-Level", "admin"]:
            continue

        authorized_results.append(chunk)

    return authorized_results
