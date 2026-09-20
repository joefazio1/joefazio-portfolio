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

### Resume published as-is, with the phone number on it

The resume PDF carries a header line with home city, email, phone, and LinkedIn.
CLAUDE.md's constraint said no phone number on the site, so this was raised
before publishing: a PDF at a public URL is public display, and scrapers harvest
phone numbers out of public PDFs as a matter of course.

Decided to **publish it as-is**. The convenience to a recruiter who wants the
document in one click outweighed the spam risk. That supersedes the earlier
no-phone-on-the-site rule, which was written before there was a resume link to
argue about; the CLAUDE.md constraint should be updated to match rather than
left contradicting the site.

Mechanics: the file is copied into `public/` as `resume.pdf`, which Astro passes
through to the site root, so it is served at `https://joefazio.dev/resume.pdf`.
The stable filename is the point — updating the resume means replacing that one
file, and every link that was ever shared keeps working. Archived dated copies
stay out of the repo.

One consequence to be aware of, given this repo is public: once a commit
containing `resume.pdf` is pushed, that exact file stays retrievable from GitHub
history even if a later commit removes or replaces it. The same property already
came up with CLAUDE.md in the 2026-09-16 entry. If the resume ever needs to
change for privacy reasons rather than for content, removing it from the current
commit is not enough on its own.

### Session wrap-up, 2026-09-18

**Where the site ended the day.** Live and merged: the navy palette, the
sans-serif type, the shared layout, the 404 page, and the branch protection
ruleset. Built but **not merged**: pull request #6, holding the about page, the
projects page, the resume, and `.gitattributes`. It was opened but the merge
never went through, so `/about`, `/projects`, and `/resume.pdf` still return 404
on the live site. The branch `add-about-page` is pushed and intact, so nothing
is lost. Merging #6 is the first task next session.

**Writing rules set at the end of the day**, to apply to everything on the site
from here:

1. **No em dashes anywhere on the site, for any reason.** Use commas, colons,
   parentheses, or two sentences instead. The current copy violates this in
   seven places: three in about, three in projects, one in the layout. All are
   on the unmerged branch, so the fix goes in right after #6 merges.
2. **The projects page reads too snarky.** Lines like "Coursework still counts,
   as long as I say so" and the aside about Capsim were written for personality
   and land as a young adult being clever. Rewrite in a professional register.
   The honesty about what was coursework stays, stated plainly rather than
   wryly.
3. **Explain each project quickly and concisely**, then stop. The current ACC
   entry runs six paragraphs before it reaches what was built. Short first pass,
   then fill in detail from what gets supplied per project.
4. **Give each project context and callbacks to the resume.** The resume lists
   employers and coursework the projects grew out of, and the projects page
   currently reads as though it exists in isolation from that history.

**Keeping the resume current.** The site serves `public/resume.pdf` at
`https://joefazio.dev/resume.pdf`. That URL is fixed and never needs to change.
The source file lives at
`C:\Users\jdfaz\OneDrive\Documents\Job Application Documents\Resume_Joe_Fazio.pdf`.
Updating the site resume means copying that file over `public/resume.pdf` and
committing it. Nothing about the link, the filename on the site, or anything
already shared changes. Keeping the OneDrive filename stable is what makes this
a one-command update rather than a hunt each time.

### What is next
1. **Merge pull request #6.** Everything below assumes it is in.
2. Strip the em dashes from all site copy.
3. Rewrite the projects page in a professional register: concise entries, resume
   context, no snark. Supply detail per project to fill it out.
4. Confirm `https://joefazio.dev/resume.pdf` downloads once #6 is live.
5. Delete the six stale branches on GitHub left over from merged pull requests.
6. Still carried over: confirm Node 24 in the Cloudflare Pages and GitHub Actions
   build logs. Both need a login.
7. Still carried over: open VS Code on the `portfolio` folder rather than
   `portfolio\node_modules`.
