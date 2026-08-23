# 🚀 GitHub Builder — Daily Activity & Learning Log Automation

[![Daily Activity & Learning Log Builder](https://github.com/USERNAME/REPO_NAME/actions/workflows/daily-update.yml/badge.svg)](https://github.com/USERNAME/REPO_NAME/actions/workflows/daily-update.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

An intelligent, lightweight GitHub automation that maintains a consistent, high-quality engineering and learning journal on your repository. 

Every day on a scheduled cadence (or on-demand via manual trigger), a GitHub Actions workflow executes an automated learning generator, updates `activity.txt`, appends structured notes to `learning-log.md`, and creates conventional commits linked to your GitHub account.

---

## 🌟 Key Features

- ⏱ **Multi-Schedule Automation**: Pre-configured to run across 4 realistic intervals daily (Morning, Afternoon, Evening, Night).
- 🧠 **Curated Tech Curriculum**: Rotates deterministically through diverse engineering tracks:
  - **AI & Machine Learning** (LLM Fine-tuning, RAG, Multi-Agent Systems, Neural Nets, PyTorch)
  - **Full-Stack & Cloud Architecture** (Microservices, Next.js App Router, Distributed Caching, Security)
  - **DevOps & Cloud Infrastructure** (Kubernetes, Terraform IaC, CI/CD Security, Observability)
  - **System Design & Algorithms** (Distributed Consensus, Rate Limiters, Graph Algorithms, Dynamic Programming)
- 🎯 **Profile Contribution Graph Compatibility**: Easily link your personal verified GitHub email so automated commits contribute directly to your green profile squares.
- ⚡ **Manual Dispatch with Custom Topics**: Trigger on-demand via GitHub Actions UI with custom topics or test dry-runs.
- 💻 **Cross-Platform Local Runner**: Includes a standalone Python runner (`scripts/generate_log.py`) to test, preview, or run locally on Windows, macOS, and Linux.
- 📝 **Conventional Commits**: Produces clean semantic commit messages (`docs:`, `study:`, `feat:`, `refactor:`, `track:`).

---

## 📂 Repository Structure

```
├── .github/
│   └── workflows/
│       └── daily-update.yml     # Automated GitHub Actions workflow
├── scripts/
│   └── generate_log.py          # Log generator engine & curriculum rotator
├── activity.txt                 # Real-time status line of the latest session
├── learning-log.md              # Running journal of dated learning entries
├── .gitignore                   # Ignore rules for OS & temporary files
└── README.md                    # Documentation & setup guide
```

---

## 🚀 Quick Start & Setup Guide

### 1. Initialize & Push to GitHub

If you haven't already created a GitHub repository:

```bash
# 1. Initialize git repository
git init

# 2. Stage and commit files
git add .
git commit -m "feat: initial repository setup for github builder"

# 3. Rename branch to main
git branch -M main

# 4. Link your remote GitHub repository
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git

# 5. Push to GitHub
git push -u origin main
```

### 2. Enable GitHub Actions Write Permissions (Crucial ⚠️)

GitHub Actions requires write permissions to push commits back to your repository:

1. Open your repository on GitHub.
2. Go to **Settings** → **Actions** → **General**.
3. Scroll down to **Workflow permissions**.
4. Select **"Read and write permissions"**.
5. Check the box for **"Allow GitHub Actions to create and approve pull requests"**.
6. Click **Save**.

---

## 🟩 How to Make Commits Count on Your Contribution Graph

GitHub only attributes commits to your personal contribution graph (the green squares) if the commit email matches a **verified email address** on your GitHub account.

You can configure your identity in one of two easy ways:

### Option A: Repository Variables / Secrets (Recommended)
1. Go to your repository **Settings** → **Secrets and variables** → **Actions**.
2. Click the **Variables** tab (or **Secrets** if you prefer keeping your email private).
3. Add two items:
   - `GIT_USER_NAME`: Your GitHub username (e.g. `yourusername`)
   - `GIT_USER_EMAIL`: Your GitHub account's primary/verified email (e.g. `you@example.com` or your `id+username@users.noreply.github.com`)

### Option B: Automatic Default
If you don't add secrets, the workflow automatically uses `github.actor` and `github.actor@users.noreply.github.com`. Make sure "Keep my email addresses private" settings in your GitHub profile allow noreply commits.

---

## 🕒 Schedule & Timezone Reference

The workflow schedule is defined in `.github/workflows/daily-update.yml` using standard UTC cron syntax:

```yaml
schedule:
  - cron: "30 4 * * *"   # 10:00 AM IST / 04:30 UTC
  - cron: "30 8 * * *"   # 02:00 PM IST / 08:30 UTC
  - cron: "30 13 * * *"  # 07:00 PM IST / 13:30 UTC
  - cron: "30 16 * * *"  # 10:00 PM IST / 16:30 UTC
```

### UTC Timezone Conversion Cheat Sheet

| Desired Time (IST) | Desired Time (EST) | Desired Time (PST) | UTC Cron Expression |
| :--- | :--- | :--- | :--- |
| 10:00 AM IST | 11:30 PM (prev) EST | 08:30 PM (prev) PST | `30 4 * * *` |
| 02:00 PM IST | 03:30 AM EST | 12:30 AM PST | `30 8 * * *` |
| 07:00 PM IST | 08:30 AM EST | 05:30 AM PST | `30 13 * * *` |
| 10:00 PM IST | 11:30 AM EST | 08:30 AM PST | `30 16 * * *` |
| 12:00 AM Midnight | 07:00 PM (prev) EST | 04:00 PM (prev) PST | `0 0 * * *` |

---

## 🕹️ Manual Execution & Custom Logs

You can trigger a manual run anytime directly from GitHub:

1. Navigate to the **Actions** tab in your GitHub repository.
2. Under **Workflows**, click on **Daily Activity & Learning Log Builder**.
3. Click the **Run workflow** dropdown on the right:
   - **Custom study topic** *(optional)*: Type any specific topic you worked on (e.g. `Building Distributed Key-Value Store`).
   - **Custom session label** *(optional)*: e.g. `Weekend Hackathon Sprint`.
   - **Dry run**: Check this if you want to test the workflow without committing or pushing.
4. Click **Run workflow**.

---

## 🛠️ Local Usage & Testing

You can also run the generator locally on your machine anytime using Python 3:

```bash
# Preview without modifying files (Dry Run)
python scripts/generate_log.py --dry-run

# Generate and write a standard scheduled session
python scripts/generate_log.py

# Log a specific custom topic
python scripts/generate_log.py --topic "Implementing Raft Consensus from Scratch" --session "Evening Coding Session"
```

---

## 🎨 Customizing Your Learning Tracks

To add your own topics, tech stacks, or domains, edit the `CURRICULUM` dictionary inside [`scripts/generate_log.py`](file:///scripts/generate_log.py):

```python
CURRICULUM = {
    "Your Custom Domain": [
        "Topic 1: Deep dive into...",
        "Topic 2: Architecture of...",
        "Topic 3: Benchmarking...",
    ],
    # Add more domains as desired
}
```

---

## 📄 License

Distributed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to adapt and customize for your own projects and learning goals.
