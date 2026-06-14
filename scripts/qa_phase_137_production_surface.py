from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
APP_PATH = REPO_ROOT / "app.py"
README_PATH = REPO_ROOT / "README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _public_blocks_prefix(app_text: str) -> str:
    blocks = app_text.split("with gr.Blocks(", 1)[1]
    return blocks.split('with gr.Tabs(elem_classes=["pmw-tabs"]):', 1)[0]


def _short_description(readme: str) -> str:
    for line in readme.splitlines():
        if line.startswith("short_description:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    raise AssertionError("README missing short_description")


def main() -> None:
    app = _read(APP_PATH)
    readme = _read(README_PATH)
    public_prefix = _public_blocks_prefix(app)

    assert "SF_PREMIUM_WAR_ROOM_CSS" in app
    assert 'gr.HTML("<style>"' not in app
    assert "gr.HTML(value=_appstore_first_screen_html())" not in public_prefix
    assert "gr.HTML(value=_premium_cta_strip_html())" not in public_prefix
    assert "Runtime Data Mode" in readme
    assert "LIVE_SCORE_PROVIDER" in app
    assert "LIVE_SCORE_PROVIDER" in readme
    assert 'with gr.Tab("💎 Premium"' in app
    assert 'with gr.Tab("🏟️ Match Center"' in app
    assert "Load Demo Scenario" in app
    assert 'href="#"' not in app
    assert len(_short_description(readme)) <= 60

    lower = (app + "\n" + readme).lower()
    if "real-time" in lower:
        assert "real-time requires hf space secrets" in lower
        assert "without provider secrets" in lower

    print("PHASE_1_37_PRODUCTION_SURFACE_QA_PASS")


if __name__ == "__main__":
    main()
