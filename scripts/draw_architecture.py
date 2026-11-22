"""Render the two README figures as standalone SVGs (Python standard library)."""
from pathlib import Path
from xml.etree import ElementTree as ET

OUT = Path(__file__).resolve().parents[1] / "docs" / "figures"
INK, MUTED, WIRE = "#182d3c", "#495f6c", "#5a6f7b"
PAPER, TEAL, GOLD = "#f0f4f6", "#ddf2ed", "#faebd2"


class Plate:
    def __init__(self, number, title, note, height):
        self.svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width="900",
                              height=str(height), viewBox=f"0 0 900 {height}", role="img",
                              **{"aria-labelledby": "title", "font-family": "DejaVu Sans, sans-serif"})
        ET.SubElement(self.svg, "title", id="title").text = title
        marker = ET.SubElement(ET.SubElement(self.svg, "defs"), "marker", id="tip",
                               viewBox="0 0 8 8", refX="8", refY="4", orient="auto",
                               markerWidth="5", markerHeight="5")
        ET.SubElement(marker, "path", d="M0 0L8 4L0 8Z", fill=WIRE)
        self.add("rect", x=0, y=0, width=900, height=height, rx=12, fill="#fcfdfc")
        self.add("rect", x=22, y=16, width=34, height=27, rx=5, fill=INK)
        self.text(39, 35, number, 14, "#ffffff", bold=True)
        self.text(69, 36, title, 21, anchor="start", bold=True)
        self.text(878, 34, note, 13, MUTED, anchor="end")
        self.add("path", d="M22 55H878", stroke="#cfdbde")

    def add(self, tag, **attrs):
        return ET.SubElement(self.svg, tag, {k.replace('_', '-'): str(v) for k, v in attrs.items()})

    def text(self, x, y, value, size=15, color=INK, anchor="middle", bold=False):
        self.add("text", x=x, y=y, fill=color, font_size=size, text_anchor=anchor,
                 font_weight=700 if bold else 400).text = value

    def box(self, x, cy, w, title, detail, fill=PAPER):
        self.add("rect", x=x, y=cy-25, width=w, height=50, rx=8, fill=fill, stroke="#becdd0")
        self.text(x+w/2, cy-2, title, bold=True)
        self.text(x+w/2, cy+16, detail, 13, MUTED)

    def arrow(self, path, dashed=False):
        self.add("path", d=path, fill="none", stroke=WIRE, stroke_width=1.7,
                 stroke_linejoin="round", marker_end="url(#tip)",
                 **({"stroke_dasharray": "5 4"} if dashed else {}))

    def dot(self, x, y):
        self.add("circle", cx=x, cy=y, r=3, fill=WIRE)

    def plus(self, x, y):
        self.add("circle", cx=x, cy=y, r=13, fill="#fff", stroke=WIRE)
        self.text(x, y+6, "+", 19)

    def save(self, name):
        ET.indent(self.svg)
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_bytes(ET.tostring(self.svg, encoding="utf-8") + b"\n")


def overview():
    p = Plate("01", "SMoVSR · два прохода по клипу", "ПРОСТРАНСТВО  /  ВРЕМЯ", 263)
    p.box(22, 100, 100, "Клип", "T · RGB")
    p.box(151, 100, 142, "Признаки", "SMB × 2")
    p.box(335, 100, 157, "Прямой", "FSMoSR · 1 → T", TEAL)
    p.box(335, 181, 157, "Слияние", "concat → 1×1")
    p.box(539, 181, 182, "Обратный", "FSMoSR · T → 1", GOLD)
    p.box(539, 100, 182, "Реконструкция", "concat → SR-голова")
    p.arrow("M122 100H151")
    p.arrow("M293 100H335")
    p.arrow("M222 125V181H335")
    p.arrow("M414 125V156")
    p.arrow("M492 181H539")
    p.arrow("M492 100H539")
    p.arrow("M630 156V125")
    p.arrow("M721 100H780")
    p.plus(793, 100)
    p.arrow("M806 100H832")
    p.text(856, 105, "HR", bold=True)
    p.arrow("M72 125V237H793V113", dashed=True)
    p.text(415, 231, "Билинейная база · ×s", 13, MUTED)
    p.save("smovsr.svg")


def cell():
    p = Plate("02", "FSMoSR · один шаг с историей", "ЯЧЕЙКА  /  ОБА НАПРАВЛЕНИЯ", 243)
    p.text(35, 122, "x", bold=True)
    p.text(37, 204, "h", bold=True)
    p.box(72, 198, 143, "Выравнивание", "поканально", GOLD)
    p.plus(250, 117)
    p.box(292, 117, 118, "Признаки", "SMB × 3", TEAL)
    p.plus(508, 117)
    p.box(552, 117, 168, "Выход шага", "SMB → Conv 3×3")
    p.box(425, 198, 295, "a + z ⊙ (f − a)", "z = sigmoid(Conv 1×1(cat(x, a)))", GOLD)
    p.arrow("M48 117H237")
    p.arrow("M115 117V78H508V104")
    p.dot(115, 117)
    p.arrow("M48 198H72")
    p.arrow("M215 198H425")
    p.arrow("M250 198V130")
    p.dot(250, 198)
    p.text(266, 187, "a", bold=True)
    p.arrow("M263 117H292")
    p.arrow("M410 117H495")
    p.arrow("M450 117V173")
    p.dot(450, 117)
    p.text(462, 107, "f", bold=True)
    p.arrow("M521 117H552")
    p.arrow("M720 117H753")
    p.text(765, 122, "в SR-голову", anchor="start")
    p.arrow("M720 198H753")
    p.text(765, 203, "новая память", anchor="start")
    p.save("fsmosr.svg")


if __name__ == "__main__":
    overview()
    cell()
