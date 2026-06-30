# Locked GLB asset repository

This folder contains GLB assets that can be locked before publishing to GitHub. The lock keeps the file names visible while making the committed binary content unreadable without the password.

## Test lock created

The following files were encrypted for testing with the temporary password `testpass`:

- `winlose_khan.glb` -> `winlose_khan.glb.enc`
- `winlose_bgj.glb` -> `winlose_bgj.glb.enc`

The original `.glb` files were not removed. For real use, delete the test `.enc` files and re-run encryption with your own password.

## File list

Edit `private-files.txt` and put one file name per line:

```text
winlose_khan.glb
winlose_bgj.glb
```

## Manual encryption

From PowerShell:

```powershell
$env:PRIVATE_IMAGE_PASSWORD = "your-real-password"
powershell -ExecutionPolicy Bypass -File C:\Discovery\Cosmo\dev\lab\utility\card\protect-private-images.ps1 -ListPath .\private-files.txt -RootPath .
```

This creates `.enc` files next to the originals. Use `-RemoveOriginal` only when you have verified the encrypted files and have a backup.

## Manual decryption

```powershell
$env:PRIVATE_IMAGE_PASSWORD = "your-real-password"
powershell -ExecutionPolicy Bypass -File C:\Discovery\Cosmo\dev\lab\utility\card\protect-private-images.ps1 -Mode Decrypt -ListPath .\private-files.txt -RootPath .
```

## Git locked workflow

For local files to remain openable while GitHub receives encrypted bytes, use a Git clean/smudge filter. In that workflow:

- Local checkout: normal `.glb` files open in local tools.
- Git index and GitHub: encrypted bytes are stored under the same file names.
- Password holders: checkout/pull can smudge the files back into readable GLB files.

Setup commands from a repository root:

```powershell
powershell -ExecutionPolicy Bypass -File C:\Discovery\Cosmo\dev\lab\utility\card\setup-private-image-git-filter.ps1 -ListPath .\private-files.txt
$env:PRIVATE_IMAGE_PASSWORD = "your-real-password"
git add --renormalize .
git commit -m "Lock private GLB assets"
git push
```

Do not commit your password. Keep it in your shell environment, password manager, or CI secret store.
