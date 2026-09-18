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

## 2026-09-17

### What changed
- Attached **joefazio.dev** to the Pages project under Workers & Pages → joefazio-portfolio → Custom domains, apex only. Cloudflare created a proxied, flattened CNAME from the apex to `joefazio-portfolio.pages.dev` and issued a certificate from Google Trust Services.
- Verified from outside the dashboard while it still said "Initializing": `1.1.1.1` resolved the apex to Cloudflare addresses, the certificate named `joefazio.dev`, and the site returned 200 with the Astro 7 markup.
- Added the `www` redirect: a proxied A record for `www` at `192.0.2.1`, plus Cloudflare's **"Redirect from WWW to root"** template as a Single Redirect rule (wildcard `https://www.*`, 301, keeps path and query string).
- Turned on **Always Use HTTPS** (SSL/TLS → Edge Certificates).
- Changed `site` in `astro.config.mjs` to `https://joefazio.dev` (`795c6a5`) and added four glossary terms (`9dc299b`). Pushed both; GitHub Actions passed and Cloudflare Pages deployed `9dc299b`.
- Ran `npm run dev` for the first time on Astro 7: the dev server started (v7.3.2) and served the page with a 200.

### Why
- The redirect template over a hand-written rule: it does the same thing as the rule I planned, with less to type wrong. The dangerous mistake here is swapping source and target, which would send the apex to a `www` that has no site.
- Always Use HTTPS over widening the redirect rule: the rule only matched `https://www.*`, so a plain `http://www` request fell through to the placeholder origin. One zone-wide switch fixes that for every hostname, instead of patching one rule.
- `site` changed now, even though nothing uses it yet, so canonical links and a future sitemap point at the real domain from the start.

### What broke
- **`http://www` returned 522** ("Cloudflare could not reach the origin") before Always Use HTTPS was on. The request did not match the `https://` rule, so Cloudflare passed it through to `192.0.2.1`, which deliberately answers nothing. Browsers never hit this, because `.dev` is HSTS-preloaded and upgrades to HTTPS before sending anything, but `curl` and scripts did. Now `http://www` → `https://www` → `https://joefazio.dev`, two 301s ending in 200.
- **Google's resolver and this PC still said "no record"** for the apex for a while after Cloudflare's own resolver had it. They had looked the name up before the record existed and were remembering that empty answer (negative caching). Tested around it by pointing `curl` straight at Cloudflare's address with `--resolve`.
- Not broken, but noticed: a path that does not exist (e.g. `/x`) returns 200 with the homepage rather than a 404. Cloudflare Pages does this when a site has no `404` page.

### What is next
1. Open the build log for deployment `9dc299b` (Deployments → Details) and confirm Cloudflare Pages built with Node 24. Do the same in a GitHub Actions run log. Still unconfirmed.
2. Confirm `https://joefazio.dev` loads in a normal browser once the cached "no record" answer expires.
3. Open VS Code on the `portfolio` folder rather than `portfolio\node_modules`. The terminal has been starting inside `node_modules`; npm still finds the project by walking up, but other tools may not.
4. Decide whether GitHub Actions should become a real deploy gate.
5. Real site content: homepage, about, ACC Timebank case study, resume, contact, `/now`, plus a `404` page.
6. Later: update the LinkedIn and resume links to `joefazio.dev`.

## 2026-09-18

### What changed
- Confirmed the apex now resolves everywhere. `8.8.8.8` returns Cloudflare addresses for `joefazio.dev` and the site returns 200. The negative cache from the last session expired on its own, as expected.
- **Made GitHub Actions a real deploy gate, via branch protection.** Created a repository ruleset named `main protection` targeting the default branch, with an empty bypass list, and four rules: restrict deletions, block force pushes, require a pull request before merging (required approvals `0`), and require the `build` status check to pass.
- Tested it in both directions rather than trusting the settings page. A direct push to `main` was refused by the server with `GH013: Repository rule violations found for refs/heads/main`, naming both the pull-request rule and the missing `build` check. A pull request from `test-gate` ran `build`, went green, and merged cleanly (`d5b3bd2`).
- This was the repo's first ever `pull_request` workflow run; every prior run had been a `push` on `main`.
- Left the Cloudflare Pages Git integration deploying from `main` unchanged.

### Why
- **Branch protection (option B) now, moving deploys into Actions (option C) later.** B took one sitting, needs no secrets, and is free on a public repo. C — disconnecting the Pages Git integration and deploying from Actions with Wrangler and a scoped API token — is the stronger story but introduces an API token to scope, store and rotate, and it drops the automatic preview deployments unless those get rebuilt too. B is not throwaway work: branch protection still applies on top of C whenever C happens.
- **Required approvals set to `0`.** GitHub does not let anyone approve their own pull request, so any non-zero value would make every PR on a solo repo permanently unmergeable. Zero still forces the PR to exist; it just does not demand a second person.
- **Empty bypass list**, so the rules apply to the repo owner too. A gate with a personal exemption does not prove much, and the ruleset can be set to `Disabled` from its own settings page if it ever genuinely blocks something.
- **"Require branches to be up to date before merging" left off.** It earns its keep when two people touch the same file; with one committer it is pure friction.
- The required check is spelled `build`, lowercase — the **job** id in `build.yml`, not the workflow's `name: Build`. GitHub reports status checks by job name.

