# GitHub profile setup

## 1. Create the profile repository

Create a public GitHub repository whose name exactly matches your GitHub username. GitHub renders that repository's `README.md` on your profile.

Copy these items into the repository root:

```text
README.md
assets/
.github/workflows/snake.yml
```

`scripts/build_banner.py`, `assets/banner-source.png`, and `assets/banner-prompt.txt` are optional source files. Keep them if you want the banner to remain reproducible.

## 2. Replace the four personal placeholders

Replace every occurrence of:

| Placeholder | Replace with |
|---|---|
| `YOUR_GITHUB_USERNAME` | Your exact GitHub username |
| `YOUR_LINKEDIN_URL` | Your full LinkedIn profile URL |
| `YOUR_PORTFOLIO_URL` | Your portfolio URL |
| `YOUR_EMAIL` | Your professional email address |

PowerShell example:

```powershell
$readme = Get-Content -Raw README.md
$readme = $readme.Replace("YOUR_GITHUB_USERNAME", "your-username")
$readme = $readme.Replace("YOUR_LINKEDIN_URL", "https://www.linkedin.com/in/your-profile/")
$readme = $readme.Replace("YOUR_PORTFOLIO_URL", "https://your-portfolio.example")
$readme = $readme.Replace("YOUR_EMAIL", "you@example.com")
Set-Content -Path README.md -Value $readme
```

## 3. Verify project destinations

The six project buttons use clean, predictable repository slugs and GitHub Pages URLs. Keep those slugs when creating the project repositories, or update the corresponding links in `README.md`.

For each live demo button, enable GitHub Pages in the project repository under **Settings → Pages**, or replace the URL with the deployed application URL.

## 4. Enable the contribution snake

1. Push the profile repository to GitHub with `main` as the default branch.
2. Open **Actions** and enable workflows if GitHub asks.
3. Run **Generate contribution snake** manually once.
4. Confirm that an `output` branch was created.
5. The workflow then refreshes the snake every day at 00:20 UTC and on pushes to `main`.

The workflow grants write access only to repository contents and uses GitHub's built-in token.

## 5. Enable WakaTime

The WakaTime card assumes your public WakaTime username matches your GitHub username. If it does not, replace the username only in the WakaTime image URL. The card stays empty until the WakaTime profile is public and has coding activity.

## 6. Banner note

No portrait file was included with the original brief, so the delivered banner intentionally avoids generating or impersonating a face. It uses a text-safe left panel and a data-engineering scene on the right.

To add an authentic portrait later, use your own high-resolution photo, preserve facial features, and composite it into the right side with cool blue and subtle violet rim lighting. Keep the left text panel unchanged.

To rebuild the current banner on Windows:

```powershell
python .\scripts\build_banner.py
```

Pillow is required:

```powershell
python -m pip install Pillow
```

## 7. Final checks before publishing

- Confirm every project repository exists.
- Confirm each live demo opens successfully.
- Add repository descriptions, topics, screenshots, and concise case-study READMEs.
- Pin the strongest four to six repositories on your GitHub profile.
- Keep achievements and certification claims verifiable.
- Review the profile on desktop and mobile after pushing.
