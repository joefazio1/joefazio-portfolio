# Glossary

Plain-language definitions for terms used in this project, grouped by topic.

## Websites and hosting

### Static site
A website made of pre-built files (HTML, CSS, images) that the server hands out as-is, with no code running on the server per visit.

### Static site generator
A tool that turns source files (templates, Markdown) into a static site ahead of time.

### Astro
The static site generator this site uses; it builds content-focused pages with very little JavaScript.

### Build
The step that turns source code into the finished files a browser can load; here, `npm run build`.

### dist/
The folder where Astro puts the finished site after a build; this is what gets published.

### Bundler
The part of a build tool that combines and shrinks source code into the few files a browser actually downloads; Astro 7 uses Vite 8 with the Rolldown bundler.

### Minification
Removing characters a browser does not need — spaces, line breaks, comments — so files download faster.

### Block-level vs inline elements
Block elements (`<p>`, `<main>`, `<div>`) stack vertically, and whitespace between them is ignored; inline elements (`<span>`, `<em>`) sit inside a line of text, where a space between them is visible and meaningful.

### compressHTML (Astro config)
Astro's setting for stripping whitespace out of the built HTML. Astro 7 changed the default to `'jsx'`, which also removes whitespace between inline elements that earlier versions kept as a single space.

### `site` (Astro config)
The setting in `astro.config.mjs` that tells Astro the site's real public address, so it can generate full links like sitemaps and canonical URLs.

### Canonical URL
A tag telling search engines which address is the "official" one for a page, so duplicates don't compete.

### Sitemap
A file listing every page on a site so search engines can find them.

### Cloudflare Pages
Cloudflare's hosting service for static sites; it watches the GitHub repo, builds each new commit, and publishes the result.

### pages.dev
The free address Cloudflare Pages gives every project (this one is `joefazio-portfolio.pages.dev`).

### Cloudflare Workers
Small programs that run on Cloudflare's servers when a request comes in, used for backend features a static site can't do alone.

### KV (Workers KV)
Cloudflare's simple key-value storage (like a dictionary: a name maps to a value) that Workers can read and write.

### 404
The HTTP status code a server returns when it can't find the requested page.

### Custom domain
A domain name you own (like `yourname.com`) pointed at your hosting instead of the free provider address.

### DNS (Domain Name System)
The internet's phone book: it translates a domain name into the address of the server that hosts it.

### CDN (Content Delivery Network)
A network of servers around the world that keeps copies of a site so visitors load it from a nearby location.

### WAF (Web Application Firewall)
A filter in front of a website that blocks malicious requests before they reach it.

### /now page
A short page saying what someone is currently working on and learning, dated so a reader can tell how current it is. A small convention on personal sites.

## Domains, DNS, and certificates

### TLD (top-level domain)
The last part of a domain name, like `.com` or `.dev`; each one is run by a registry.

### Registry
The organization that operates a TLD and keeps the master list of every domain under it.

### Registrar
The company you buy a domain from, which registers it with the registry on your behalf; Cloudflare is this project's registrar.

### ICANN
The nonprofit that coordinates domain names worldwide; it adds a small per-domain fee, about $0.18/yr.

### At-cost pricing
Charging only what the registry and ICANN charge, with no markup; it also means the renewal price matches the first-year price instead of jumping.

### WHOIS / RDAP
Public lookups showing whether a domain is registered and by whom; RDAP is the newer structured replacement for WHOIS and gives the authoritative answer on availability.

### WHOIS redaction (privacy)
Keeping your personal contact details out of those public records; Cloudflare does this for free.

### Zone
A domain's complete set of DNS records, managed together as one unit.

### Nameserver
The server that answers DNS questions for a domain; whoever controls it controls where the domain points.

### DNS record
A single entry in a zone saying what a name points to and what kind of pointer it is.

### A record
A record pointing a name straight at an IP address.

### CNAME record
A record pointing a name at another name rather than an address, so it follows wherever that name leads.

### Apex (root) domain
The bare domain with nothing in front, like `joefazio.dev`; the DNS standard does not allow an ordinary CNAME here.

### CNAME flattening
Cloudflare's workaround for that rule: it resolves the target to an address before answering, so the apex can behave like a CNAME.

### Subdomain
A name placed in front of the domain, like `www.joefazio.dev`, which can point somewhere different from the apex.

### HTTPS
HTTP with the traffic encrypted, so nobody in between can read or tamper with it.

### TLS/SSL certificate
The file proving a site really controls its domain, which is what lets browsers show HTTPS; Cloudflare issues and renews it automatically.

### HSTS preload
A list built into browsers naming domains that may only ever load over HTTPS; every `.dev` domain is on it automatically.

### TTL (time to live)
How long other servers are allowed to cache a DNS answer before asking again.

