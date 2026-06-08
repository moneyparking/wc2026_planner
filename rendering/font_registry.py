from __future__ import annotations
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class FontRegistry:
    FALLBACK_DISPLAY = "Helvetica-Bold"
    FALLBACK_BODY = "Helvetica"
    FALLBACK_MONO = "Courier"
    def __init__(self, fonts_dir: str | Path = "assets/fonts") -> None:
        self.fonts_dir = Path(fonts_dir)
    def register_all(self) -> dict[str, str]:
        mapping = {"display": self.FALLBACK_DISPLAY, "body": self.FALLBACK_BODY, "body_bold": self.FALLBACK_DISPLAY, "mono": self.FALLBACK_MONO}
        specs = (("BebasNeue", "BebasNeue-Regular.ttf", "display"), ("Inter", "Inter-Regular.ttf", "body"), ("InterBold", "Inter-Bold.ttf", "body_bold"), ("IBMPlexMono", "IBMPlexMono-Regular.ttf", "mono"))
        for name, filename, key in specs:
            path = self.fonts_dir / filename
            if path.exists():
                pdfmetrics.registerFont(TTFont(name, str(path)))
                mapping[key] = name
        return mapping
