# Git Skills — Agent Reference

A comprehensive reference for AI agents to perform git operations. Each skill includes the command, usage context, and common flags.

---

## Repository Setup

### Initialize a new repository
```bash
git init
git init <directory>
git init --bare  # Server-side repo without working directory
```

### Clone an existing repository
```bash
git clone <url>
git clone <url> <directory>
git clone --depth 1 <url>          # Shallow clone (latest commit only)
git clone --branch <branch> <url>  # Clone specific branch
git clone --recurse-submodules <url>  # Clone with submodules
```

### Configure identity (required before first commit)
```bash
git config user.name "Name"
git config user.email "email@example.com"
git config --global user.name "Name"   # Set globally
git config --list                      # View all config
git config --get <key>                 # View specific config
```

---

## Staging & Committing

### Check working tree status
```bash
git status
git status -s           # Short format
git status --ignored    # Show ignored files
```

### Stage changes
```bash
git add <file>                  # Stage specific file
git add <file1> <file2>         # Stage multiple files
git add <directory>             # Stage all changes in directory
git add -A                      # Stage all changes (new, modified, deleted)
git add -p                      # Interactive staging (hunk by hunk)
git add '*.js'                  # Stage by pattern
```

### Unstage changes
```bash
git restore --staged <file>     # Unstage file (keep changes)
git reset HEAD <file>           # Alternative unstage
git reset HEAD                  # Unstage everything
```

### Commit
```bash
git commit -m "message"
git commit -m "subject" -m "body"      # Multi-line commit
git commit -am "message"               # Stage tracked files + commit
git commit --amend -m "new message"    # Amend last commit message
git commit --amend --no-edit           # Amend last commit, keep message
git commit --allow-empty -m "message"  # Empty commit (useful for CI triggers)
```

### Using HEREDOC for multi-line commit messages
```bash
git commit -m "$(cat <<'EOF'
Subject line here

Body of the commit message.
More details.

Co-Authored-By: Agent <agent@example.com>
EOF
)"
```

---

## Branching

### List branches
```bash
git branch              # Local branches
git branch -r           # Remote branches
git branch -a           # All branches (local + remote)
git branch -v           # Branches with last commit
git branch --merged     # Branches merged into current
git branch --no-merged  # Branches not merged into current
```

### Create branches
```bash
git branch <name>                  # Create branch
git checkout -b <name>             # Create and switch
git switch -c <name>               # Create and switch (modern)
git branch <name> <start-point>    # Create from specific commit/branch
git checkout -b <name> origin/<remote-branch>  # Create tracking branch
```

### Switch branches
```bash
git checkout <branch>
git switch <branch>       # Modern alternative
git switch -              # Switch to previous branch
```

### Rename branches
```bash
git branch -m <old> <new>    # Rename branch
git branch -m <new>          # Rename current branch
```

### Delete branches
```bash
git branch -d <name>     # Delete (safe — only if merged)
git branch -D <name>     # Force delete
git push origin --delete <name>  # Delete remote branch
```

---

## Merging

### Merge a branch
```bash
git merge <branch>
git merge <branch> --no-ff          # Force merge commit (no fast-forward)
git merge <branch> --squash         # Squash all commits into one
git merge <branch> -m "message"     # Custom merge commit message
git merge --abort                   # Abort an in-progress merge
git merge --continue                # Continue after resolving conflicts
```

### Check merge conflicts
```bash
git diff --name-only --diff-filter=U   # List conflicted files
git diff --check                        # Show conflict markers
```

---

## Rebasing

### Rebase current branch
```bash
git rebase <branch>               # Rebase onto branch
git rebase <branch> --onto <new>  # Rebase onto different base
git rebase --abort                # Abort rebase
git rebase --continue             # Continue after resolving conflicts
git rebase --skip                 # Skip current commit
```

---

## Remote Operations

### Manage remotes
```bash
git remote -v                          # List remotes with URLs
git remote add <name> <url>            # Add remote
git remote remove <name>               # Remove remote
git remote rename <old> <new>          # Rename remote
git remote set-url <name> <url>        # Change remote URL
git remote show <name>                 # Detailed remote info
```

### Fetch
```bash
git fetch                    # Fetch from default remote
git fetch <remote>           # Fetch from specific remote
git fetch --all              # Fetch from all remotes
git fetch --prune            # Fetch and remove stale remote branches
git fetch <remote> <branch>  # Fetch specific branch
```

### Pull
```bash
git pull                          # Fetch + merge
git pull --rebase                 # Fetch + rebase (cleaner history)
git pull <remote> <branch>        # Pull specific branch
git pull --ff-only                # Only fast-forward (fail if diverged)
```

### Push
```bash
git push                              # Push current branch
git push <remote> <branch>            # Push specific branch
git push -u origin <branch>           # Push and set upstream tracking
git push --all                        # Push all branches
git push --tags                       # Push all tags
git push origin <local>:<remote>      # Push local branch to different remote name
git push --force-with-lease           # Safe force push (fails if remote changed)
git push --force                      # Force push (DANGEROUS — overwrites remote)
```

---

## Inspection & Comparison

