# Python Environments — Conda and venv

- **Document ID:** KB-PY-ENV-14
- **Status:** general technical guidance; commands must be checked against the installed Python/Conda versions
- **Applies to:** Windows 11, Python projects, VS Code, terminal workflows
- **Keywords:** Python environment, virtual environment, venv, virtualenv, Conda, Miniconda, Anaconda, pip, requirements.txt, environment.yml, interpreter, package conflict, Python ei löydy, virtuaaliympäristö, riippuvuudet

## 1. Why environments matter

A Python environment isolates a project's interpreter and installed packages from other projects. It prevents one project's dependency upgrade from unexpectedly breaking another project.

Do not install every package globally. Choose one environment strategy per project and document it.

## 2. Conda versus venv

| Topic | Conda | Python venv |
|---|---|---|
| Main purpose | Environments and packages; can manage Python and non-Python binaries | Isolates Python packages for a chosen Python interpreter |
| Package tools | `conda`, often also `pip` | `pip` |
| Strength | Useful for scientific, GPU and native-library stacks | Built into Python; lightweight and simple |
| Portability | `environment.yml` is convenient, but platform-specific packages may differ | `requirements.txt` or modern project metadata; system dependencies remain external |
| Typical use | Data science, ML, complex native dependencies | Web apps, scripts, libraries and ordinary Python services |

Do not casually mix Conda and pip. If pip is needed inside a Conda environment, install Conda packages first, then pip packages, and record the result.

## 3. Windows: create and use a venv

From the project directory in PowerShell:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip freeze > requirements-lock.txt
```

If activation is blocked by PowerShell execution policy, you can avoid activation and call the interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe your_script.py
```

Do not weaken machine-wide security policy just to activate an environment. If policy changes are necessary, understand the scope and use the narrowest permitted setting.

Deactivate an active venv with `deactivate`.

## 4. Conda workflow

Install Miniconda or another approved Conda distribution. Then:

```powershell
conda --version
conda create -n helpdesk-dev python=3.12
conda activate helpdesk-dev
python --version
python -m pip install --upgrade pip
```

Install dependencies using the project's declared method. To export:

```powershell
conda env export --from-history > environment.yml
conda env list
conda deactivate
```

To recreate:

```powershell
conda env create -f environment.yml
conda activate helpdesk-dev
```

An exported environment may contain machine-specific details. Review it before committing. Prefer a deliberate, minimal environment specification for shared projects.

## 5. VS Code interpreter selection

1. Open the project folder, not just an individual file.
2. Use **Python: Select Interpreter** from the Command Palette.
3. Select the project's `.venv\Scripts\python.exe` or the intended Conda environment.
4. Open a new terminal and verify `python --version` and `python -m pip --version`.
5. Ensure the selected interpreter matches the terminal and test runner.

The Python extension does not automatically mean a standalone system Python is installed. Check the actual interpreter path.

## 6. Common problems

### 'python' or 'py' is not recognized
Check installation, PATH and Windows app execution aliases. Try the Python launcher `py`. In VS Code, inspect the selected interpreter path.

### ModuleNotFoundError
The package may be installed into a different interpreter. Run `python -m pip show package-name` using the same interpreter that runs the application.

### pip installs into the wrong environment
Avoid bare `pip`; use `python -m pip`. Check `where.exe python` and `python -m pip --version`.

### Activate.ps1 is blocked
Use the environment's Python executable directly, or follow your organization's approved PowerShell policy. Do not run random administrator commands from forum posts.

### Conda command not found
Open the intended Conda prompt, initialize the current shell with the official Conda setup, or inspect PATH. Do not add several conflicting Python distributions to PATH blindly.

### Package conflict / incompatible Python version
Read the package's supported Python versions, architecture and platform requirements. Create a clean environment and install compatible versions. Do not repeatedly upgrade every package without diagnosing the conflict.

### Native library or GPU package fails
Check Python version, CPU architecture, CUDA/runtime compatibility, driver version and package installation instructions. GPU frameworks often require a specific combination; a successful pip install does not prove GPU support.

## 7. Good project practices

- Keep `.venv/`, Conda caches and local secrets out of Git.
- Commit dependency declarations and lock files where appropriate.
- Record the supported Python version.
- Use `python -m pip` consistently.
- Recreate the environment from declarations to test reproducibility.
- Never put API keys or passwords in `requirements.txt` or `environment.yml`.

## 8. AI HelpDesk relevance

The backend is a Python/FastAPI service, but it normally runs in Docker in the project workflow. A local venv is useful for editor support, linting and isolated tests; it does not replace the Compose runtime. Verify the current Dockerfile and dependency files before choosing a Python version or installing packages locally.


## Tiivistelmä suomeksi

Pythonin virtuaaliympäristö eristää projektin Python-tulkin ja paketit muista projekteista. venv kuuluu Pythonin standardikirjastoon ja sopii hyvin pip-pohjaisiin projekteihin. Conda hallitsee ympäristöjen lisäksi myös muita kuin Python-paketteja ja on hyödyllinen esimerkiksi data- ja GPU-työnkuluissa. Aktivoi oikea ympäristö ennen asennusta ja varmista tulkin polku komennolla python -c "import sys; print(sys.executable)". Älä sekoita ympäristöjen paketteja huomaamatta.
