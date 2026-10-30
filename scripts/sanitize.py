"""转义来自第三方仓库的文本，使其在 Markdown 与 HTML 中都是纯文本。

索引里大量字段直接摘自上游 README 与 GitHub API 描述，其中可能带有
`<`、`>`、`&`。这些内容最终会经 marked 渲染成 HTML，若不转义，
一个上游仓库的 README 就能往本站注入任意标记。

在数据源头统一转义，文档生成与站点装配共用同一套规则。
"""

URL_KEYS = {"url", "html_url", "homepage", "paper_id", "source_url", "requested_url"}


def sanitize_text(value):
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sanitize_url(value):
    # URL 里的 & 是真实分隔符，不能转义成实体
    return value.replace("<", "&lt;").replace(">", "&gt;")


def sanitize(value, key=None):
    if isinstance(value, str):
        return sanitize_url(value) if key in URL_KEYS else sanitize_text(value)
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, dict):
        return {k: sanitize(v, k) for k, v in value.items()}
    return value