### View commit history
```bash
git log                                # Full log
git log --oneline                      # Compact one-line log
git log --oneline -n 10                # Last 10 commits
git log --graph --oneline --all        # Visual branch graph
git log --author="name"                # Filter by author
git log --since="2024-01-01"           # Commits after date
git log --until="2024-12-31"           # Commits before date
git log --grep="keyword"              # Search commit messages
git log -- <file>                      # History of specific file
git log <branch1>..<branch2>           # Commits in branch2 not in branch1
git log --stat                         # Show files changed per commit
git log -p                             # Show full diffs
```

### View changes
```bash
git diff                          # Unstaged changes
git diff --staged                 # Staged changes
git diff <commit>                 # Changes since commit
git diff <branch1>..<branch2>     # Diff between branches
git diff <branch1>...<branch2>    # Changes since branches diverged
git diff --name-only              # Only file names
git diff --stat                   # Summary stats
git diff -- <file>                # Diff specific file
```

### Show commit details
```bash
git show <commit>            # Show commit details + diff
git show <commit>:<file>     # Show file at specific commit
git show HEAD                # Show latest commit
git show HEAD~2              # Show 2 commits ago
```

### Blame (line-by-line authorship)
```bash
git blame <file>                    # Who changed each line
git blame -L 10,20 <file>          # Blame specific line range
git blame -L :<function> <file>    # Blame specific function
```

### Search code
```bash
git grep "pattern"                  # Search working directory
git grep "pattern" <commit>         # Search specific commit
git grep -n "pattern"               # Show line numbers
git grep -c "pattern"               # Count matches per file
git log -S "string" --oneline       # Find commits that added/removed string (pickaxe)
git log -G "regex" --oneline        # Find commits matching regex in diff
```

---

## Undoing Changes

### Discard working directory changes
```bash
git restore <file>               # Discard changes in file
git restore .                    # Discard all changes
git checkout -- <file>           # Alternative (older syntax)
```

### Reset commits
```bash
git reset --soft HEAD~1          # Undo last commit, keep changes staged
git reset --mixed HEAD~1         # Undo last commit, keep changes unstaged (default)
git reset --hard HEAD~1          # Undo last commit, discard all changes (DANGEROUS)
git reset --hard <commit>        # Reset to specific commit (DANGEROUS)
```

### Revert (safe undo — creates new commit)
```bash
git revert <commit>              # Revert specific commit
git revert <commit> --no-edit    # Revert without editing message
git revert HEAD                  # Revert last commit
git revert <oldest>..<newest>    # Revert range of commits
```

### Recover lost commits
```bash
git reflog                       # View history of HEAD movements
git checkout <reflog-hash>       # Recover to a lost state
git branch <name> <reflog-hash>  # Create branch at lost commit
```

---

## Stashing

### Save work in progress
```bash
git stash                        # Stash tracked changes
git stash -u                     # Include untracked files
git stash -a                     # Include untracked + ignored files
git stash push -m "description"  # Stash with message
git stash push <file>            # Stash specific file
```

### Retrieve stashed work
```bash
git stash list                   # List all stashes
git stash show                   # Show latest stash summary
git stash show -p                # Show latest stash diff
git stash pop                    # Apply latest stash and remove it
git stash apply                  # Apply latest stash, keep it
git stash apply stash@{2}       # Apply specific stash
git stash drop stash@{0}        # Delete specific stash
git stash clear                  # Delete all stashes
```

---

## Tagging

### Create tags
```bash
git tag <name>                          # Lightweight tag at HEAD
git tag <name> <commit>                 # Tag specific commit
git tag -a <name> -m "message"          # Annotated tag (recommended)
git tag -a <name> <commit> -m "msg"     # Annotated tag on specific commit
```

### Manage tags
```bash
git tag                       # List all tags
git tag -l "v1.*"             # List tags matching pattern
git show <tag>                # Show tag details
git tag -d <name>             # Delete local tag
git push origin --delete <tag>  # Delete remote tag
```

### Push tags
```bash
git push origin <tag>         # Push specific tag
git push --tags               # Push all tags
git push origin --tags        # Push all tags to specific remote
```

---

## Cherry-Pick

### Apply specific commits to current branch
```bash
git cherry-pick <commit>                 # Apply single commit
git cherry-pick <commit1> <commit2>      # Apply multiple commits
git cherry-pick <start>..<end>           # Apply range (exclusive start)
git cherry-pick --no-commit <commit>     # Apply without committing
git cherry-pick --abort                  # Abort in-progress cherry-pick
git cherry-pick --continue               # Continue after conflict resolution
```

---

## Submodules

### Add and manage submodules
```bash
git submodule add <url> <path>           # Add submodule
git submodule init                       # Initialize submodules
git submodule update                     # Fetch submodule content
git submodule update --init --recursive  # Init + update all nested submodules
git submodule status                     # Show submodule status
git submodule foreach <command>          # Run command in each submodule
```

---

## Worktrees

### Manage multiple working directories
```bash
git worktree add <path> <branch>    # Create worktree for branch
git worktree add -b <new> <path>    # Create new branch in worktree
git worktree list                   # List all worktrees
git worktree remove <path>          # Remove worktree
git worktree prune                  # Clean up stale worktree refs
```

