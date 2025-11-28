# Git Setup and Push to Dev Branch

## Initialize Git Repository
```bash
cd /path/to/TOON-JSON
git init
```

## Add All Files
```bash
git add .
```

## Create Initial Commit
```bash
git commit -m "Initial commit: TOON Data & Token Studio"
```

## Create and Switch to Dev Branch
```bash
git checkout -b dev
```

## Add Remote Origin
```bash
git remote add origin https://github.com/hemanth090/TOON-JSON.git
```

## Push to Dev Branch
```bash
git push -u origin dev
```

## Optional: Create Main Branch (without pushing)
```bash
git branch main
```

---

## Workflow Going Forward

### For New Features:
```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name

# Make changes, then commit
git add .
git commit -m "Add: your feature description"

# Push feature branch
git push origin feature/your-feature-name
```

### Merge to Dev:
```bash
# Switch to dev and merge
git checkout dev
git merge feature/your-feature-name
git push origin dev
```

### When Ready for Production:
```bash
# Merge dev to main
git checkout main
git merge dev
git push origin main
```

---

## Current Branch Structure
- `dev` - Development branch (active development)
- `main` - Production branch (stable releases)

All new code goes to `dev` first, then merges to `main` when stable.
