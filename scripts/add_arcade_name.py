
from pathlib import Path
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

FILES = [
    Path("dist/readme-arcade.svg"),
    Path("dist/readme-arcade-dark.svg"),
]

NAME = "KAUSTUBH CHATURVEDI"
STRIP_HEIGHT = 46


def add_name(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Arcade artwork not found: {path}")

    tree = ET.parse(path)
    root = tree.getroot()

    viewbox = root.get("viewBox")
    if not viewbox:
        raise ValueError(f"Missing SVG viewBox in {path}")

    min_x, min_y, width, height = map(
        float, viewbox.replace(",", " ").split()
    )

    # Remove an existing strip so reruns never duplicate the name.
    for child in list(root):
        if child.get("id") == "profile-name-strip":
            root.remove(child)

    dark = path.name.endswith("-dark.svg")

    background = "#0D1117" if dark else "#FFFFFF"
    foreground = "#F4F4F4" if dark else "#24292F"
    accent = "#FC3D21"

    new_height = height + STRIP_HEIGHT

    root.set(
        "viewBox",
        f"{min_x:g} {min_y:g} {width:g} {new_height:g}"
    )
    root.set("height", f"{new_height:g}px")

    group = ET.SubElement(
        root,
        f"{{{SVG_NS}}}g",
        {"id": "profile-name-strip"}
    )

    ET.SubElement(
        group,
        f"{{{SVG_NS}}}rect",
        {
            "x": str(min_x),
            "y": str(min_y + height),
            "width": str(width),
            "height": str(STRIP_HEIGHT),
            "fill": background,
        },
    )

    ET.SubElement(
        group,
        f"{{{SVG_NS}}}line",
        {
            "x1": str(min_x + width * 0.30),
            "x2": str(min_x + width * 0.70),
            "y1": str(min_y + height + 2),
            "y2": str(min_y + height + 2),
            "stroke": accent,
            "stroke-width": "2",
        },
    )

    label = ET.SubElement(
        group,
        f"{{{SVG_NS}}}text",
        {
            "x": str(min_x + width / 2),
            "y": str(min_y + height + 31),
            "text-anchor": "middle",
            "dominant-baseline": "middle",
            "font-family": "monospace",
            "font-size": "20",
            "font-weight": "700",
            "letter-spacing": "2",
            "fill": foreground,
        },
    )
    label.text = NAME

    tree.write(path, encoding="utf-8", xml_declaration=True)
    print(f"Added {NAME} to {path}")


if __name__ == "__main__":
    for file in FILES:
        add_name(file)
