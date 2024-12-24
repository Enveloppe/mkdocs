import argparse
from pathlib import Path
from string import Template

from pydantic import BaseModel


class TemplateModel(BaseModel):
    site_name: str
    site_url: str
    site_description: str
    site_author: str
    language: str
    auto_h1: bool
    comments: bool
    submodule: bool = False



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
    parser.add_argument(
        "--submodule", action="store_true", help="Enable submodule for the site, default is False")

    args = parser.parse_args()

    template = TemplateModel(
        site_name=args.site_name,
        site_url=args.site_url,
        site_description=args.site_description,
        site_author=args.site_author,
        language=args.language,
        auto_h1=args.auto_h1,
        comments=args.comments,
        submodule=args.submodule if args.submodule else False
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
    )
    with mkdocs_yaml.open("w", encoding="UTF-8") as f:
        f.write(s)
    print("Mkdocs template generated:")
    print(s)
    print("Done!")

    if template.submodule:
        workflow_path = Path(".github/workflows/deploy.yml")
        with workflow_path.open("r", encoding="UTF-8") as f:
            workflow = f.read()
        wf=workflow.replace("FETCH_SUBMODULE: false", "FETCH_SUBMODULE: true")
        with workflow_path.open("w", encoding="UTF-8") as f:
            f.write(wf)
        print("Workflow template generated:")
        print(wf)
        print("Done!")

if __name__ == "__main__":
    main()