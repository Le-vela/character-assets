# character-assets

This repository stores character asset files. Some large GLB assets are locked before publishing so their file names remain visible on GitHub, but their binary contents cannot be previewed or opened without the password.

## Locked GLB files

The current locked test targets are listed in:

```text
animation_model/3motion_versus_cooking_glb/private-files.txt
```

Current entries:

```text
winlose_khan.glb
winlose_bgj.glb
```

## How the lock works

This repository uses a Git clean/smudge filter:

- In a local checkout with the password, `.glb` files stay readable and can be opened normally.
- During `git add`, Git stores encrypted bytes in the index.
- On GitHub, the same `.glb` file names are visible, but the contents are locked and cannot be previewed as GLB assets.
- During checkout or pull, the smudge filter restores readable local files when `PRIVATE_IMAGE_PASSWORD` is set.

The password is never committed. Keep it in your shell environment, password manager, or CI secret store.

## One-time setup on a local clone

Run this from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-private-image-git-filter.ps1 -ListPath .\animation_model\3motion_versus_cooking_glb\private-files.txt
$env:PRIVATE_IMAGE_PASSWORD = "your-password"
git add --renormalize .
```

## Commit and push

```powershell
$env:PRIVATE_IMAGE_PASSWORD = "your-password"
git add .
git commit -m "Lock private GLB assets"
git push
```

## Manual `.enc` backup mode

For a manual encrypted copy next to the original file, use:

```powershell
$env:PRIVATE_IMAGE_PASSWORD = "your-password"
powershell -ExecutionPolicy Bypass -File .\protect-private-images.ps1 -ListPath .\animation_model\3motion_versus_cooking_glb\private-files.txt -RootPath .\animation_model\3motion_versus_cooking_glb
```

This creates `.enc` files next to originals. `.enc` files are ignored by default in this repository.
