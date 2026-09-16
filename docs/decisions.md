# Decision log

## 2026-09-15

### Stack choices
- **Astro** — static site generator. It turns source files into plain HTML at build time, ships almost no JavaScript, and is easy to restyle repeatedly without fighting a framework.
- **Cloudflare Pages** for hosting, over Vercel or Netlify. All three host a static site for free, but Cloudflare also exposes real DNS, CDN cache rules, a WAF, and access policies on the same account. Those are the infrastructure pieces I want hands-on practice with for IT roles.
- **Cloudflare DNS** — the domain's records will live on the same account as the hosting.
- **GitHub, public repo** — version history, and the repo itself is part of the portfolio.
- **GitHub Actions** — automated build checks that live next to the code, free for public repos.
- **Terraform** — deferred until the site is live and stable. It is easier to learn infrastructure as code after doing the same configuration by hand and knowing what it replaces.
- **Cloudflare Workers + KV** — planned for small backend features (guestbook, visitor counter), within the free tier.

### What changed
- Started the project as a minimal Astro site: one page, no styling, so the deployment path is the first milestone.
- Initialized Git locally and pushed to GitHub (`joefazio1/joefazio-portfolio`) so the project had version history and a remote copy before deployment.
- Added a GitHub Actions workflow (`.github/workflows/build.yml`) that runs `npm run build` on every push and pull request to `main`.
- Connected the GitHub repo to Cloudflare Pages. The site is live at https://joefazio-portfolio.pages.dev.
- First milestone is half done: the site is publicly deployed, but not yet on a custom domain.

### How deployment actually works
Every push to `main` starts two independent processes at the same time:

1. **GitHub Actions** builds the site as a check, then throws the output away. It does not deploy anything.
2. **Cloudflare Pages** pulls the same commit, builds it on Cloudflare's servers, and publishes the `dist/` folder.

Neither waits for the other, so the Actions workflow is **not** a gate on deployment. A broken build would still not go live, but only because Cloudflare's own build would also fail. The Actions check is most useful on pull requests, where it flags a broken build before merging.

Cloudflare Pages build settings. These live in the Cloudflare dashboard, not in this repo, so they are recorded here:
- Production branch: `main`
- Build command: `npm run build`
- Build output directory: `dist`
- Deploy command: none (Pages publishes the output folder on its own)

### Why
- The project's first priority is learning the deployment pipeline well enough to explain it in an interview.
- A working live site is a stronger foundation than polishing design before the infrastructure is proven.

### What broke
- The Cloudflare dashboard's setup flow defaulted to creating a Worker instead of a Pages project. That path asked for Worker-style configuration (including a deploy command), and those deploy attempts failed. The fix was to use the Pages flow with the build command `npm run build` and no deploy command.
- The project URL returned 404s until the deployment settings matched a static Astro site through the Pages flow.

### What is next
- Buy a custom domain and connect it through Cloudflare DNS. This finishes the first milestone and is the only planned cost (~$15/yr). Then update `site` in `astro.config.mjs` to the new domain.
- Decide whether GitHub Actions should become a real deploy gate: either require the check to pass before anything merges to `main` (branch protection), or deploy from Actions and turn off Cloudflare's automatic deploys.
- Build the real content: homepage, about, ACC Timebank case study, resume, contact, `/now`.
- Keep this log and the glossary updated as new concepts come up.

## 2026-09-15 (session 2: project review)

### What changed
- Reviewed the repo. Only 9 files had ever been committed, there were no secrets in the history, generated folders (`node_modules/`, `dist/`, `.astro/`) were correctly ignored, the build passed, and the site was live.
- Took `CLAUDE.md` (private working notes) out of the public repo. I stopped tracking it, added it to `.gitignore`, rewrote both existing commits with `git filter-branch` to remove it, and force-pushed with `--force-with-lease`. The commit IDs changed, but the messages, author, dates, and every other file stayed the same. Cloudflare Pages and GitHub Actions both passed on the rewritten commit.
- Set `site` in `astro.config.mjs` to `https://joefazio-portfolio.pages.dev`. It was still the `example.com` placeholder.
- Updated the GitHub Actions workflow:
  - Node 20 → Node 24, read from a new `.node-version` file that both Actions and Cloudflare Pages use
  - `npm install` → `npm ci`
  - added `permissions: contents: read`
  - `actions/checkout` and `actions/setup-node` v4 → v7, after checking the release notes for breaking changes (none affect this workflow)
