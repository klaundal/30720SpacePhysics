# 30720 Space Physics

Notebooks and supporting Python code for the DTU Space course **30720 Space Physics**.

The notebooks under `notebooks/` are the clean course versions. During setup they are copied to `student_work/`, which is where students should write their answers and code.

## How the notebooks work

The course material is provided as Jupyter notebooks (`.ipynb` files). A notebook combines explanatory text, Python code cells, figures, and results in one document. You open and edit it in JupyterLab, which runs in a web browser.

The browser is only the user interface. The Python code can run either on a remote computer or on your own computer:

|                              | VirES VRE                              | Local computer                         |
|------------------------------|----------------------------------------|----------------------------------------|
| Where the code runs          | On a remote VirES server               | On your own computer                   |
| Software                     | Already installed                      | Installed from `environment.yml`       |
| Where your notebooks are kept | In your VRE account                   | On your own disk                       |
| Internet connection          | Required                               | Required when accessing online data    |

The notebook looks and behaves almost identically in both cases.

## Option 1: VirES VRE (recommended)

The simplest option is to use the VirES Virtual Research Environment (VRE), where JupyterLab and the scientific Python packages are already installed. Nothing needs to be installed on your own computer, but your notebooks run and are stored on the remote service.

1. [Create a free VirES account](https://vires.services/oauth/accounts/signup/) and accept the ESA data and VirES service terms.
2. [Log in to the VirES VRE](https://vre.vires.services/).
3. In JupyterLab, open a terminal using **File → New → Terminal**.

Then follow the getting-started instructions below in that terminal.

## Option 2: your own computer

You can instead run JupyterLab locally. It still opens in your browser, but Python runs on your computer and the notebooks remain on your own disk. This requires a local Python environment, described below, but gives you control of the installed software and files.

## Getting started

Open a terminal, either in the VirES VRE or on your own computer, and clone the course repository:

```bash
git clone https://github.com/klaundal/30720SpacePhysics
cd 30720SpacePhysics
```

### Local Python environment

Skip this section when using the VRE. With [Miniforge](https://github.com/conda-forge/miniforge) installed, create and activate the local course environment:

```bash
mamba env create -f environment.yml
mamba activate spacephysics
```

If `environment.yml` changes later, update it with `mamba env update -f environment.yml --prune`.

If activation is not configured, run `mamba shell init -s zsh` on macOS, `mamba shell init -s bash` on Linux, or `mamba shell init -s powershell` in Windows PowerShell. Restart the terminal afterwards.

Prepare the editable notebook copies:

```bash
python update_course.py
```

If the `python` command is not available, try `py` on Windows or `python3` on macOS/Linux. If you are working locally, start JupyterLab:

```bash
jupyter lab
```

In the VRE, return to the JupyterLab file browser after running the update script. Open:

```text
student_work/00_getting_started.ipynb
```

> **Only edit notebooks in `student_work/`.** The notebooks in `notebooks/` are clean originals and may be updated during the course.

## Updating the course material

Before class, run this command from the repository directory:

```bash
python update_course.py
```

The update script performs two operations:

1. It downloads the latest course material from GitHub.
2. It copies newly released notebooks into `student_work/`.

An existing file in `student_work/` is **never overwritten**. This means that an update will not remove answers or code already written by a student.

## Back up your work

The `student_work/` directory is ignored by Git and is not backed up by this repository. Copy important work out of the VRE regularly, or keep a local copy of the repository in a backed-up Dropbox or Drive folder.

## Repository layout

```text
notebooks/               Clean notebooks
notebooks/course_tools/  Imported helper code
student_work/            Editable student copies; created locally and ignored by Git
scripts/                 Small scripts used to prepare the student workspace
update_course.py         Downloads updates and prepares newly released notebooks
environment.yml          Packages needed to run the notebooks locally
```