### DNS propagation
The wait while cached copies of an old DNS answer expire around the internet and the new one takes over.

### Negative caching
A resolver remembering "this name has no record" for a while, so a record you just added can stay invisible to it until that memory expires.

### Proxied record (orange cloud)
A Cloudflare DNS record whose traffic passes through Cloudflare first, which is what lets Cloudflare's rules, redirects, and caching act on it.

### Documentation address (192.0.2.1)
An IP address reserved for examples that never belongs to a real server; used as a placeholder when a record only needs to exist.

### 301 redirect
A "moved permanently" response telling the browser, and search engines, to use a different URL from now on.

## Git and GitHub

### Git
A tool that records the history of changes to a project's files.

### GitHub
The website that hosts copies of Git repositories online; Git is the tool on your PC, GitHub is where the repo lives publicly.

### Repository (repo)
A project folder tracked by Git, including its full change history.

### Commit
A saved snapshot of the project's files at a point in time, with a message describing the change.

### Staging (git add)
Choosing which changed files go into the next commit; staged files show in green in `git status`.

### git diff --staged
Shows the exact line-by-line changes that are staged and about to be committed.

### Ahead of origin/main
What `git status` says when you have local commits that haven't been pushed to GitHub yet.

### Pager
The scrolling viewer Git uses for long output like `git log` or `git diff`; press `q` to exit it.

### History
Every commit ever made in a repo; a file deleted today can still be read from an older commit.

### Branch
A separate line of commits; `main` is the default branch that the live site is built from.

### Remote
A copy of the repo hosted somewhere else (here, GitHub), named `origin` by default.

### Push
Uploading local commits to the remote.

### Pull request (PR)
A proposal on GitHub to merge one branch's changes into another, where checks run and changes can be reviewed first.

### .gitignore
A file listing files and folders Git should never track or upload.

### Untracking a file
Telling Git to stop recording a file (`git rm --cached`) while leaving it on your computer; older commits still contain it.

### Rewriting history / force push
Changing past commits and overwriting the remote copy with them; used to scrub something from history, but disruptive and hard to undo.

### Force-with-lease
A safer force push that only overwrites the remote if it still points at the commit you expect, so you can't wipe out changes you haven't seen.

### Unreachable (dangling) commit
An old commit that no branch points to anymore; GitHub can keep serving it by its exact ID for a while after a history rewrite.

### git filter-branch
A built-in Git command that rewrites every commit on a branch, for example to remove one file from all of them.

### Git bundle
A single file containing a repo's full history, useful as a backup before risky Git operations.

### Branch protection
A GitHub rule that blocks changes to a branch unless conditions are met, like a passing check. Enforced on GitHub's servers, so it holds no matter which computer or Git client the push comes from.

### Check run
A pass/fail result GitHub shows on a commit, reported by a tool like GitHub Actions or Cloudflare Pages.

### Line endings (LF / CRLF)
The invisible characters marking the end of a line: Linux/macOS use LF, Windows uses CRLF; Git can convert between them.

### Ruleset
GitHub's current system for branch rules, at Settings → Rules → Rulesets. It replaces the older "branch protection rule" screen and adds a bypass list, an `Evaluate` dry-run mode, and targeting by pattern rather than one branch at a time.

### Bypass list (ruleset)
The people or roles allowed to ignore a ruleset's rules. Left empty, the rules apply to everyone, including the repository owner.

### Evaluate mode (ruleset)
A dry run: GitHub records what a ruleset *would* have blocked without actually blocking it, so a rule can be tested before it starts refusing pushes.

### Required status check
A named check that must report success before a pull request can be merged. It is matched by **job** name (here `build`), not by the workflow's `name:` field.

### Required approvals
How many people must approve a pull request before it can merge. GitHub never lets you approve your own, so on a solo repo this has to be `0` or nothing is ever mergeable.

### GH013 / remote rejected
The error Git prints when GitHub's server refuses a push for violating a repository rule. `[remote rejected]` means the refusal came from GitHub, not from anything local.

### Merge commit
The commit GitHub creates when a pull request is merged, joining the branch's history into the target branch; it is what `main` advances to.

### git reset --hard
Moves the current branch to a given commit and discards everything after it, including uncommitted file changes. Used here as `git reset --hard origin/main` to drop a commit that the server had refused.

### Remote-tracking branch
Your local record of where a branch sat on the remote the last time you checked, shown as `origin/<name>`. It does not update by itself.

### Deleting a branch: local vs remote
`git branch -d <name>` deletes only your copy. The branch on GitHub survives until it is deleted there, with the button on the merged pull request or `git push origin --delete <name>`.

### git fetch --prune
Removes remote-tracking branches for branches that no longer exist on the remote, clearing stale `origin/<name>` entries.

