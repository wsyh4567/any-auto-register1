"""导出 Kiro 认证 JSON 文件（与 Kiro IDE 本地 token 文件格式兼容）"""

from core.base_platform import Account


def generate_auth_json(account: Account) -> dict:
    """
    生成与 Kiro IDE 本地 token 文件兼容的认证 JSON。

    字段映射：
        clientId      ← extra.clientId
        clientSecret  ← extra.clientSecret
        accessToken   ← extra.accessToken 或 account.token
        refreshToken  ← extra.refreshToken
        authMethod    ← extra.authMethod（默认 "IdC"）
        idcRegion     ← extra.region（默认 "us-east-1"）
        expiresAt     ← extra.expiresAt（可为空）
    """
    extra = account.extra or {}

    return {
        "clientId": extra.get("clientId", ""),
        "clientSecret": extra.get("clientSecret", ""),
        "accessToken": extra.get("accessToken", "") or account.token or "",
        "refreshToken": extra.get("refreshToken", ""),
        "authMethod": extra.get("authMethod", "IdC"),
        "idcRegion": extra.get("region", "us-east-1"),
        "expiresAt": extra.get("expiresAt", ""),
    }
