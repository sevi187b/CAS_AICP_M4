# CAS AICP M4: Notes

Notes from chats with Claude, grouped by notebook. Type `+++` in the chat to add to them.

## 01-Images_as_arrays.ipynb

### Reading images with `imread` (2026-10-27)

- `import imageio.v3 as iio`, then `iio.imread('path')` returns the image as a NumPy array.
- Other libraries have their own `imread`. The prefix tells you which one is being used:
  - `skimage.io.imread`: mostly uses imageio internally, returns the same kind of array
  - `imageio.v2.imread`: the older imageio interface (legacy)
  - `matplotlib.pyplot.imread`, `cv2.imread` (OpenCV)
- ⚠️ `cv2.imread` returns colors in **BGR** order, not RGB.

### Image shape (2026-10-27)

`im_cats.shape` → `(2448, 3264, 3)`:

| Axis | Size | Meaning |
| --- | --- | --- |
| 0 | 2448 | rows = height |
| 1 | 3264 | columns = width |
| 2 | 3 | channels (R, G, B) |

- Pixel count = 2448 × 3264 ≈ 8 megapixels. With 3 values per pixel that's ≈ 24 million numbers.
- ⚠️ Height comes first: `im_cats[100, 200]` is row 100, column 200 (y=100, x=200).
- `im_cats[:, :, 0]` is the red channel on its own.
- Grayscale images have no channel axis: `(height, width)`. PNGs with transparency have 4 channels (RGBA).

### `np.mean` on an image (2026-10-27)

- Without `axis`, it averages every value (all pixels, all channels) and returns one number from 0 to 255: the overall brightness.
- It shows that images are just arrays, so any NumPy function works on them.
- `axis` chooses which axes get averaged away:

```python
np.mean(im_cats)               # 1 number: overall brightness
np.mean(im_cats, axis=(0, 1))  # 3 numbers: average R, G, B (the average color)
np.mean(im_cats, axis=2)       # shape (2448, 3264): channels averaged per pixel ≈ grayscale
```

- The result is a float even though the image is `uint8`. No overflow problem.

### Displaying the average color (2026-10-27)

```python
avg_color = np.mean(im_cats, axis=(0, 1))     # 3 values: mean R, G, B
swatch = np.full((100, 100, 3), avg_color)    # 100x100 image filled with that color
plt.imshow(swatch.astype(np.uint8));
```

- `np.full(shape, value)` creates a new array of that shape with every position set to `value`. Related: `np.zeros`, `np.ones`.
- Here the value is 3 numbers. The last axis also has size 3, so NumPy copies `[R, G, B]` into every pixel. This is called **broadcasting**; the sizes must line up from the right.
- `.astype(np.uint8)` returns a converted **copy** with whole numbers from 0 to 255. It **truncates**: 123.9 → 123.
- ⚠️ `plt.imshow` reads integers as 0–255 but floats as 0–1, and clips anything above 1. A float swatch without conversion comes out nearly white. `plt.imshow(swatch / 255)` also works.
- The `;` at the end is a Jupyter trick: it hides the `<matplotlib.image.AxesImage ...>` text output.
- The average color of a photo is usually a dull brown or gray. That's normal.

## General

### Marking things in a notebook (2026-10-27)

- In code: a tagged comment such as `# QUESTION: ...`. Find all of them with Ctrl+F.
- A markdown heading such as `### ❓ Question: ...` shows up in VS Code's **Outline** panel.
- Red text: `<span style="color:red">text</span>` works in VS Code and Jupyter, but not on GitHub. `$\color{red}{\text{text}}$` works on GitHub too (in a math font).
- Emoji on Windows: **Win + .** opens the emoji picker. Codes like `:warning:` don't work in notebooks.

### Notes setup with Claude (2026-10-27)

- `CLAUDE.md` in the repo is loaded automatically in every Claude session, on any machine. It explains the `+++` shortcut and the format of these notes.
- Claude reads `NOTES.md` only when adding to it or when I refer to something discussed earlier. To load it in every session instead, add a line `@NOTES.md` to `CLAUDE.md`.
- Claude Code keeps past chat sessions only on the machine where they happened. These notes are the way to carry things across machines (OneDrive syncs them).

### Making the GitHub repo private (2026-10-27)

- My repo `sevi187b/CAS_AICP_M4` is a **public fork** of the teacher's repo. ⚠️ GitHub doesn't allow forks of public repos to be made private.
- Options:
  1. **New private repo** (recommended): create an empty private repo on GitHub (no README, .gitignore or license), then:

     ```bash
     git remote set-url origin https://github.com/sevi187b/<new-name>.git
     git push -u origin main
     ```

     The `upstream` remote stays, so teacher updates still work with `git pull upstream main`. Afterwards the old fork can be deleted under **Settings → Danger Zone**.
  2. Ask GitHub Support to detach the fork, then make it private.
  3. Keep it public and add `NOTES.md` to `.gitignore`. OneDrive still syncs it, but there's no GitHub backup.

### Broken venv: "uv trampoline failed to spawn Python" (2026-10-30)

- Symptom: VS Code asks to install `ipykernel` and shows a strange version ("Python 3.13.-1"). Running `.venv\Scripts\python.exe` fails with `uv trampoline failed to spawn Python child process`.
- Cause: OneDrive had synced `.venv` from my other machine. A venv stores the **absolute path** of the Python it was built from (see `home = ...` in `.venv\pyvenv.cfg`). Here that was `C:\Users\station.plus\...`, which doesn't exist on this machine.
- ⚠️ A venv only works on the machine that created it, so it must not be synced. Machines share `pyproject.toml` and `uv.lock` (tracked by git), and each one builds its own venv with `uv sync`.
- uv venvs have no `pip`. Add packages with `uv add <pkg>`.
- Git ignores `.venv` already, because uv puts a `.gitignore` containing `*` inside it. Check with `git status --ignored` (`!!` = ignored). OneDrive ignores nothing and syncs every file in the folder.

**Fix:** keep the venv outside OneDrive. Do this once per machine, in the project folder:

```powershell
# Windows (PowerShell)
[Environment]::SetEnvironmentVariable("UV_PROJECT_ENVIRONMENT", "$env:LOCALAPPDATA\uv-venvs\cas-aicp-m4", "User")  # permanent
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\uv-venvs\cas-aicp-m4"  # current window
uv sync
```

```bash
# macOS/Linux: add to ~/.zshrc or ~/.bashrc
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/cas-aicp-m4"
# then: source ~/.zshrc && uv sync
```

- Then restart VS Code completely. It only reads environment variables at startup.
- **Select Kernel → Python Environments**, or choose **Enter interpreter path**:
  - Windows: `C:\Users\sevi\AppData\Local\uv-venvs\cas-aicp-m4\Scripts\python.exe`
  - macOS: `~/.venvs/cas-aicp-m4/bin/python`
- Done on this Windows machine (2026-10-30). ⚠️ Still to do on the other machine.

## ❓ Questions for teacher

None yet.
