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
A GitHub rule that blocks changes to a branch unless conditions are met, like a passing check.

### Check run
A pass/fail result GitHub shows on a commit, reported by a tool like GitHub Actions or Cloudflare Pages.

### Line endings (LF / CRLF)
The invisible characters marking the end of a line: Linux/macOS use LF, Windows uses CRLF; Git can convert between them.

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
A check that must pass before code is allowed to go live; this project's Actions workflow is currently **not** one.

### GITHUB_TOKEN
A temporary access key GitHub automatically gives each workflow run so it can interact with the repo.

### Least privilege
The security principle of giving a person or program only the access it needs and nothing more.

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

### Dev server
A local preview server (`npm run dev`) that rebuilds the site instantly as you edit; for development only, never for the public.

### localhost vs 0.0.0.0
`localhost` means "only this computer can connect"; `0.0.0.0` means "accept connections from any device on the network."
