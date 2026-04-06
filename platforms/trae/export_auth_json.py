"""
Trae.ai 账号认证文件导出
生成可导入 Trae 的 storage.json 片段或独立认证 JSON
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Any

logger = logging.getLogger(__name__)


def generate_auth_json(account: Any) -> dict:
    """
    生成 Trae 认证 JSON。

    字段来源：
      - token      -> account.token 或 extra["token"]
      - userId     -> account.user_id 或 extra["user_id"]
      - email      -> account.email
      - region     -> account.region 或 extra["region"]
      - cashierUrl -> extra["cashier_url"]
      - aiPayHost  -> extra["ai_pay_host"]
    """
    extra: dict = getattr(account, "extra", {}) or {}

    token = str(account.token if hasattr(account, "token") and account.token else extra.get("token", "")).strip()
    user_id = str(
        (getattr(account, "user_id", "") or extra.get("user_id") or extra.get("userId") or "")
    ).strip()
    email = str(getattr(account, "email", "") or extra.get("email", "")).strip()
    region = str(
        (getattr(account, "region", "") or extra.get("region") or "")
    ).strip() or "cn"
    cashier_url = str(extra.get("cashier_url") or extra.get("cashierUrl") or "").strip()
    ai_pay_host = str(extra.get("ai_pay_host") or extra.get("aiPayHost") or "").strip()

    now = datetime.now(tz=timezone(timedelta(hours=8)))
    exported_at = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

    return {
        "type": "trae",
        "email": email,
        "token": token,
        "userId": user_id,
        "region": region,
        "cashierUrl": cashier_url,
        "aiPayHost": ai_pay_host,
        "exportedAt": exported_at,
    }


def generate_storage_json_patch(account: Any) -> dict:
    """
    生成可直接合并到 Trae storage.json 的 key-value 片段。
    用于批量导出或调试查看实际写入内容。
    """
    extra: dict = getattr(account, "extra", {}) or {}
    token = str(account.token if hasattr(account, "token") and account.token else extra.get("token", "")).strip()
    user_id = str(
        (getattr(account, "user_id", "") or extra.get("user_id") or extra.get("userId") or "")
    ).strip()
    email = str(getattr(account, "email", "") or extra.get("email", "")).strip()
    region = str(
        (getattr(account, "region", "") or extra.get("region") or "")
    ).strip() or "cn"

    patch: dict = {"trae.token": token}
    if user_id:
        patch["trae.userId"] = user_id
    if email:
        patch["trae.email"] = email
    if region:
        patch["trae.region"] = region
    return patch
