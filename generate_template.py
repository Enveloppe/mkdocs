import argparse
from pathlib import Path
from string import Template
from typing import Literal

import requests
from pydantic import BaseModel


class TemplateModel(BaseModel):
    site_name: str
    site_url: str
    site_description: str
    site_author: str
    language: str
    auto_h1: bool
    comments: bool
    generate_graph: bool = False


class Environment(BaseModel):
    env: str
    deploy: str


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a template for Obsidian Publisher"
    )
    parser.add_argument("site_name", type=str, help="The name of the site")
    parser.add_argument("site_url", type=str, help="The url of the site")
    parser.add_argument(
        "site_description", type=str, help="The description of the site"
    )
    parser.add_argument("site_author", type=str, help="The author of the site")
    parser.add_argument("language", type=str, help="The language of the site")
    parser.add_argument(
        "--auto-h1", action="store_true", help="Automatically add h1 to the title"
    )
    parser.add_argument(
        "--comments", action="store_true", help="Enable comments on the site"
    )

    args = parser.parse_args()

    template = TemplateModel(
        template_type=args.template,
        site_name=args.site_name,
        site_url=args.site_url,
        site_description=args.site_description,
        site_author=args.site_author,
        language=args.language,
        auto_h1=args.auto_h1,
        comments=args.comments,
        generate_graph=True if args.template == "gh_pages" else False,
    )
    # download the files
    
    mkdocs_yaml = Path("mkdocs.yml")
    with mkdocs_yaml.open("r", encoding="UTF-8") as f:
        mkdocs = f.read()
    mkdocs = Template(mkdocs)
    s = mkdocs.substitute(
        site_name=template.site_name,
        site_url=template.site_url,
        site_description=template.site_description,
        site_author=template.site_author,
        language=template.language,
        auto_h1=template.auto_h1,
        comments=template.comments,
        generate_graph=template.generate_graph,
    )
    
    
    with mkdocs_yaml.open("w", encoding="UTF-8") as f:
        f.write(s)

    print("Mkdocs template generated:")
    print(s)
    print("Done!")


if __name__ == "__main__":
    main()