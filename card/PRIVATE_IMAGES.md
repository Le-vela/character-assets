# Private image encryption

`private-images.txt` lists image file names that should be encrypted.
The script searches the selected root folder recursively, so the file can be
inside any subfolder.

## Encrypt

```powershell
powershell -ExecutionPolicy Bypass -File .\protect-private-images.ps1
```

This creates encrypted files next to the originals with `.enc` added.
Original files are kept by default.

To remove the original files after encrypted copies are created:

```powershell
powershell -ExecutionPolicy Bypass -File .\protect-private-images.ps1 -RemoveOriginal
```

## Decrypt

```powershell
powershell -ExecutionPolicy Bypass -File .\protect-private-images.ps1 -Mode Decrypt
```

To remove the encrypted files after restored copies are created:

```powershell
powershell -ExecutionPolicy Bypass -File .\protect-private-images.ps1 -Mode Decrypt -RemoveOriginal
```

## Notes

- Put one file name per line in `private-images.txt`.
- Lines starting with `#` are ignored.
- The password is requested each time and is not saved.
- For automation, set `PRIVATE_IMAGE_PASSWORD` before running the script.
- If the same file name exists in multiple folders, every match is processed.

## Git locked images

Use the Git filter when local files should stay openable, but committed and
pushed files should be encrypted under the same file name.

1. Add file names to `private-images.txt`.
2. Install or refresh the local Git filter:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-private-image-git-filter.ps1
```

3. Set the password in the shell before using Git:

```powershell
$env:PRIVATE_IMAGE_PASSWORD = "your-password"
```

4. Re-add files so Git stores encrypted bytes:

```powershell
git add --renormalize .
git commit -m "Lock private images"
git push
```

After this, your local checkout is decrypted by the same password, but GitHub
receives encrypted bytes. The file name still appears, but GitHub cannot preview
the image format or contents.
