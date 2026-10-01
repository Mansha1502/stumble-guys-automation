import json
from pathlib import Path

from utils.config import SESSION_STORAGE_PATH, SITE_ORIGIN


def save_session_storage(page):
    data = page.evaluate("() => Object.assign({}, window.sessionStorage)")
    Path(SESSION_STORAGE_PATH).parent.mkdir(exist_ok=True)
    Path(SESSION_STORAGE_PATH).write_text(json.dumps(data))
    return list(data.keys())


def restore_session_storage(context):
    path = Path(SESSION_STORAGE_PATH)
    if not path.exists():
        return

    data = json.loads(path.read_text())
    script = (
        "(() => {"
        f"  if (window.location.origin !== {json.dumps(SITE_ORIGIN)}) return;"
        f"  const data = {json.dumps(data)};"
        "  for (const [key, value] of Object.entries(data)) {"
        "    sessionStorage.setItem(key, value);"
        "  }"
        "})();"
    )
    context.add_init_script(script)