from __future__ import annotations
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas

class IconLoader:
    def __init__(self, icons_dir: str | Path = "assets/icons") -> None:
        self.icons_dir = Path(icons_dir)
    def draw_icon(self, canvas: Canvas, filename: str, x: float, y: float, size: float = 24.0, allow_missing: bool = True) -> None:
        path = self.icons_dir / filename
        if path.exists():
            canvas.drawImage(str(path), x, y, width=size, height=size, preserveAspectRatio=True, mask="auto")
            return
        if not allow_missing:
            raise FileNotFoundError(path)
        canvas.saveState()
        canvas.setStrokeColorRGB(0.65, 0.70, 0.76)
        canvas.rect(x, y, size, size, fill=0, stroke=1)
        canvas.line(x, y, x + size, y + size)
        canvas.line(x + size, y, x, y + size)
        canvas.restoreState()