### Stale branch
A branch whose commits are already merged into `main`, so it holds no unique work. Deleting it removes the label only; the commits stay in `main`'s history through the merge commit.

### Automatically delete head branches
A GitHub repository setting that deletes a pull request's source branch as soon as the pull request merges, so merged branches never pile up.

## Node and npm

### Node.js
A program that runs JavaScript outside a browser; Astro needs it to build the site.

### LTS (Long-Term Support)
A Node version that is officially maintained with fixes for an extended period.

### End-of-life (EOL)
The date a version stops receiving security fixes; Node 20 reached EOL in April 2026.

### .node-version
A file stating which Node version the project uses, read by GitHub Actions and Cloudflare Pages.

### npm
Node's package manager: it downloads the libraries a project depends on.

### package.json
The file listing the project's name, commands (scripts), and the packages it depends on.

### package-lock.json (lockfile)
A file recording the exact version of every package installed, so every install gets the same ones.

### node_modules/
The folder where npm puts downloaded packages; it is regenerated from the lockfile and never committed.

### npm install vs npm ci
`npm install` can update the lockfile; `npm ci` installs exactly what the lockfile says and fails if it doesn't match `package.json`, which makes automated builds repeatable.

### Dependency
A package the project needs in order to work, listed in `package.json`.

### Transitive dependency
A package you never asked for directly; it got installed because one of your dependencies needs it.

### Semantic versioning (semver)
The `major.minor.patch` numbering scheme: a patch fixes bugs, a minor adds features without breaking anything, and a major may break existing code.

### Caret range (^)
A version rule like `^7.3.2` meaning "any 7.x release from this one up," so npm accepts compatible updates but never jumps to 8 on its own.

### Breaking change
A change in a new major version that can stop working code from working, which is why major upgrades are done deliberately and one at a time.

### Install script (postinstall)
Code a package runs automatically right after npm downloads it, often to fetch the compiled binary for your operating system; useful, but it is also code that arrived without being reviewed.

### allowScripts (package.json)
The field recording which packages are allowed to run install scripts, so `npm ci` runs them in automated builds instead of warning every time.

### engines (package.json)
A package's statement of which Node and npm versions it supports; Astro 7 requires Node 22.12.0 or newer.

## CI/CD and GitHub Actions

### CI/CD
Continuous integration and continuous deployment: automatically checking code on every change (CI) and automatically releasing it (CD).

### GitHub Actions
GitHub's built-in automation service that runs tasks when something happens in a repo, like a push.

### Workflow
A YAML file in `.github/workflows/` that defines when an automation runs and what steps it performs.

### YAML
A plain-text format for configuration files that uses indentation to show structure.

### Runner
The temporary virtual machine GitHub starts to run a workflow; it is thrown away afterward.

### Job and step
A job is a group of steps that runs on one runner; a step is a single command or action inside it.

### Action (reusable)
A prepackaged step someone published, like `actions/checkout`, used with `uses:` and a version tag such as `@v7`.

### Deploy gate
A check that must pass before code is allowed to go live. Since 2026-09-18 this project's `build` workflow is one: nothing reaches `main` without it passing, and Cloudflare Pages deploys from `main`. Pages itself still does not wait for the check — the gate controls what enters the branch, not what Pages does with it.

### GITHUB_TOKEN
A temporary access key GitHub automatically gives each workflow run so it can interact with the repo.

### Least privilege
The security principle of giving a person or program only the access it needs and nothing more.

### Queued (job status)
A workflow run that GitHub has created but not yet started, because it is waiting for a runner. Normally clears in under a minute or two.

### "Expected — Waiting for status to be reported"
What a pull request shows for a required check that has not reported yet. The message is the same whether the job is simply queued or the required check name matches no real job — the Actions tab tells them apart: a run that exists means waiting, no run at all means a wrong name.

### Preview deployment
A build of a branch or pull request published at its own temporary URL, separate from production. Cloudflare Pages makes these automatically and does not wait for any check first.

## Security and infrastructure as code

### Secret
A value that grants access, like a password or API key, which must never be committed to a public repo.

### Environment variable
A named value supplied to a program from outside its code, often used to pass in secrets.

### .env / .dev.vars
Local files that hold environment variables and secrets during development (`.dev.vars` is the Cloudflare Workers version); always gitignored.

### Terraform
A tool that creates and changes infrastructure (like DNS records) from configuration files instead of clicking through a dashboard.

### Infrastructure as code (IaC)
Managing servers, DNS, and other infrastructure through version-controlled files rather than manual setup.

### Terraform state file (.tfstate)
Terraform's record of what it has built; it can contain secrets in plain text, so it is never committed.

### npm audit
An npm command that checks installed packages against a public list of known security flaws.