---

## Clean

### Remove untracked files
```bash
git clean -n              # Dry run (show what would be deleted)
git clean -f              # Delete untracked files
git clean -fd             # Delete untracked files and directories
git clean -fX             # Delete only ignored files
git clean -fx             # Delete untracked + ignored files
```

---

## Bisect (Binary Search for Bugs)

### Find the commit that introduced a bug
```bash
git bisect start
git bisect bad                  # Mark current commit as bad
git bisect good <commit>        # Mark known good commit
# Git checks out middle commit — test and mark:
git bisect good                 # If this commit is OK
git bisect bad                  # If this commit has the bug
# Repeat until git finds the culprit
git bisect reset                # End bisect session
```

### Automated bisect
```bash
git bisect start <bad> <good>
git bisect run <test-script>    # Auto-run script to determine good/bad
```

---

## Patches & Bundles

### Create and apply patches
```bash
git format-patch <commit>           # Create patch files since commit
git format-patch -1 <commit>        # Patch for single commit
git format-patch <branch> -o <dir>  # Output patches to directory
git am <patch-file>                 # Apply patch
git apply <patch-file>              # Apply patch without committing
git apply --check <patch-file>      # Test if patch applies cleanly
```

### Bundles (offline transfer)
```bash
git bundle create <file> <branch>          # Create bundle
git bundle create <file> --all             # Bundle entire repo
git clone <bundle-file> <directory>        # Clone from bundle
git bundle verify <file>                   # Verify bundle integrity
```

---

## GitHub CLI (gh) Operations

### Repository
```bash
gh repo create <name> --public --source=. --push   # Create and push
gh repo clone <owner/repo>                          # Clone
gh repo view <owner/repo>                           # View repo info
gh repo fork <owner/repo>                           # Fork
gh repo list <owner>                                # List user's repos
gh repo delete <owner/repo> --yes                   # Delete repo
```

### Pull Requests
```bash
gh pr create --title "title" --body "body"   # Create PR
gh pr create --fill                          # Auto-fill from commits
gh pr list                                   # List open PRs
gh pr view <number>                          # View PR details
gh pr checkout <number>                      # Check out PR branch
gh pr merge <number>                         # Merge PR
gh pr merge <number> --squash               # Squash merge
gh pr merge <number> --rebase               # Rebase merge
gh pr close <number>                         # Close PR
gh pr review <number> --approve             # Approve PR
gh pr review <number> --comment -b "msg"    # Comment on PR
gh pr diff <number>                          # View PR diff
gh pr checks <number>                        # View CI status
```

### Issues
```bash
gh issue create --title "title" --body "body"  # Create issue
gh issue list                                   # List open issues
gh issue view <number>                          # View issue
gh issue close <number>                         # Close issue
gh issue reopen <number>                        # Reopen issue
gh issue comment <number> -b "message"          # Add comment
gh issue list --label "bug"                     # Filter by label
```

### Actions / Workflows
```bash
gh run list                          # List recent workflow runs
gh run view <run-id>                 # View run details
gh run watch <run-id>                # Watch run in real time
gh run rerun <run-id>                # Re-run a workflow
gh workflow list                     # List workflows
gh workflow run <workflow> --ref <branch>  # Trigger workflow
```

### Releases
```bash
gh release create <tag> --title "title" --notes "notes"  # Create release
gh release create <tag> <files>                           # Release with assets
gh release list                                           # List releases
gh release view <tag>                                     # View release
gh release download <tag>                                 # Download assets
gh release delete <tag> --yes                             # Delete release
```

### Gists
```bash
gh gist create <file>                    # Create gist
gh gist create <file> --public           # Public gist
gh gist list                             # List gists
gh gist view <id>                        # View gist
gh gist edit <id>                        # Edit gist
```

---

## Agent Best Practices

### Before committing
1. Always run `git status` and `git diff --staged` to review changes.
2. Never commit `.env`, credentials, secrets, or large binaries.
3. Write meaningful commit messages — subject line (what), body (why).
4. Prefer staging specific files over `git add -A` to avoid accidental inclusions.

### Safe operations
- Use `git push --force-with-lease` instead of `--force`.
- Use `git revert` instead of `git reset --hard` on shared branches.
- Use `git stash` before switching branches with uncommitted work.
- Run `git fetch` before making assumptions about remote state.

### Commit message format
```
<type>: <short summary in imperative mood>

<optional body — explain why, not what>

Co-Authored-By: Agent Name <agent@example.com>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `style`, `perf`

### Conflict resolution workflow
```bash
git status                          # Identify conflicted files
# Edit files to resolve conflicts (remove <<<< ==== >>>> markers)
git add <resolved-files>            # Stage resolved files
git commit                          # Complete the merge
```

### Common recovery patterns
```bash
# Undo last commit but keep changes
git reset --soft HEAD~1

# Recover deleted branch
git reflog
git branch <name> <hash>

# Fix wrong branch (move commits)
git stash
git checkout <correct-branch>
git stash pop

# Undo a pushed commit safely
git revert <commit>
git push
```
