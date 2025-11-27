# HOW TO REVERT IF SOMETHING BREAKS

## Quick Revert (Local Backup)
The working version without raindrops is saved locally:
```
C:\Users\krista-showputer\Desktop\liquid-milk-balls-web\mirrors-echo-fixed-BACKUP-WORKING.html
```

To restore it:
```powershell
cd C:\Users\krista-showputer\Desktop\liquid-milk-balls-web
copy mirrors-echo-fixed-BACKUP-WORKING.html mirrors-echo-fixed.html
git add mirrors-echo-fixed.html
git commit -m "Revert to backup working version"
git push
```

## Git Revert (Any Previous Commit)
See all commits:
```powershell
git log --oneline -10
```

Revert to a specific commit:
```powershell
git revert <commit-hash>
git push
```

## Key Commits to Know:
- `d734f0c` - Added raindrops + 10min disconnect (CURRENT)
- `bf02714` - Simple working version (before raindrops)
- `c9f1497` - Fixed existing participant detection
- `687d57e` - Added /api/ endpoints

## Emergency: Full Reset to Working State
```powershell
git checkout bf02714 -- mirrors-echo-fixed.html
git commit -m "Emergency revert to working version"
git push
```