### Security advisory (vulnerability)
A published notice that a specific version of a package has a security flaw, usually with the version that fixes it.

### NIST Cybersecurity Framework (NIST CSF)
A US government framework that sorts security work into five questions an organisation answers about itself: Identify (what do we have and what could go wrong), Protect (what stops it), Detect (how would we notice), Respond (what do we do when it happens), Recover (how do we get back). It describes outcomes, not products, so it suits an organisation assessing how mature it currently is.

### CIS Controls v8
A prioritised list of 18 specific safeguards, ordered so the first ones block the most common attacks. Where NIST CSF asks what outcomes you want, CIS Controls tells you what to go and do, in what order. It suits a team that already knows it is exposed and wants a to-do list.

### Choosing between NIST CSF and CIS Controls
They are not rivals and they overlap heavily. The practical split: NIST CSF is the better fit for assessing and communicating current posture to leadership, CIS Controls for sequencing the remediation work afterwards.

## Windows and local development

### PowerShell execution policy
A Windows safety setting that controls whether PowerShell may run script files (`.ps1`); on a fresh Windows install it blocks them.

### RemoteSigned
An execution policy setting that runs scripts created on your own computer but requires scripts downloaded from the internet to be digitally signed.

### Working directory
The folder a terminal is currently "in"; commands like `npm run build` look for project files there, so you `cd` into the project first.

### ENOENT
An error code meaning "no such file or directory": the program looked for a file that isn't where it expected.

### npm.ps1 vs npm.cmd
Two launchers for npm on Windows; PowerShell picks the `.ps1` script first (blocked by the execution policy), while `npm.cmd` is not a PowerShell script and is not blocked.

### Symbolic link
A shortcut-like file that points to another file's real location, so programs opening the link actually open the target.

### Dev server
A local preview server (`npm run dev`) that rebuilds the site instantly as you edit; for development only, never for the public.

### localhost vs 0.0.0.0
`localhost` means "only this computer can connect"; `0.0.0.0` means "accept connections from any device on the network."

## Fonts and images on the web

### Web font
A font file the browser downloads with the page, so text renders in a typeface the visitor does not already have installed.

### Self-hosted font
A web font served from your own domain instead of a third party's CDN; it avoids an extra connection to someone else's server and tells that third party nothing about your visitors.

### Astro Fonts API
Astro's built-in font handling: it downloads the font files at build time, writes the `@font-face` rules for you, and serves the files from your own site.

### woff2
The standard compressed file format for web fonts; smaller than the formats it replaced and supported by every current browser.

### Preload
A hint in the page `<head>` telling the browser to start downloading a file immediately rather than waiting until it discovers the need for it.

### Variable font
One font file that contains a whole range of weights or styles, adjustable by number, instead of a separate file per weight.

### Fallback font
The typeface a browser uses if the web font has not arrived yet or fails to load; listed after the web font in the CSS `font-family` line.

### WebP
A modern image format that produces noticeably smaller files than JPEG at the same visual quality.

### Responsive images
Publishing several sizes of one image and letting the browser pick the smallest one that still looks sharp on that screen, so phones do not download desktop-sized files.

### sharp
The image-processing library Astro uses under the hood to crop, resize and convert images during the build.

### Runbook
A written procedure for operating and recovering a system, aimed at whoever has to run it later rather than at the person who built it.

### Content hash
A short string in a built file's name (`headshot.4USbYTB3_Z26vfcl.webp`) calculated from the file's contents. Change the file and the name changes with it.

### Cache busting
Using a content hash in a filename so that new content always arrives at a new URL, which no browser or CDN can have cached yet.

### Browser cache
The copy of a file your own browser keeps so it does not download it twice. It is keyed on the URL, so if a file changes but its URL does not, the browser keeps serving the old copy.

### Hard reload
Reloading a page while telling the browser to ignore its cache (Ctrl+Shift+R). The fix when the site on disk is correct but the screen is not.

## Page layout

### CSS Grid
A layout system that arranges elements into rows and columns, rather than letting them flow one after another.

### Grid track
One row or one column of a grid.

### auto-fit
A grid setting that lets the browser decide how many columns fit at the current width. Flexible, but it gives up control of which item lands where.

### Grid template areas
Naming each region of a grid and assigning items to those names, so the layout is written out as a small picture in the CSS and items can be rearranged without touching the HTML.

### Media query
A block of CSS that only applies when a condition is met, usually a minimum screen width.

### Breakpoint
The width at which a layout changes, named in a media query; this site switches the home board from one column to two at 46rem.

### rem
A CSS length equal to the page's base font size, so layouts measured in rem scale with the reader's text-size setting instead of ignoring it.

### Progressive enhancement
Building the plain version first so it works without JavaScript, then layering extras on top for browsers that can run them.