### A correction to the record
CLAUDE.md has said "a broken build breaks the deploy." That is not quite how Cloudflare Pages behaves: a failed build is marked failed and **the last successful deployment stays live**, so the site does not go down. The actual risks were that `main` could hold a commit that does not build, discoverable only by reading logs in two places, and that anything which builds but is wrong went straight to production unreviewed. Branch protection addresses both.

### What broke
- **Nothing broke.** One false alarm worth recording, because it will recur.
- The PR sat on `build — Expected — Waiting for status to be reported` with no visible run. That message is ambiguous: it reads identically whether the job is merely queued waiting for a runner (normal, clears in a minute or two) or the required check name matches no real job (never clears). Checking the Actions tab distinguishes them — a run that exists means waiting, no run at all means a wrong name. This one was queued, and it passed at 16:22 without intervention. The GitHub REST API also served a stale listing during that window, showing zero `pull_request` runs after one had already been created, which made it briefly look like the trigger was not firing.
- The rejected push left its commit sitting on local `main`, one ahead of `origin/main`. Cleared with `git reset --hard origin/main`.
- `git branch -d test-gate` deleted only the local branch; the branch on GitHub survived it and needed deleting separately.

### The gap that remains
Cloudflare Pages reported `Deployed successfully` on the test commit **before the Actions build had even started**. Pages watches the repo directly and waits for nobody. So the accurate description of this setup is: branch protection controls what is allowed to enter `main`, and therefore what reaches production — it does not make Pages wait for a check. Preview deployments on feature branches stay ungated, which is fine; they are throwaway URLs. Closing the gap properly is option C.

### What is next
1. Open the Cloudflare Pages build log (Deployments → Details) and a GitHub Actions run log, and confirm both build with Node 24. Carried over two sessions now; both need a login.
2. Open VS Code on the `portfolio` folder rather than `portfolio\node_modules`. Still opening in the wrong place.
3. A `404` page (`src/pages/404.astro`). Nonexistent paths currently return 200 with the homepage.
4. Real site content: homepage, about, ACC Timebank case study, resume, contact, `/now`.
5. Option C, as its own session: deploy from Actions with Wrangler and a scoped API token, and disconnect the Pages Git integration so the two do not both deploy.
6. Later: update the LinkedIn and resume links to `joefazio.dev`.

### Design direction: navy, and a site with interests in it

Two changes to the look, decided after seeing the first styled pass:

- **Navy as the anchor colour**, with brass (`--accent`) as the warm note and a
  muted sea green (`--accent-2`) as the quieter second voice for links. Light
  mode is the same palette on paper rather than a different scheme. Checked
  every pair against the WCAG contrast formula rather than eyeballing it:
  everything clears AA, most clears AAA.
- **Sans-serif instead of monospace.** The monospace read as generic-developer,
  which is the wrong signal for a wide IT net. Now a system sans stack, which
  lands on Segoe UI on Windows, Helvetica/Arial elsewhere. The two other
  terminal-ish touches went with it: the `~/` wordmark prefix became a small
  brass square, and the `*` marking the active nav item became an underline.

**The larger intent, recorded now and built later.** This should not read as a
resume in HTML. The plan is to put actual interests on it and let them carry the
personality. Unfiltered ideas so far:

- **Vinyl record collection** — some view of what is on the shelf.
- **Song of the day**, pulled from a Spotify playlist that stays vetted, so the
  site shows something current without being a live feed of everything played.

Neither is built. **Content comes first**: about, the ACC Timebank case study,
`/now`. These are a deliberate second pass, once there is something to decorate.

Worth noting for when that pass happens: song-of-the-day is a genuinely good fit
for the Cloudflare Workers + KV track already in the stack plan, and not a
frontend problem. Spotify's API needs a client ID and secret exchanged for a
token that expires, so the credentials cannot sit in the page — that is exactly
what a Worker is for, with KV caching the day's pick so the site is not calling
Spotify on every visit. Free tiers cover it.

### About page trimmed, projects page added, music gets its own home

Feedback on the first About draft: the "How I work" and "Skills, honestly"
sections both read as strained, and the interests did not belong on that page at
all. Cut all three. About is now the opening, the wide-net paragraph, and "What
I'm building" — shorter, and it stops trying to sell.

**Music and vinyl move to their own tab** rather than living as a paragraph on
About. The idea worth keeping, unbuilt for now: the menu or a page that behaves
like a crate of records — you flip through sleeves rather than read a list. That
is a real interaction to design, not a styling tweak, so it waits until the
content pages are done. It is also the first thing on this site that would need
meaningful client-side JavaScript, which is a deliberate departure from Astro's
ship-almost-no-JS default and should be a conscious choice when it happens.

**Projects page** built from what was already on the resume: ACC Timebank, the
BRHS cybersecurity risk assessment, the Capsim simulation, and this site. Each
entry says plainly what it was, including that three of the four were coursework
and that the fictional healthcare org in the BRHS report was invented for the
assignment. Claiming coursework as client work is the easiest way to lose an
interview; labelling it costs nothing.