8. The ACC Timebank deep case study, and the `/now` page.
9. The music and vinyl tab, including the record crate interaction idea.
10. Later: option C, deploying from Actions with Wrangler; Terraform for the
    Cloudflare configuration; updating the LinkedIn and resume links to
    joefazio.dev.

## 2026-09-18 (second session)

### What shipped

Six pull requests merged, #6 through #11. The site went from three pages to
nine.

**Merged the backlog (#6).** The about page, the projects page, `resume.pdf`
and `.gitattributes` had been sitting unmerged on `add-about-page` since the
last session, so `/about`, `/projects` and `/resume.pdf` were all returning 404
on the live site. Merging it was the first task. Verified afterwards by
downloading the live PDF and byte-comparing it against `public/resume.pdf`:
identical.

**Stripped every em dash (#7).** Seven of them, across the layout, the about
page and the projects page. A grep for both em and en dashes across `src/` now
returns nothing, and that check gets run before every commit.

**Rewrote the projects page in a professional register (#7).** Cut the dry
asides ("Coursework still counts, as long as I say so", the Capsim quip). The
ACC entry dropped from six paragraphs of setup to one, plus the build list and
the two decisions that actually shaped it. Added resume callbacks throughout,
grounded in the real resume rather than guessed: the intro links `/resume.pdf`
and the ACC entry names the line it corresponds to.

**Added `/now` (#8).** Studying for Security+, PowerShell automation as the next
project, and the remaining infrastructure work here. Carries a visible "last
updated" date, because a stale `/now` page is worse than none.

**Built the ACC Timebank case study (#9).** Its own page at
`/projects/acc-timebank` rather than a tab, so it has a URL that can be sent to
someone on its own. Covers the constraints, why AppSheet was abandoned, why a
Google Sheet was the right database for this client, the five-state request
lifecycle, and the guardian authorisation path for youth members. Three code
excerpts, highlighted with Astro's built-in Shiki, no plugin and no cost.

**Added the client handover section and corrected the framework claim (#10).**
See the two subsections below.

**Rebuilt the home page and added the personal side (#11).** See below.

### Why a separate case study page instead of tabs

Tabs were the original request. Separate pages won for three reasons: Ctrl+F
stops finding text that is hidden behind a tab, search engines index less of it,
and you cannot send a recruiter a link to one specific tab. Tabs still earn
their place inside a single project page, splitting Overview from Code, and that
option stays open.

### Reading the source documents

Joe's coursework lives in Word, PowerPoint and PDF files that Claude Code cannot
read directly. Set up a drop folder at `C:\Users\jdfaz\dev\source-material\`
holding `read_docs.py`, which unzips the XML out of Office files with nothing but
the Python standard library and writes a `.txt` twin beside each one. `pypdf`
handles the PDFs. Joe drops files in and says so; the conversion happens on his
behalf.

**That folder deliberately sits outside the repo.** It holds client notes,
stakeholder interviews and personal data, and anything committed to a public
repo stays retrievable from history forever. The same property that trapped
CLAUDE.md in the 2026-09-16 entry.

### Three findings from the ACC source code

Joe supplied the full Apps Script backend and front end, which changed the case
study from description into evidence.

**Passwords are stored in plaintext.** There is a SHA-256 function in the code,
but registration writes the raw password to the sheet and login accepts either
value, so the plaintext comparison is the one that matches. Worse, the admin CSV
export passes a flag that deliberately keeps the password column, so credentials
leave the system in a downloadable file. The decision was to name this openly in
a "What I would do differently" section rather than stay quiet, because a case
study that identifies a flaw in its author's own work is stronger evidence of
review skill than one that does not, and it supports the Security+ and junior
security direction.

**No excerpt may carry the real identifiers.** The spreadsheet ID, the password
salt and the deployment URL are redacted from everything published. Verified by
grepping the built `dist/` output, not just the source, for each token
individually.

**There is no real usage data.** `ACC Timebank Data.pdf` contains two test
members, one request and one transaction. The system was built, tested and
handed over but never populated with real ACC members, so the case study claims
no membership or volume figures. That PDF also contains a working admin password
in plain text, which is the flaw above demonstrating itself sixteen months
later. Joe confirmed the password is not reused anywhere.

### The handover document is the strongest artifact

The ACC deliverable included a written runbook for administrators who had never
opened Apps Script: standing the system up from an empty Google account, the
exact tab and column schema the code reads by name, deployment, a pre-launch
test script, routine administration, and a troubleshooting list anticipating the
failures a volunteer would hit. It now has its own section, because writing
documentation a non-technical person can follow is closer to the help desk and
systems administration work being applied for than the code is.

### Corrected an overstated framework claim

The site and the resume both said the BRHS assessment used NIST CSF and CIS
Controls v8. The assignment rubric required choosing one, and the report's
Framework Selection section explicitly picks NIST CSF and argues for it. Asked
about the difference, Joe said he could not remember one from the other or why
one was chosen. Since skills on this site have to be defensible in conversation,
the site now says NIST CSF only.

The glossary picked up NIST CSF, CIS Controls v8 and how to choose between them.
The short version: NIST CSF describes outcomes across Identify, Protect, Detect,
Respond and Recover, and suits assessing and explaining current posture; CIS
Controls v8 is a prioritised list of 18 safeguards and suits sequencing the
remediation. The report's own reasoning, now available as an interview answer,
was that BRHS had to keep its existing EHR and minimise disruption, and its
weaknesses were in policy, monitoring, access management and incident
preparedness rather than missing technology.

**The resume still claims both.** Updating it is Joe's call and was left undone.

### Added the ethical hacking lab course

A fifth project. Leads with the isolated lab Joe built, a Kali Linux machine and
a Windows victim on a private host-only adapter with no route to the outside,
then covers the breadth: defence in depth, keylogger detection, social
engineering, PGP, hash functions, and a Nessus scan whose deliverable was a
triaged, prioritised set of fixes rather than raw findings. Written at portfolio
altitude, defensively framed, no step-by-step technique.

### Capsim: kept broad on purpose

The round reports show team Digby finishing last in the industry on nearly every
measure, with sales collapsing from above the industry average in round one to
roughly a third of it by round four while the fixed cost base stayed put. That is
a genuinely strong diagnosis, and telling it straight was recommended.

**Joe chose to keep the entry broad and lesson-focused instead**, matching the
resume, and to note that his own role was R&D. That decision stands. The numbers
are not published. The lesson stated on the page, that a strategy is only worth
the follow-through behind it each round, is true and is the honest core of it.

### What broke, and the design reversal

**The terminal hero was built and thrown away.** The first home page led with a
console window running `whoami`, `cat now.txt` and `git push`. Joe called it
cringe and it was removed the same session. The direction correction is the
important part and is worth keeping: the site should read as a well-rounded
person with character who happens to love computers, not as a computer nerd. No
terminal, matrix or hacker aesthetics on the personal-facing pages.

**The stale branch count was wrong twice.** Reported as four, then five, then
six, because branches kept becoming stale mid-conversation as pull requests
merged. Fixed properly by turning on the repository's "Automatically delete head
branches" setting, which has worked on every merge since.

**A shell heredoc failed twice** while writing large files with mixed quoting,
including this log. The lesson: large multi-line content with nested quotes and
apostrophes should be written with the editor tool, not piped through a bash
heredoc.

### The personal side: The Record Store

The site now has a second function alongside the portfolio. `/records`, "The
Record Store", is a crate of album sleeves standing upright, each jacket naming
its subject, with a record peeking out of the top that slides the rest of the
way out when clicked before redirecting to the list. Two sleeves are live, Top
25 Movies and Top 25 Games, both read off screenshots Joe supplied. Two are
dimmed and marked coming soon, Top 25 Albums and My Record Collection.

The slide is progressive enhancement. The sleeves are ordinary links underneath,
so with JavaScript off, reduced motion on, or a modified click to open a new
tab, they navigate normally. The animation is never a dependency.

The lists are set typographically with no cover art, which keeps the pages light
and avoids poster licensing questions entirely. Each entry has a slot for a
one-line note, rendered only when filled, so the pages look finished now and
become Joe's writing space later.

**The home page went back to a placeholder** because Joe is considering making
the about page the landing page instead. The nav settled at five boxed tabs:
Home, About, Projects, Now, The Record Store. Movies and Games left the nav and
live inside the store.

### What is next
1. Delete the stale `home-page` branch on GitHub, left over from the abandoned
   terminal hero. It was never merged and never will be.
2. Merge the pull request holding this session log.
3. Decide whether the about page replaces the home page as the landing page.
4. Give the portfolio pages the same UI care the record store got. Joe was
   explicit that the portfolio is still the site's main function.
5. Fill in the one-line notes on the movies and games lists, which is the start
   of the "writeups gushing about things I like" idea.
6. Build `/albums` from a top 25 albums list, and `My Record Collection` as a
   data file Joe edits whenever he buys a record. Then flip both sleeves live.
7. Decide between inline notes and a real blog at `/writing`. The recommendation
   was to fill in notes first and build the blog when there is a first real post,
   rather than standing up an empty shell.
8. Update the resume: drop CIS Controls v8 from the BRHS bullet, or move it to
   the skills list where "familiar with" is fair.
9. Wire up the parked Letterboxd, Steam and Spotify links once Joe supplies the
   profile URLs.
10. Still carried over: confirm Node 24 in the Cloudflare Pages build log. The
    repo has a `.node-version` file containing `24` and the workflow reads it
    via `node-version-file`, so Actions provably uses 24 and Pages reads the
    same file. That is config-level evidence, not a log.
11. Still carried over: open VS Code on the `portfolio` folder rather than
    `portfolio\node_modules`.
12. Later: deploying from Actions with Wrangler; Terraform for the Cloudflare
    configuration; updating the LinkedIn and resume links to joefazio.dev.

## 2026-09-20

### Two home pages built, one kept

The session opened on the question of what the landing page should be, and the
answer took two attempts.

**A manila folder was built and rejected.** The idea was a personnel file: a
tabbed folder reading "Fazio, Joe" with the contents visible on the paper
inside. It built and worked, and Joe did not like it. That is now two home-page
concepts rejected, after the terminal hero of 2026-09-18. The lesson taken from
it: Joe reacts to built pages rather than to descriptions, so for anything
subjective the cheapest path is to build a throwaway comparison and let him
pick, rather than to argue for one option in prose.

**The bulletin board replaced it and stayed.** A cork panel with a speckle
texture, holding pinned paper: an index card with the name and the one-line
pitch, two polaroid photographs, and four link cards for Projects, About,
Resume and The Record Store. Each item sits at a slight tilt and straightens and
lifts on hover.

The interaction is pure CSS, works on keyboard focus as well as mouse hover, and
switches itself off under `prefers-reduced-motion`. Every pinned item is an
ordinary link. Nothing on the board is hidden behind a click, which was the one
firm rule: a recruiter with twenty seconds should not have to open anything.

### Photographs

Joe supplied three photographs, which are the first images on the site. They
live in `src/assets/` rather than `public/` so that Astro processes them.

- The professional headshot, cropped to 4:5, sits beside the intro on the about
  page and stacks below it on a phone.
- The graduation photograph, cropped square and tight enough to keep the
  pointing hand in frame, is pinned to the board.
- The capstone team photograph, cropped to 3:2 with the ceiling
  trimmed away, is pinned to the board and links into the ACC case study.

Cropping was done with `sharp`, which ships with Astro, rather than by hand. The
originals total roughly 12MB and stay untouched in `dev/source-material/`. Astro
generates three WebP sizes of each at build time, so a phone downloads about
30KB and a desktop about 60KB.

The team photograph shows eight other people. Joe confirmed a teammate had
already posted it publicly on LinkedIn, so consent was not an open question. The
poster in the shot lists teammate names in small print and carries a QR code;
both were checked and are far too small at the rendered size to be read or
scanned.

### Fonts, and why the first choice failed

Joe asked for distinctive headings with readable body text. Fraunces was fitted
first and rejected for one specific reason: its J descends below the baseline
and curls, and J is the first letter of his name, so it appears everywhere.

Rather than guess again, a throwaway page at `/font-test` rendered "Joe Fazio"
in five candidates at full size with a line of bare J's under each. Joe picked
**Gabarito**. The test page and the four losing families were deleted
immediately afterwards.

The typography is now Gabarito for headings and the wordmark, Inter for body
text.

**The infrastructure piece here is worth recording.** Astro 7 has a stable Fonts
API, configured with a `fonts` array in `astro.config.mjs`. It downloads the
font files at build time and serves them from joefazio.dev. The alternative, a
`<link>` to Google's CDN, means every visitor's browser opens a connection to
Google before the text can render. Self-hosting removes a DNS lookup and a TLS
handshake from the critical path and tells Google nothing about who visits the
site. Verified after the build: two `woff2` files under `dist/_astro/fonts/`,
both preloaded, and no `fonts.googleapis.com` or `fonts.gstatic.com` string
anywhere in `dist/`.

### The word slop cut

Joe's words: "not a single person is reading through all of that word slop."
Measured on the built HTML, including about 40 words of nav and footer
boilerplate on every page:

| Page | Before | After |
| --- | --- | --- |
| ACC case study | ~1,440 | 673 |
| Projects | ~640 | 513 |
| About | 272 | 277 |
| Home | 45 | 176 |

The case study came down by more than half. The projects page came down by only
about a fifth, which was reported as falling short rather than presented as a
win; cutting it further means dropping entries or going to two sentences each,
and that is Joe's call. About and home went up slightly, but both gained a
photograph and real content in exchange.

### The ACC case study, rewritten

**All code excerpts are gone, and so is the security self-critique.** This
reverses the 2026-09-18 decision to name the plaintext-password flaw openly, and
it contradicts the standing note in CLAUDE.md that said not to remove that
section. The contradiction was raised explicitly before anything was deleted
rather than actioned silently, because "do not quietly remove it" was the point
of that note. Joe confirmed.

The reason is stronger than stylistic preference. It matches the standing
constraint that everything on the site must be defensible in conversation.
Published code invites line-by-line questions, and the case study makes a better
argument without it: what the client needed, and what was built to meet it.

With no code on the page, the redaction rule has nothing left to act on, though
the `dist/` grep still runs.

The page is now five sections: what ACC needed, how we solved it, what it does,
handing it over, where it stands. The ledger-mechanics walkthrough, the
five-state request lifecycle and the guardian-authorisation detail were all cut
as mechanism nobody asked for. What survived is the reasoning: why AppSheet was
abandoned, why a Google Sheet was the right recommendation for this client even
though a real database would have been cleaner, and why the handover runbook is
the part closest to the IT work Joe is applying for.

### The KPMG award

Two facts about the capstone surfaced this session that had never been captured:
the team, Purple Peak Consulting, received the **KPMG Choice Award for Best
Overall System**, and the system runs at a cost of **$0**, which is worth
stating plainly for a nonprofit client.

The award is now in the case study spec box and on the projects page, phrased as
the team receiving it rather than claimed personally, because that is what
happened and because claiming it personally is the kind of thing an interviewer
unpicks in one question.

Adding it to the resume was raised and declined for now: there is no obvious
place it fits. Revisit only if Joe raises it.

### Capsim, reframed

The old entry was built around deciding under incomplete information and
strategy needing follow-through, which read as a lesson learned from doing
badly. Joe asked for the opposite emphasis.

The entry now leads with the cross-functional angle. It was a College of
Business simulation, his teammates were marketing, management and accounting
majors, and he ran R&D, revising product designs each round against shifting
segment buying criteria. It closes on what that taught him about how a technical
decision reads to the people who have to sell, staff and account for it. No
outcomes, no numbers. The 2026-09-18 decision to keep the entry broad and
lesson-focused still holds; only the lesson changed.

### Other honesty fixes

The BRHS entry's byline still listed "NIST CSF 2.0, CIS Controls v8" even though
the 2026-09-18 session had corrected the body text to NIST only. The byline now
matches the body. The resume still claims both, which remains Joe's call.

The about page gained the reliable-and-persistent line. Those two traits were
supposed to lead and were not on the page at all.

### What broke

Nothing broke. Two things needed correcting mid-session:

- Removing Fraunces from the config left `--font-display` undefined while the
  layout still referenced it, which would have silently dropped headings to the
  browser default. Caught by reading the layout rather than by the build, since
  an undefined CSS variable is not a build error. Fixed with an explicit
  fallback chain while the font was undecided.
- A config change does not hot-reload. The dev server was restarted after each
  `astro.config.mjs` edit.

The heredoc lesson from 2026-09-18 held: all large page content this session was
written with the editor tool, and none of it failed.

### What is next

1. Joe is writing record store content: the Top 25 Albums list, the list of
   records he owns, the one-line notes for the movies and games pages, and
   further UI ideas. Those land next session.
2. Build `/albums` and `My Record Collection`, then flip both dimmed sleeves
   live. The collection should be a data file Joe edits when he buys a record,
   not hand-written markup.
3. Decide whether to cut the projects page further. It came down only a fifth
   this session and is the longest page that is not the case study.
4. Decide whether to credit the other developer on the ACC case study.
5. Decide on CIS Controls v8 in the
   BRHS bullet. The KPMG award was considered for the resume and declined.
6. Delete the stale `home-page` branch on GitHub. Raised twice now and still
   unanswered; it was never merged and never will be.
7. Decide between inline notes and a real blog at `/writing`. The standing
   recommendation is to fill in notes first and build the blog when there is a
   first real post.
8. Wire up the parked Letterboxd, Steam and Spotify links once Joe supplies the
   profile URLs.
9. Still carried over: confirm Node 24 in the Cloudflare Pages build log.
10. Still carried over: open VS Code on the `portfolio` folder rather than
    `portfolio\node_modules`.
11. Later: deploying from Actions with Wrangler; Terraform for the Cloudflare
    configuration; updating the LinkedIn and resume links to joefazio.dev.

## 2026-09-20 (cleanup after pull request 13)

### What changed
- Deleted the stale `home-page` branch on GitHub. Only `main` remains.
- Removed individual people's names from the decision log and the case study
  spec box. The team name stays; individuals do not.
- Removed a line from the decision log that described private reasoning about
  how the capstone code was written.
- Added three standing rules to CLAUDE.md: keep commit and pull request text
  short, never name other people in anything public, and never publish the
  internal authorship note.

### Why
Commit messages, pull request descriptions and this log are all public. They
should record what changed, not narrate private reasoning or name people who
did not choose to be listed.

### What broke
Pull request 13 was merged before these corrections were written, so the
original commit message and the pre-fix file content are still reachable from
`main`'s history. The working files are correct now, but history is not.
Removing it needs a history rewrite, which is Joe's call and has not been done.
The same tradeoff was faced and accepted once before, in the 2026-09-16 entry.

### What is next
Unchanged from the entry above, minus the stale branch and the resume item,
both now closed.
