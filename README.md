# Requirements
- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/)

> [!warning]
> As Netlify doesn't support Python past 3.8, the template **can't** be used with Netlify. 
> Only GitHub Page is officially supported.

# Installation
1. Click on "use this template"
2. Create the new repository from the template
3. [Generate a new GH token with the `repo` and workflow scope](https://github.com/settings/tokens/new?scopes=repo,workflow)
4. In Settings > Secrets and variables > actions 
 - Click on "New repository secret"
 - Name: `GH_TOKEN`
 - Value: `<your token>`
5. While in Settings, go to "Pages" and select "Deploy from a branch" and select `gh-pages` branch (from root)
> [!Warning] You can publish a private repository as a public page in the free tier of GitHub. But you can use a private submodule as your docs folder and publish it as a public page.

# Template generation 

1. In Actions, go "Generate Website" and click on "Run workflow".
2. Fill the items and click on "Run workflow"
3. Wait for the workflow to finish
4. Read and validate the pull request, merge it.
5. You can now go into "Publish" and click on "Run workflow" to publish the website.