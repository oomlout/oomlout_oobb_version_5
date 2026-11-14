# Replacing a refreshed catalogue's Git history

This is the final publication phase of the [catalogue refresh](CATALOGUE_REFRESH.md).
It is documentation, not an instruction to reset any repository now. Finish the
code repairs, full requested regeneration, README/navigation update and validation
before using it. A normal README/render update after adoption uses an ordinary
commit and push; do not reset history on every build.

The intended result is a new root commit containing the reviewed current tree.
This is not an ordinary rebase, not a deletion of the GitHub repository, and not
deletion of the production source. A root commit has no parent; `commit-tree`
can create one by omitting parent arguments. See the
[Git commit-tree manual](https://git-scm.com/docs/git-commit-tree).

## 1. Establish the exact scope

Record the repository, target branch, push destination, old local HEAD and observed
remote branch SHA. Confirm whether old remote branches and tags are also in the
authorized reset scope. Resetting `main` alone does not remove history retained by
another branch/tag. Release attachments, Git LFS storage, forks, submodules and
GitHub pull-request refs are separate from the ordinary branch history.

An existing user instruction to reset and push this named repository is sufficient;
do not ask for repeated confirmation. A request merely to document the procedure
does not authorize executing it. Do not assume an absent remote URL, create a new
GitHub repository or disable branch protection to make a command succeed.

The snippets below are deliberately separate checkpoints. Replace the repository
placeholder before use. Do not concatenate the whole document into a batch script.
Commands after a failed check must not continue.

## 2. Baseline and recovery location

Use one PowerShell session for these variables and helper. The helper checks native
Git exit codes; PowerShell's error preference alone does not reliably do that.

```powershell
$ErrorActionPreference = 'Stop'
$repoPath = (Resolve-Path -LiteralPath 'C:/gh/REPLACE_WITH_APPROVED_REPOSITORY').Path
$branchName = 'main' # Replace with the actual authorized branch.
$branchRef = "refs/heads/$branchName"

function Invoke-RepoGit {
    & git -C $repoPath @args
    if ($LASTEXITCODE -ne 0) {
        throw "Git failed with exit code $LASTEXITCODE"
    }
}

$topLevel = (Invoke-RepoGit rev-parse --show-toplevel | Out-String).Trim()
if ((Resolve-Path -LiteralPath $topLevel).Path -ne $repoPath) {
    throw 'The selected path is not this repository root'
}
$currentRef = (Invoke-RepoGit symbolic-ref HEAD | Out-String).Trim()
if ($currentRef -ne $branchRef) {
    throw 'Review the current branch before proceeding; do not switch blindly'
}
$oldHead = (Invoke-RepoGit rev-parse HEAD | Out-String).Trim()
$pushUrl = (Invoke-RepoGit remote get-url --push origin | Out-String).Trim()
Invoke-RepoGit remote -v
Invoke-RepoGit worktree list --porcelain
Invoke-RepoGit status --short --untracked-files=all
Invoke-RepoGit for-each-ref --format='%(refname) %(objectname)'

$repoName = Split-Path -Leaf $repoPath
$stamp = Get-Date -Format 'yyyy-MM-dd_HHmmss'
$recoveryPath = Join-Path 'C:/gh/_repository_recovery' "${repoName}_${stamp}"
if (Test-Path -LiteralPath $recoveryPath) { throw 'Recovery path already exists' }
New-Item -ItemType Directory -Path $recoveryPath | Out-Null
```

Verify that the resolved recovery directory is outside the source repository and
has sufficient free space. Do not repurpose system variables such as `$HOME`.
If the checkout is a linked worktree, inspect its shared Git directory and other
worktrees before any reference cleanup or garbage collection. Do not delete `.git`.

Inspect all configured push URLs, not only the first. If `origin` pushes to multiple
destinations, resolve the intended destination before using the publication snippet.
Record remote branches and tags from the verified push endpoint:

```powershell
$remoteLine = @(Invoke-RepoGit ls-remote --refs $pushUrl $branchRef)
if ($remoteLine.Count -ne 1) { throw 'Expected exactly one existing remote branch' }
$oldRemote = ($remoteLine[0] -split '\s+')[0]
Invoke-RepoGit ls-remote --heads --tags $pushUrl |
    Set-Content -LiteralPath (Join-Path $recoveryPath 'remote-refs-before.txt') -Encoding utf8
Invoke-RepoGit for-each-ref --format='%(refname) %(objectname)' |
    Set-Content -LiteralPath (Join-Path $recoveryPath 'local-refs-before.txt') -Encoding utf8
Invoke-RepoGit status --porcelain=v1 --untracked-files=all |
    Set-Content -LiteralPath (Join-Path $recoveryPath 'status-before.txt') -Encoding utf8
@{ repository=$repoPath; branch=$branchRef; local_head=$oldHead;
   remote_head=$oldRemote; push_url=$pushUrl } |
    ConvertTo-Json |
    Set-Content -LiteralPath (Join-Path $recoveryPath 'baseline.json') -Encoding utf8
```

Fetch the reviewed remote refs before bundling so remote-only work is preserved
and inspected. Do not merely overwrite newer remote work with an older local tree.
If HEAD and the remote differ, review both directions and reconcile the intended
final source state before continuing. Capture the explicit remote SHA once that
state is understood; keep it unchanged as the publication lease.

For the usual single-remote case, the inspection commands are:

```powershell
Invoke-RepoGit fetch origin
Invoke-RepoGit log --left-right --oneline "${branchRef}...refs/remotes/origin/${branchName}"
```

If fetch and push URLs point to different repositories, inspect the actual push
endpoint's refs explicitly instead. Do not assume `origin/main` represents it.

## 3. Preserve both history and uncommitted work

Create a self-contained bundle of all relevant local refs and verify it. A bundle
does not substitute for backing up the working directory, index state, configuration
or other local material. The distinction and verification command are described in
the [Git bundle manual](https://git-scm.com/docs/git-bundle).

```powershell
$bundlePath = Join-Path $recoveryPath 'before-history-reset.bundle'
Invoke-RepoGit bundle create $bundlePath --all
Invoke-RepoGit bundle verify $bundlePath
Invoke-RepoGit bundle list-heads $bundlePath

$unstagedPatch = Join-Path $recoveryPath 'unstaged.patch'
$stagedPatch = Join-Path $recoveryPath 'staged.patch'
Invoke-RepoGit diff --binary "--output=$unstagedPatch"
Invoke-RepoGit diff --cached --binary "--output=$stagedPatch"
```

Use Git's own patch output option; do not pipe binary patch content through an
encoding-changing PowerShell text redirection. Separately copy and hash untracked
source files, required ignored files and any uncommitted submodule work. Record
stash entries and preserve the required stash data explicitly before clearing any
ref. Retain local configuration/hooks privately when needed for recovery; do not
publish those backups. Bundle refs alone do not back up LFS payloads or submodule
repositories. Handle those separately if present.

For a dirty repository, classify every change: incorporate it as intended work,
preserve it separately, or leave it untouched and isolate the refresh. Never erase
unrelated work to get a clean status. The audited bearing-holder, gear and pulley
repositories already had local changes when this plan was written.

If archival/regeneration can remove worktree files, the hashed worktree backup must
exist before that step, not just before the final Git reset. The bundle here may
be created at the start of the refresh and verified again before publication.

## 4. Finish and review the new tree

All of the main workflow's acceptance checks must pass. Review every staged path,
including deletions. Ignore/cache policy must already be implemented. `.gitignore`
alone does not untrack a historical cache or archive.

Stage an explicitly reviewed path list. The following is illustrative; replace it
with the actual changed files and intended generated directories. Do not use
`git add -A` across a dirty project without deciding the scope of every change.

```powershell
$reviewedPaths = @(
    '.gitignore', '.gitattributes', 'README.md',
    'parts', 'navigation_oobb', 'presentation'
    # Add the exact repaired scripts, source definitions and tests for this project.
)
Invoke-RepoGit add -A -- @reviewedPaths
Invoke-RepoGit diff --cached --check
Invoke-RepoGit diff --cached --stat
Invoke-RepoGit diff --cached --name-status
```

Review source-code changes and representative generated pages. Confirm that only
final production files and necessary provenance are published. Check that copied
navigation assets, raw renders, archives and dependency environments are absent
from the intended tree. Use the actual project exclusions, not filename guesses.

```powershell
$unexpected = @(Invoke-RepoGit ls-files -- .archives build .venv .dependencies)
if ($unexpected.Count -ne 0) { throw 'Unwanted generated/recovery paths are tracked' }
Invoke-RepoGit diff --quiet
$untracked = @(Invoke-RepoGit ls-files --others --exclude-standard)
if ($untracked.Count -ne 0) { throw 'Resolve remaining untracked files before resetting history' }
$tree = (Invoke-RepoGit write-tree | Out-String).Trim()
```

`diff --quiet` must pass for tracked unstaged changes; staged changes are expected.
Do not silence remaining work by broadly ignoring source files. Confirm the staged
tree contains all repaired code as well as generated files. Check blob bytes against
any artifact/source hash manifests after Git attributes have been applied.

`commit-tree` does not run ordinary commit hooks. Run required project validation
and hook-equivalent checks explicitly. Preserve the configured author identity;
use the required signing option if this repository requires signed commits.

## 5. Create the parentless commit

Record a useful initial-commit message covering the resulting catalogue, not a
transcript of the migration. There is no need to commit the temporary old tree first.

```powershell
$newRoot = (Invoke-RepoGit commit-tree $tree -m 'Rebuild catalogue with folder navigation and studio renders' |
    Out-String).Trim()
$parents = (Invoke-RepoGit show -s --format=%P $newRoot | Out-String).Trim()
if ($parents) { throw 'New commit unexpectedly has parents' }
$newCount = (Invoke-RepoGit rev-list --count $newRoot | Out-String).Trim()
if ($newCount -ne '1') { throw 'New history is not a single root commit' }

Invoke-RepoGit update-ref $branchRef $newRoot $oldHead
$newRoot | Set-Content -LiteralPath (Join-Path $recoveryPath 'new-root.txt') -Encoding utf8
Invoke-RepoGit status --short
Invoke-RepoGit log -1 --format='%H %P %s'
```

The expected-old-value check prevents replacing a local branch that changed while
the migration was being prepared. Because the commit uses the reviewed index tree,
the intended tracked files remain in place; no `reset --hard` or `.git` removal is
needed. If a check fails, investigate rather than bypassing it.

If intentional commits were added during the refresh after recording `$oldHead`,
review them, recreate/verify a current recovery bundle under a new filename, and
record the actual current branch SHA before `update-ref`. Do not bypass its
expected-old-value check to compensate for a stale baseline.

## 6. Publish with an exact remote lease

Verify the push URL is still the one reviewed earlier. Push only the intended
branch with the old remote SHA captured before publication. An explicit lease
rejects the update if that remote ref has changed; see the
[Git push manual](https://git-scm.com/docs/git-push).

```powershell
$currentPushUrl = (Invoke-RepoGit remote get-url --push origin | Out-String).Trim()
if ($currentPushUrl -ne $pushUrl) { throw 'Push destination changed' }
Invoke-RepoGit push "--force-with-lease=${branchRef}:${oldRemote}" origin "${newRoot}:${branchRef}"
$published = @(Invoke-RepoGit ls-remote --refs $pushUrl $branchRef)
if ($published.Count -ne 1 -or ($published[0] -split '\s+')[0] -ne $newRoot) {
    throw 'Remote verification did not find the new root'
}
```

Do not replace the captured SHA with a freshly fetched value merely to overcome
a rejected lease. Inspect the intervening remote changes and reconcile them first.
Do not use an unqualified `--force`, `--mirror`, or a push that updates every branch.
If protection or access rules reject the operation, report the concrete blocker;
do not silently weaken those rules or claim the reset was published.

## 7. Verify an independent clone

Clone from the verified remote, not the local worktree, into a new recovery-area
directory. Do not use `--depth 1` to prove that the actual published history is one
commit: shallow cloning would hide the history being measured.

```powershell
$clonePath = Join-Path $recoveryPath 'fresh-clone-check'
if (Test-Path -LiteralPath $clonePath) { throw 'Clone destination already exists' }
& git clone --branch $branchName $pushUrl $clonePath
if ($LASTEXITCODE -ne 0) { throw 'Fresh clone failed' }
& git -C $clonePath rev-list --count HEAD
if ($LASTEXITCODE -ne 0) { throw 'Clone history check failed' }
& git -C $clonePath log -1 --format='%H %P'
if ($LASTEXITCODE -ne 0) { throw 'Clone commit check failed' }
& git -C $clonePath status --short
if ($LASTEXITCODE -ne 0) { throw 'Clone status check failed' }
```

Require the expected root SHA, no parents and a count of one on the reset branch.
Run the adapted source/image/hash/link audit in this clone. Source dependencies
must be documented for builds; existing published images and links must already
work without the original ignored build cache. Inspect the live GitHub root,
folder-based discovery and a representative canonical part folder.

If all branch/tag history was meant to be replaced, also inspect every fetched ref
and `git rev-list --all --count`. A one-commit `HEAD` is not proof that other branches
or tags no longer retain old commits. Resolve retained refs according to the scope
recorded in section 1; do not delete unrelated release tags automatically.

## 8. Reclaim local Git storage after successful publication

Keep the verified external bundle. Retaining a backup branch/tag in the same
repository defeats local compaction because its old objects stay reachable.
Inspect local heads, remote-tracking refs, tags, stash, tool snapshot refs such as
`refs/codex`, and all worktrees. Decide exactly which old references may be removed.

For an individually reviewed obsolete local ref, the command shape is:

```text
git -C <repository> update-ref -d <exact-ref-name> <recorded-old-object-id>
```

Use actual recorded values, not a loop that deletes all refs. Update stale remote
tracking state from the verified remote. Remove a remote branch/tag only when it
was specifically included in the reset scope, with its own recorded old SHA and
explicit lease; do not push backup refs back to the cleaned remote.

Only after the ref audit and recovery verification, and with no Git-writing process
running against this repository or its worktrees, compact local unreachable history:

```powershell
Invoke-RepoGit reflog expire --expire=now --all
Invoke-RepoGit gc --prune=now
Invoke-RepoGit count-objects -v
Invoke-RepoGit for-each-ref --format='%(refname) %(objectname)'
Invoke-RepoGit rev-list --all --count
```

Immediate pruning removes the ordinary recovery grace period and can race with
concurrent writers. The [Git gc manual](https://git-scm.com/docs/git-gc) describes
that constraint. If an IDE/tool keeps creating snapshots or cannot be quiesced,
use the verified fresh clone as the compact checkout and retain the old checkout
as an explicitly measured backup until its disposition is decided. Do not delete
shared Git directories or active worktrees to force a smaller number.

## 9. Recovery and failure handling

| Failure | Response |
| --- | --- |
| Build/audit fails | Repair the source/generator and rerun affected work; keep old history intact |
| Bundle fails verification | Repair recovery before updating refs or removing files |
| Local `update-ref` rejects old SHA | Review concurrent local changes; do not force past the mismatch |
| Remote lease is rejected | Review remote changes; preserve and integrate their intended content |
| Push denied by access/protection | Keep the reviewed local result; report the exact unresolved publication step |
| Fresh-clone hashes differ | Inspect attributes/normalization and manifests; correct the published tree |
| `.git` remains large | Inspect retaining refs, reflogs, shared worktrees and packs; measure a real fresh clone |
| Filesystem cleanup blocked | Retain the files and report their size; do not evade the block |

The first recovery action is an independent clone of the verified bundle:

```text
git clone --branch <old-branch-name> <verified-bundle-path> <new-recovery-directory>
```

Restore backed-up working files/patches into that recovery clone as needed. Inspect
the result before moving any branch. Before publication, the local branch can be
restored using `update-ref <branch> <old-head> <new-root>` if that reversal is intended;
the current files/index remain and must be reconciled deliberately. After publication,
restoring old remote history is itself a history rewrite: only do it within the
authorized recovery scope and with a lease expecting the published new SHA.

## 10. Completion report and later work

Report the new root commit, verified remote, active part/render counts, passed
checks, preserved recovery paths and before/after sizes. Distinguish clean-clone
size from the local folder with archives, caches and any external verification
clone. Account for the recovery bundle's own bytes. Do not claim GitHub immediately
deleted every unreachable historical object or release attachment.

Other developers should normally use a fresh clone after this reset, preserving
their local work first. Continuing ordinary work produces subsequent commits;
that is expected. The reset establishes a new baseline, not a permanent rule that
every future repository state must contain exactly one commit.

## 11. A folder without Git

For a project such as the audited timing-belt-storage folder, there is no existing
history to erase. Preserve its files, complete the same build/documentation audits,
then initialize Git only if repository creation/publication is in the authorized
scope. Configure the actual intended remote; do not guess it from the directory name.
Create an ordinary initial commit and push normally to an empty remote. If the
destination already has history, inspect it and use the relevant preservation and
lease procedure instead of treating it as empty.
