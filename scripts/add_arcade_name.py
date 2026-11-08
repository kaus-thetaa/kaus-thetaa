
from pathlib import Path
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

FILES = [
    Path("dist/readme-arcade.svg"),
    Path("dist/readme-arcade-dark.svg"),
]

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

    strip = next(
        (child for child in list(root) if child.get("id") == "profile-name-strip"),
        None,
    )
    if strip is not None:
        root.remove(strip)
        height -= STRIP_HEIGHT
        root.set("viewBox", f"{min_x:g} {min_y:g} {width:g} {height:g}")
        root.set("height", f"{height:g}px")

    tree.write(path, encoding="utf-8", xml_declaration=True)
    print(f"Removed profile title strip from {path}")


if __name__ == "__main__":
    for file in FILES:
        add_name(file)
