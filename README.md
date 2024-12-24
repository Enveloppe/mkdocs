# Requirements
- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/)

# Installation
1. Click on "use this template"
2. Create the new repository from the template
3. [Generate a new GH token with the `repo` and workflow scope](https://github.com/settings/tokens/new?scopes=repo,workflow)
4. In Settings > Secrets and variables > actions 
 - Click on "New repository secret"
 - Name: `GH_TOKEN`
 - Value: `<your token>`
5. In "Actions" tab, click on "generate website" and fill the information needed