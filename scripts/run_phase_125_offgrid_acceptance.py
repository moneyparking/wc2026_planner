from __future__ import annotations

from pathlib import Path
import inspect
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import app


def main() -> None:
    assert getattr(app, "OFFGRID_ENGINE_MARKER", "") == "PHASE_1_25_OFFGRID_LOCAL_ENGINE"
    assert "requests" not in inspect.getsource(app.check_modal_gpu_health).lower()
    assert "requests" not in inspect.getsource(app.fetch_ai_scout_slip).lower()

    badge = app.check_modal_gpu_health()
    assert "AUTONOMOUS LOCAL ENGINE ACTIVE" in badge

    slip = app.fetch_ai_scout_slip("Team A", "Team B", "Group", "A")
    assert "Tactical" in slip or "Match analysis" in slip or "Scout note" in slip

    print("PHASE_125_OFFGRID_ACCEPTANCE_PASS")


if __name__ == "__main__":
    main()
