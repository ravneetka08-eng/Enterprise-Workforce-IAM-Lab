# Publish the project to GitHub

## Create a new repository

1. Extract this package. Open iam-lab in VS Code and open its PowerShell terminal.
2. Create an empty repository on GitHub with your chosen name. Do not initialize it with another README if using these local files.
3. Run the commands below from iam-lab. The first commit describes prepared material, not completed tests.

```powershell
git init
git branch -M main
git status
git add README.md START-HERE.md .gitignore requirements.txt app automation data templates docs evidence
git diff --cached
```

4. Review the staged files. Inspect staged images too. The private folder, databases, backups, tokens and raw exports must be absent. The manual DOCX is optional to publish; the Markdown version is already under docs.
5. Commit and replace YOUR-USERNAME and REPOSITORY-NAME in the URL with your actual values:

```powershell
git commit -m "Add IAM lab code and prepared documentation"
git remote add origin https://github.com/YOUR-USERNAME/REPOSITORY-NAME.git
git push -u origin main
```

Use GitHub's supported sign-in flow for Git; do not put access tokens into the remote URL or a public file.

## Update after each lab

Save sanitized evidence and update actual result/status fields. Then run git status, stage only intended files, review git diff --cached, commit with a meaningful change description and push.

## Existing repository

Do not replace unrelated files, remove .git, re-add an existing origin or force push. Keep an existing checkout; copy only the intended project files, inspect git status and compare conflicts before committing. An unexpected rejected push requires examining remote changes, not overriding history.

## Credentials accidentally published

Revoke/rotate the credential immediately. Follow the hosting provider's documented history-removal process. Deleting the visible file does not remove older commits.
