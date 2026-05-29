from __future__ import annotations
from reportlab.pdfgen.canvas import Canvas


def draw_label(canvas: Canvas, text: str, x: float, y: float, font_name: str, font_size: float) -> None:
    canvas.setFont(font_name, font_size)
    canvas.drawString(x, y, text)


def draw_centered_label(canvas: Canvas, text: str, x_center: float, y: float, font_name: str, font_size: float) -> None:
    canvas.setFont(font_name, font_size)
    canvas.drawCentredString(x_center, y, text)


def draw_right_label(canvas: Canvas, text: str, x_right: float, y: float, font_name: str, font_size: float) -> None:
    canvas.setFont(font_name, font_size)
    canvas.drawRightString(x_right, y, text)
