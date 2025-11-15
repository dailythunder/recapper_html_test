import json
import sys
import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape


def main(input_json: str, output_html: str = "site/index.html") -> None:
    base_dir = pathlib.Path(__file__).parent
    input_path = base_dir / input_json
    output_path = base_dir / output_html

    if not input_path.exists():
        raise SystemExit(f"Input JSON not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    env = Environment(
        loader=FileSystemLoader(str(base_dir / "templates")),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("report.html.jinja")
    html = template.render(data=data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Wrote HTML report to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python render_html.py <input_json> [output_html]")
    input_json = sys.argv[1]
    output_html = sys.argv[2] if len(sys.argv) > 2 else "site/index.html"
    main(input_json, output_html)
