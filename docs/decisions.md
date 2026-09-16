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

## 2026-09-16

### What changed
- Pushed the previous session's doc updates (`6f1081c`).
- Upgraded Astro from 5.18.2 to 7.3.2 in a single step (`7153150`). Read the v6 and v7 upgrade guides first and checked every breaking change against this repo. None applied: no integrations, no content collections, no adapters, no environment variables, and no `src/fetch.ts`, which v7 now reserves for routing. Node 24 already meets v7's minimum of 22.12.0, so `.node-version` and the workflow needed no change.
- `npm audit` went from 3 known vulnerabilities (critical in Astro, high in sharp, low in esbuild) to 0.
- Approved esbuild's install script, which npm recorded as a new `allowScripts` field in `package.json` (`ed12d5f`).
- Verified with a clean `npm ci`, the same command CI runs, followed by a build, an audit, and a check for unreviewed install scripts. All clean.
- Confirmed the deploy from the outside: the live site returns 200 and serves the Astro 7 markup.
- Added the packaging and build terms from this session to the glossary (`8645575`).

### Why
- Upgrading while the site is still one unstyled page: this is the smallest the upgrade will ever be, and the real content then gets built on the version I intend to stay on.
- Straight from 5 to 7 rather than stopping at 6, because the upgrade guides are cumulative and I checked both against the actual files in this repo.
- Plain `npm install astro@^7` rather than `npx @astrojs/upgrade`, because that helper mainly exists to keep integration packages in version lockstep, and this project has no integrations. The plain install changed exactly one dependency.
- Approving the install script rather than leaving it blocked: npm now holds install scripts until they are reviewed, and recording the approval means `npm ci` runs it in Actions and Cloudflare Pages instead of warning on every build.
- The only difference in the built HTML comes from v7's new `compressHTML: 'jsx'` default, which strips whitespace between block-level tags. Browsers ignore that whitespace, so the rendered page is identical. It would matter for two inline elements side by side, which this page does not have.

### The old commits: accepted, not purged
The two pre-rewrite commits (`605869bee5e65a27062e4e46fd8d36b28b7c98ba` and `7a5b215ad87fe945e628f5d8e8f530e4f1263852`) still return 200 on GitHub, and `CLAUDE.md` is still readable raw at both. I looked at the options and chose to accept this rather than spend the time removing it:

- Removing it properly requires a GitHub Support ticket. Only Support can run garbage collection server-side and clear cached views. Deleting and recreating the repo would also remove the objects, but it is not a documented remedy and it costs the Cloudflare Pages reconnection.
- What is exposed is working notes, not credentials. There is nothing to rotate and nothing an attacker can use.
- Nothing is holding the old objects alive: 0 forks, `network_count` of 0, 0 pull requests in any state, and all 5 workflow runs point at current commits.
- The repo is two days old with 0 stars and 0 watchers, so the chance anyone fetched those exact SHAs is very low.

If that stops being true, the Support route stays open and the ticket is small: 0 affected pull requests and the 2 commit IDs above.

### Custom domain: bought, not yet connected
Registered **joefazio.dev** through Cloudflare Registrar: about $12/yr plus ICANN's $0.18, at cost with no markup, free WHOIS redaction, and auto-renew left on. Registered 2026-09-16, expires 2027-09-16.

Choices made along the way:

- **`.dev` over the alternatives.** `joefazio.com` was already taken, as were `josephfazio.com` and `fazio.dev`. `.dev` reads as technical without claiming a specialty, which suits casting a wide net. It is also on the browsers' HSTS preload list, so every `.dev` domain is refused over plain HTTP and forced to HTTPS automatically.
- **Registering at Cloudflare rather than elsewhere.** Buying from the same company that hosts the site means the domain arrives already on Cloudflare's nameservers with the zone created. Buying at Namecheap or GoDaddy would have added a manual nameserver change and a propagation wait.
- **Apex canonical, `www` redirects to it.** `joefazio.dev` is the real address and `www.joefazio.dev` will 301 to it. Serving both directly would split the search ranking between two identical sites, and an apex is shorter to say out loud or print on a resume.
- **`pages.dev` left working.** It stays useful as a fallback for telling apart "the domain is misconfigured" from "the site is broken." Setting `site` in `astro.config.mjs` will point canonical links at the real domain anyway.
- **Single Redirect over Bulk Redirects** for the `www` rule. Cloudflare's own Pages guide suggests Bulk Redirects, but those are account-level and built for long lists across many domains; this is one rule on one zone. Both are free on the Free plan (10 single rules, 15 bulk rules), so this is a simplicity choice, not a cost one.

Verified from outside the dashboard rather than trusting it: RDAP reports the domain `active` and delegated to `darwin.ns.cloudflare.com` and `reza.ns.cloudflare.com`, and Google's resolver at `8.8.8.8` returns those same nameservers. The apex has no address record yet, which is correct — Pages has not created one.

### What broke
- The Astro upgrade broke nothing. No code changes, no config changes, no build errors.
- The custom domain stalled on navigation, not on anything technical. The **Custom domains** tab lives *inside* the Pages project (Workers & Pages → joefazio-portfolio → Custom domains), not under the top-level **Domains** section in the sidebar, which is where the newly bought domain also appears. Two different places, similar names.

### What is next
1. Attach the domain to Pages: **Workers & Pages → joefazio-portfolio → Custom domains → Set up a domain**, enter `joefazio.dev` with no `www` and no `https://`. Cloudflare creates the record itself, using CNAME flattening because the DNS standard forbids a plain CNAME at a bare domain. Add only the apex — adding `www` here would serve the site at both addresses instead of redirecting.
2. Wait for the custom domain to show **Active** and the TLS certificate to issue, usually a few minutes. Then verify from outside: the apex resolves, the certificate matches the domain, and the site returns 200 with the Astro 7 markup.
3. Set up the `www` redirect: a **proxied** A record for `www` pointing at `192.0.2.1` (a reserved address that deliberately routes nowhere, giving Cloudflare something proxied to attach a rule to), plus a Single Redirect rule under **Rules → Overview** sending `www.joefazio.dev` to `https://joefazio.dev` with a 301, preserving path and query string.
4. Update `site` in `astro.config.mjs` to `https://joefazio.dev`, then push it together with the glossary commit currently held locally.
5. Run `npm run dev` once to confirm the Astro 7 dev server starts and the page loads. The build and the dev server are different code paths, and only the build has been tested.
6. Still pending from the last session: open the GitHub Actions and Cloudflare Pages build logs and confirm both used Node 24. The logs need a login.
7. Decide whether GitHub Actions should become a real deploy gate.
8. Real site content: homepage, about, ACC Timebank case study, resume, contact, `/now`.