- Added private notes, local secret files (`.env*`, `.dev.vars*`, `.wrangler/`), Terraform state and variable files, and `Thumbs.db` to `.gitignore`.
- Corrected the session 1 entry: the Actions workflow is not a deploy gate, the Cloudflare build settings are now recorded, and the custom domain is part of the milestone. Expanded the glossary.
- Set the PowerShell execution policy for my Windows user to `RemoteSigned` so `npm` runs in a normal PowerShell window. Confirmed the build works in a fresh window.
- Committed and pushed the review fixes as `4423110`. GitHub Actions and Cloudflare Pages both passed, and the site still loads.
- Deleted the old GitHub Actions run that linked to the pre-rewrite commit.
- Set up a backup for `CLAUDE.md`: a copy in OneDrive, refreshed as the last step of every wrap-up.

### Why
- The repo is public, and `CLAUDE.md` is working notes that aren't meant to be read raw.
- Node 20 stopped receiving security fixes in April 2026. One version file keeps my PC, GitHub Actions, and Cloudflare Pages on the same Node version.
- `npm ci` installs exactly what the lockfile says, so every CI build uses identical packages.
- Read-only permissions follow least privilege: the workflow never needs to write to the repo.
- Secret and Terraform state files are ignored before they exist, so they can't be committed by accident later.
- `RemoteSigned` instead of typing `npm.cmd` every time: it's the common developer setting, it applies only to my Windows user, and scripts downloaded from the internet still need a signature.
- The history rewrite ran in a separate copy of the repo, after making a full backup, so the uncommitted work in my project folder was never at risk. `--force-with-lease` meant the push would refuse if GitHub had changed unexpectedly.
- Commit first, push second, as separate steps: committing is a zero-risk snapshot on my PC, while pushing triggers a deploy, so I did it when I could watch the builds.
- The `CLAUDE.md` backup is a plain copy refreshed at wrap-up rather than a symbolic link. I rarely edit that file by hand, and a plain copy has nothing that can break.

### What broke
- Running `npm ci` while the Astro dev server was running failed partway. Windows won't delete a file a running program has open, so `node_modules/` was left half-deleted. I fixed it by stopping the dev server and running `npm ci` again. Lesson: stop the dev server before reinstalling packages on Windows.
- `npm run build` in a fresh PowerShell window fails with "running scripts is disabled on this system." PowerShell's execution policy blocks `npm.ps1`. Fixed by running `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, which lets my own local scripts run while downloaded scripts still need a signature. `npm.cmd` also works regardless of the policy.
- `npm run build` from my home folder failed with `ENOENT ... package.json`. npm commands have to be run from the project folder, where `package.json` lives.
- The history rewrite removed `CLAUDE.md` from `main`, but GitHub still serves the old commits to anyone with their exact commit ID. I checked, and both the old commit and the file inside it still load.
- `npm audit` reports 3 known vulnerabilities (critical in Astro, high in sharp, low in esbuild). The fix requires a major upgrade from Astro 5 to 7. The esbuild issue lets someone read files through the dev server on Windows, which matters when the dev server is reachable from the network (`--host 0.0.0.0`).

### What is next
1. Commit and push this wrap-up's doc updates (`decisions.md`, `glossary.md`).
2. Open the build logs for `4423110` in GitHub Actions and Cloudflare Pages and confirm both used Node 24. The builds passed, but the version is only visible in the logs, which need a login.
3. Decide whether to fully purge the old commits from GitHub: ask GitHub Support to remove them, or delete and recreate the repo and reconnect Cloudflare Pages.
4. Upgrade Astro from 5 to 7 as its own step. Until then, run the dev server without `--host 0.0.0.0`.
5. Custom domain through Cloudflare DNS (finishes the first milestone).
6. Decide whether GitHub Actions should become a real deploy gate.
7. Real site content: homepage, about, ACC Timebank case study, resume, contact, `/now`.
