"""Build phlex-first-steps.ipynb from the cell list below.

Edit the cells here, not in the notebook, then regenerate (needs nbformat):

    python3 build_nb.py                  # writes phlex-first-steps.ipynb next to this script
    python3 build_nb.py other/path.ipynb
"""

import pathlib
import sys

import nbformat as nbf

cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))


def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip("\n")))


def xkcd(num, file, title, caption):
    md(f"""
> 😂 **[xkcd {num}: {title}](https://xkcd.com/{num}/)**. {caption}
>
> <img src="figures/xkcd/{file}.png" alt="xkcd {num}: {title}" width="420">
>
> <small>By Randall Munroe, [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/).</small>
""")


# ---------------------------------------------------------------- intro
md("""
# First steps with Phlex: terminal, GitHub, build, run, share

This hands-on session comes straight after Kyle Knoepfel's introduction to frameworks and Phlex.
Kyle's lecture told you *what* Phlex is. Here you **use** it for the first time, and you practise
the everyday skills that working on DUNE software needs:

- working in a **terminal**
- getting code from **GitHub**, and sending your changes back with a **pull request**
- **building** C++ code with CMake
- **running** a Phlex job and reading what it tells you
- **writing things down**: a personal notes file, a README for other people, clear commit messages
- **reviewing** someone else's work

You don't need to know any of this already. Later sessions go deeper into Phlex (the GausHitFinder
migration and its tests). This one is about getting comfortable.

> 📦 **The code you'll use today** is **[nuRiceLab/phlex-india-sandbox](https://github.com/nuRiceLab/phlex-india-sandbox)**,
> a **trimmed copy** of the official **[Framework-R-D/phlex-examples](https://github.com/Framework-R-D/phlex-examples)**.
> We kept only the simplest examples, added a small CMake practice project, and made it a place
> where you're allowed to push and practise. At the end you'll move on to the official repository,
> which has much more.

## You don't have to finish everything

The session is a ladder. Climb as high as you can; everyone should reach rung 1.

| Rung | What you'll have done |
|---|---|
| **1** | Opened a pull request (in the browser if your terminal gives you trouble) and commented on someone else's |
| **2** | Built and run Phlex, changed a workflow, committed and pushed it from the terminal |
| **3** | Added your own C++ algorithm and answered a review with a second commit |

You have a folded **card** on your desk. Write your name and GitHub username on both sides.
Turn the **? red** side to the front when you're stuck, and a helper will come over. Keep the
**✓ green** side to the front when you're fine.

## The plan

| Part | Time | |
|---|---|---|
| 0 | 15 min | The terminal, and your notes file |
| 1 | 15 min | Getting the code with GitHub |
| 2 | 25 min | Building with CMake: a warm-up, then the Phlex code |
| 3 | 25 min | Phlex basics: run your first jobs |
| 4 | 20 min | Your contribution |
| 5 | 20 min | Share it, and review |
| 6 | 5 min | What's next |

## How to use this notebook

**Type the commands yourself in a terminal.** Each step shows the commands in a grey box like this:

```bash
echo "type me in the terminal"
```

and tells you what you should see. Typing them is slower than clicking, but it's how they stick.

If you fall behind, each step has a **catch-up cell** (a code cell marked `# Catch-up`).
Running it does the step for you. Use them freely; nobody's marking this.

Four kinds of box appear throughout:

> 🧭 **Analogy:** a picture from everyday life to hang a new idea on.

> 🔬 **In an analysis:** where you would use this in real DUNE work.

> 📝 **Write it down:** something to add to your notes file.

> 😂 **xkcd:** because everyone has been here before.
""")

# ---------------------------------------------------------------- setup cell
md("""
## Before you start: tell the notebook who you are

Choose the **phaindia apptainer** kernel (top right of the notebook, or **Kernel → Change
Kernel…**). Then put your **GitHub username** in the cell below and run it. The catch-up cells
use it.
""")
code("""
ME = "your-github-username"  # <- change this

import os
from pathlib import Path

WORK = Path.home() / "phlex-work"
SRC = WORK / "phlex-india-sandbox"
BUILD = WORK / "build-sandbox"
WARM = WORK / "build-warmup"
MINE = SRC / "contributions" / ME
WORK.mkdir(exist_ok=True)

for name, value in [("ME", ME), ("WORK", WORK), ("SRC", SRC), ("BUILD", BUILD), ("WARM", WARM), ("MINE", MINE)]:
    os.environ[name] = str(value)

# phlex finds C++ plugins through PHLEX_PLUGIN_PATH and Python algorithms through PYTHONPATH
for var, path in [("PHLEX_PLUGIN_PATH", BUILD), ("PYTHONPATH", SRC)]:
    entries = [e for e in os.environ.get(var, "").split(":") if e]
    if str(path) not in entries:
        os.environ[var] = ":".join([str(path)] + entries)

if ME == "your-github-username":
    print("⚠️  Put your GitHub username in ME first.")
for name in ["ME", "SRC", "BUILD", "MINE"]:
    print(f"{name:6} {os.environ[name]}")
""")

# ---------------------------------------------------------------- part 0
md("""
# Part 0: The terminal, and your notes file (15 min)

A terminal is a window where you type commands and the computer answers in text. It looks old
fashioned, but it's the fastest way to work with code, and every DUNE computer has one.

> 🧭 **Analogy:** menus and buttons are like pointing at photos on a restaurant menu. The terminal
> is ordering by name. It's slower on day one, and much faster once you know the words.

**Open a terminal:** in JupyterLab, **File → New → Terminal**. You'll see a **prompt**, something
like:

```
jovyan@jupyter-you:~$
 └─┬─┘ └────┬────┘ └┬┘
 user     computer  where you are (~ means your home directory)
```

Type each command below and press Enter. Watch what comes back.

```bash
pwd                      # print working directory: where am I?
ls                       # list what's here
mkdir -p ~/phlex-work    # make a directory (-p: no complaint if it already exists)
cd ~/phlex-work          # change directory: go there
pwd                      # check
ls -a                    # list everything, including hidden files that start with "."
```

Three tricks that save hours:

| Key | What it does |
|---|---|
| **Tab** | Finishes a file or command name for you. Type `cd ~/phl` and press Tab. |
| **↑** | Brings back your previous command, so you can fix it and run it again. |
| **Ctrl-C** | Stops whatever is running. Your escape hatch. |

To read a long file, use `less <file>`: space bar for the next page, `q` to quit.
""")
xkcd(1168, "tar", "tar",
     "The terminal has a reputation. By the end of today you'll know more commands than the people in this comic.")
md("""
## Step into the container

The tools for today (phlex, CMake, the compiler) live in an **apptainer image**: a sealed box
with everything installed at the right versions. Step into it:

```bash
apptainer shell --cleanenv /opt/images/phaindia-0.1-20261002.sif
```

The prompt changes to `Apptainer>`. Check the tools:

```bash
phlex --version
cmake --version
git --version
```

Your home directory is the same inside and outside the box. If `git` isn't found inside, open a
**second** terminal and leave it outside the container for the git commands. Many people work like
this anyway: one terminal for building, one for git.

To leave the container, type `exit`.
""")
md("""
## Start your notes file

Professional software people keep notes. Not for anyone else: for themselves, next week. Which
command worked, what the error said, how you fixed it. Start yours now:

```bash
echo "# Phlex workshop notes, $(date +%F)" >> ~/phlex-work/NOTES.md
cat ~/phlex-work/NOTES.md
```

`>>` adds to the end of a file (one `>` would overwrite it). Now open `phlex-work/NOTES.md` from
the JupyterLab file browser on the left, so you can type in it as you go.

> 📝 **Write it down:** keep this file open all session. Whenever a command works, paste it in.
> Whenever something fails, paste the error and what fixed it.

Your notes stay in `~/phlex-work`, **outside** the repository you're about to clone, so they can't
end up on GitHub by accident.

> 🔬 **In an analysis:** six months from now someone asks "how did you make the plot in the tech
> note?" Your notes file is the answer.
""")
xkcd(979, "wisdom_of_the_ancients", "Wisdom of the Ancients",
     "Every forum thread that ends with \"never mind, fixed it\" is a note someone didn't write. Be the one who writes it down.")
code("""
%%bash
# Catch-up: make the work directory and the notes file
mkdir -p "$WORK"
[ -f "$WORK/NOTES.md" ] || echo "# Phlex workshop notes, $(date +%F)" > "$WORK/NOTES.md"
cat "$WORK/NOTES.md"
""")

# ---------------------------------------------------------------- part 1
md("""
# Part 1: Getting the code with GitHub (15 min)

Today's code is in a practice repository, **[nuRiceLab/phlex-india-sandbox](https://github.com/nuRiceLab/phlex-india-sandbox)**.
It's a trimmed copy of the official [phlex-examples](https://github.com/Framework-R-D/phlex-examples),
made for this workshop, so you can push to it and open pull requests without any risk to the
real thing.

Three copies of the code are involved:

```mermaid
flowchart LR
    U["<b>upstream</b><br/>nuRiceLab/phlex-india-sandbox<br/>(on GitHub)"]
    F["<b>your fork</b><br/>you/phlex-india-sandbox<br/>(on GitHub)"]
    C["<b>your clone</b><br/>~/phlex-work/phlex-india-sandbox<br/>(on the hub)"]
    U -- "1. Fork (button on GitHub)" --> F
    F -- "2. git clone" --> C
    C -- "3. git push" --> F
    F -- "4. pull request" --> U
```

> 🧭 **Analogy:** upstream is the publisher's master copy of a book. Your **fork** is your own
> photocopy, kept at the publisher's, that you're allowed to write in. Your **clone** is that
> photocopy on your desk. A **pull request** is sending the editor a note: "here are my
> corrections, please put them in the next edition." The editor (a reviewer) reads them first.

## 1.1 Fork it

Log in to GitHub, open https://github.com/nuRiceLab/phlex-india-sandbox and click **Fork** (top
right), then **Create fork**. You now have `https://github.com/<you>/phlex-india-sandbox`.

## 1.2 Clone your fork

Back in the terminal (put your username in place of `<you>`):

```bash
cd ~/phlex-work
git clone https://github.com/<you>/phlex-india-sandbox.git
cd phlex-india-sandbox
ls
```

## 1.3 Look around

```bash
git log --oneline -5     # the last five commits: a short ID (hash) and a message
git remote -v            # where this clone came from ("origin" = your fork)
```

The history is short: one commit that copied and trimmed phlex-examples, and one that added the
workshop parts. Read the first one in full with `git show --stat HEAD~1`: a good commit message
says where something came from and why. The official repository has hundreds of commits.

Tell your clone about upstream too, so you can get updates later:

```bash
git remote add upstream https://github.com/nuRiceLab/phlex-india-sandbox.git
git remote -v
```

## 1.4 Say who you are, and make a branch

git signs every commit with a name and email. These lines set them **for this repository only**:

```bash
git config user.name  "Your Name"
git config user.email "you@example.org"
```

Never work directly on `main`. Make your own **branch**: a separate line of work that you can
share, change or throw away without touching anyone else's.

```bash
git switch -c my-first-contribution
git status
```

`git status` is the command you'll type most. It says which branch you're on and what you've
changed. Right now: `nothing to commit, working tree clean`.

> 🔬 **In an analysis:** when a plot goes into a technical note, write down the commit hash
> (`git log --oneline -1`) of the code that made it. Months later, that hash gets you exactly
> the same code back.
""")
xkcd(1597, "git", "Git",
     "Everyone feels like this about git at first. Today you only need six commands, and this notebook tells you each one.")
code("""
%%bash
# Catch-up: clone (your fork if it exists, otherwise upstream) and make the branch
cd "$WORK"
if [ ! -d phlex-india-sandbox ]; then
  GIT_TERMINAL_PROMPT=0 git clone "https://github.com/$ME/phlex-india-sandbox.git" \\
    || git clone https://github.com/nuRiceLab/phlex-india-sandbox.git
fi
cd phlex-india-sandbox
git remote get-url upstream >/dev/null 2>&1 \\
  || git remote add upstream https://github.com/nuRiceLab/phlex-india-sandbox.git
git switch -c my-first-contribution 2>/dev/null || git switch my-first-contribution
git remote -v
git status
""")

# ---------------------------------------------------------------- part 2
md("""
# Part 2: Building with CMake (25 min)

C++ has to be **compiled** before it runs. CMake works out how: which compiler, where Phlex is
installed, which files need rebuilding. It does this in two steps:

1. **Configure:** `cmake <source-directory>` reads `CMakeLists.txt`, finds the compiler and the
   packages, and writes build files into the current directory.
2. **Build:** `cmake --build .` runs the compiler. Next time, it rebuilds only what changed.

> 🧭 **Analogy:** CMake is a cook with a recipe (`CMakeLists.txt`). **Configure** reads the recipe
> and checks the pantry: is there a compiler, is Phlex installed? **Build** does the cooking, and
> next time only re-cooks what changed.

You always build in a **separate directory**, next to the source and not inside it:

```
~/phlex-work/
├── NOTES.md                 <- your notes
├── phlex-india-sandbox/     <- source code (git tracks this)
│   └── cmake-warmup/        <- a tiny practice project
├── build-warmup/            <- build products for the warm-up
└── build-sandbox/           <- build products for the Phlex code (git never sees these)
```

> 🧭 **Analogy:** the source directory is the drawer of blueprints; the build directory is the
> workbench. If the bench gets messy, clear it (`rm -rf build-sandbox`) and build again. The
> blueprints are untouched.

## 2.1 Warm-up: a tiny project (10 min)

Before Phlex, practise on something small: one library (`greet`) and one program (`hello`) that
uses it. Read the recipe first:

```bash
cd ~/phlex-work/phlex-india-sandbox/cmake-warmup
ls
cat CMakeLists.txt
```

| Line | What it does |
|---|---|
| `project(cmake_warmup LANGUAGES CXX)` | Names the project; it's C++ |
| `add_library(greet SHARED greet.cpp)` | Makes a **target** `greet`: a library, `libgreet.so` |
| `add_executable(hello hello.cpp)` | Makes a target `hello`: a program |
| `target_link_libraries(hello PRIVATE greet)` | `hello` uses `greet`, so connect them |

Now configure, build and run. In the terminal, **inside the container**:

```bash
mkdir -p ~/phlex-work/build-warmup
cd ~/phlex-work/build-warmup
cmake ../phlex-india-sandbox/cmake-warmup    # configure
cmake --build .                              # build
./hello
```

**Try these, one at a time:**

1. **Change the greeting.** Open `cmake-warmup/greet.cpp` in the JupyterLab editor and change
   `"Hello, "` to `"Namaskara, "`. Save, then `cmake --build .` and `./hello`. Read the build
   output: only `greet.cpp` was recompiled. `hello.cpp` didn't change, so CMake left it alone.
2. **Use your own name.** Change `"Bengaluru"` in `hello.cpp` to your name. Rebuild. Which file is
   recompiled this time?
3. **Break it on purpose.** Delete the `;` at the end of the line in `hello.cpp`. Rebuild and
   **read the first error**: it names the file, the line and what the compiler expected. Put the
   `;` back.

If something fails, **read the first error**, not the last. The first one is usually the cause,
and the rest follow from it.

When you're done, ask git what you changed, then throw the practice edits away:

```bash
cd ~/phlex-work/phlex-india-sandbox
git status                    # greet.cpp and hello.cpp are "modified"
git diff                      # exactly what changed
git restore cmake-warmup      # put both files back as they were
git status                    # clean again
```

> 🧭 **Analogy:** a commit is a save point in a video game. `git restore` loads the last save, so
> you can try something risky without fear.
""")
code("""
%%bash
# Catch-up: build and run the warm-up project
mkdir -p "$WARM"
cd "$WARM"
cmake "$SRC/cmake-warmup" > /dev/null && cmake --build . | tail -2
./hello
""")
md("""
## 2.2 Build the Phlex code (15 min)

The Phlex examples are the same idea with more targets. In the terminal, **inside the container**:

```bash
mkdir -p ~/phlex-work/build-sandbox
cd ~/phlex-work/build-sandbox
cmake ../phlex-india-sandbox       # configure
cmake --build . -j 4               # build (4 jobs at once; the hub is shared, so please no more)
```

Configure should end with `Build files have been written to: …`. The build takes a few minutes.

If something fails, **read the first error**, not the last. The first one is usually the cause,
and the rest follow from it.

When it's done, see what you made:

```bash
ls *.so
```

There are two kinds of `.so` here, as in the warm-up:

- **SHARED libraries** (`libmy_add.so`, `libmy_geometry.so`): ordinary "experiment code" that
  knows nothing about Phlex, like `libgreet.so`.
- **Plugins**, built as `MODULE` (`add_and_verify.so`, `numbers_source.so`, …): code phlex loads
  while it runs. When a configuration says `cpp: 'add_and_verify'`, phlex looks for
  `add_and_verify.so`.

> 🧭 **Analogy:** a plugin is a game cartridge. The console (phlex) is already built, and it
> loads whichever cartridges the configuration asks for.

> 📝 **Write it down:** paste the three build commands into your notes. Tomorrow you'll need them
> again.
""")
xkcd(303, "compiling", "Compiling",
     "The build is running. You have a few minutes. Use them to read Part 3.")
md("""
> 📦 **Where did phlex come from?** You didn't install phlex today: it was already in the image.
> The image was built with **Spack**, the package manager DUNE uses for Phlex and its dependencies
> (Boost, TBB, ROOT and many more). Spack builds each package from a recipe, in the right order,
> with matching compilers. That takes hours, which is why it's done once, ahead of time, and
> packed into an image. If you want to install Phlex on your own laptop later, follow Phlex's
> [INSTALLATION.md](https://github.com/Framework-R-D/phlex/blob/main/INSTALLATION.md). Ask Kyle
> or a helper this week.
""")
xkcd(1987, "python_environment", "Python Environment",
     "What your laptop looks like without a package manager. The image saves you from this.")
code("""
%%bash
# Catch-up: configure and build
mkdir -p "$BUILD"
cd "$BUILD"
cmake "$SRC" -DCMAKE_BUILD_TYPE=Release > cmake-configure.log && echo "Configure OK"
cmake --build . -j 4 2>&1 | tail -3
ls *.so
""")

# ---------------------------------------------------------------- part 3
md("""
# Part 3: Phlex basics, your first jobs (25 min)

A Phlex job has two halves:

- **code**: the algorithms, compiled into plugins (Part 2) or written in Python
- **configuration**: a `.jsonnet` file that says which algorithms to run, on what data

Changing the configuration needs no rebuild. That's on purpose.

## The words you need

You met these in Kyle's lecture. Here they are with a picture each.

| Phlex term | 🧭 Analogy | Closest art idea |
|---|---|---|
| **Layer** | Nested boxes: a job holds spills, a spill holds interactions | Run / SubRun / Event, but you choose the levels |
| **Provider** (source) | The loading dock that brings raw material in | Input source |
| **Transform** | A machine on an assembly line: products in, a new product out | EDProducer |
| **Observer** | A quality inspector: looks at products, makes nothing new | EDAnalyzer |
| **Product selector** | A shipping label: who made it, at which layer, what it's called | InputTag |
| **Stage** | A stamp on each product saying which processing pass made it | Process name |

Phlex builds the assembly line from your configuration and runs as many machines at once as the
data allow. You don't write any threading code.

## Read a configuration

Before you run anything, set two paths so phlex can find the plugins and the Python code. In the
terminal, inside the container:

```bash
cd ~/phlex-work/build-sandbox
export PHLEX_PLUGIN_PATH=$PWD:$PHLEX_PLUGIN_PATH
export PYTHONPATH=$HOME/phlex-work/phlex-india-sandbox:$PYTHONPATH
less ../phlex-india-sandbox/test-cpp-workflow.jsonnet
```

These `export` lines only last for this terminal. Put them in your notes.

The file has three parts. Here's the job it describes:

```mermaid
flowchart LR
    D["<b>driver</b><br/>generate_layers:<br/>1 job, 10 spills"]
    G["<b>provider</b><br/>geometry_source<br/>(once per job)"]
    N["<b>provider</b><br/>numbers_source<br/>i and j, per spill"]
    A["<b>transform</b><br/>add: i + j → sum"]
    V["<b>observer</b><br/>verify: is sum OK?"]
    O["<b>observer</b><br/>form_module (FORM)<br/>writes output.root"]
    D --> N
    D --> G
    N --> A
    A --> V
    G --> V
    N --> O
    A --> O
```

- `driver` makes the layers: a `job` containing 10 `spill`s.
- `sources` are the providers. `numbers_source` gives two numbers, `i` and `j = -i`, for each spill.
- `modules` are the algorithms. `add_and_verify` adds `i + j` and checks the answer. `form_module`
  is **FORM**, Phlex's input/output system, writing products to a ROOT file.

## Run it

```bash
phlex -c ../phlex-india-sandbox/test-cpp-workflow.jsonnet --stage examples
```

`--stage` names this processing pass. Current Phlex requires it.

Read the output from the bottom up. You should see:

```
Processed layers:

  job
   │
   └ spill: 10
```

and a new file:

```bash
ls -l output.root
```

> 🗄️ **A taste of FORM:** `output.root` was written by FORM, the `form_module` entry in the
> configuration. Its `products:` list says what to keep. In Part 4 you'll change that list.
> Andrew Olivier's FORM tutorial shows how to write and read products properly, including
> reading them back in a second job.

> 🔬 **In an analysis:** the `products` list is how you **skim**: keep the reconstructed products
> you need and drop the big intermediate ones, such as raw waveforms, so files stay small.

## Run a Python algorithm

Phlex can run Python functions as algorithms. Have a look at `subtract.py`; it's an ordinary
function with type hints:

```bash
less ../phlex-india-sandbox/subtract.py
phlex -c ../phlex-india-sandbox/test-py-workflow.jsonnet --stage examples
```

No build was needed. phlex found `subtract.py` through `PYTHONPATH` and matched its `i: int, j: int`
with the C++ products.

> 🔬 **In an analysis:** Python algorithms are good for trying out a selection cut or running a
> PyTorch or ONNX model on each event, with nothing to compile. When the idea works and speed
> matters, move the slow parts to C++.

> 📝 **Write it down:** the two `export` lines, the `phlex -c … --stage …` command, and what
> `Processed layers:` said.
""")
code("""
%%bash
# Catch-up: run both example jobs
cd "$BUILD"
phlex -c "$SRC/test-cpp-workflow.jsonnet" --stage examples 2>&1 | tail -4
ls -l output.root
phlex -c "$SRC/test-py-workflow.jsonnet" --stage examples 2>&1 | tail -3
""")

# ---------------------------------------------------------------- part 4
md("""
# Part 4: Your contribution (20 min)

Now make something of your own. In this repository, each person works only in their own folder,
`contributions/<your-username>/`. Nobody's work can clash with anyone else's.

## 4.1 Copy the template

In the terminal (git commands can be inside or outside the container):

```bash
cd ~/phlex-work/phlex-india-sandbox
cp -r contributions/_template contributions/<you>
ls contributions/<you>
```

You get two files: `my-workflow.jsonnet`, a copy of the configuration you just ran, and
`README.md`, for other people to read.

## 4.2 Change the workflow

Open `contributions/<you>/my-workflow.jsonnet` in the JupyterLab editor and make two changes:

1. Run on **20** spills instead of 10 (`total: 20`).
2. Keep only the `sum` in the output file: `products: ['sum']`. That's your first FORM skim.

Save (Ctrl+S), then run it from the build directory. Note there's no rebuild: you only changed
configuration.

```bash
cd ~/phlex-work/build-sandbox
phlex -c ../phlex-india-sandbox/contributions/<you>/my-workflow.jsonnet --stage <you>
```

Check that `Processed layers:` now says `spill: 20`.
""")
code("""
%%bash
# Catch-up: copy the template and make the two changes
cd "$SRC"
[ -d "$MINE" ] || cp -r contributions/_template "$MINE"
sed -i "s/total: 10,/total: 20,/; s/products: \\['i', 'j', 'sum'\\]/products: ['sum']/" "$MINE/my-workflow.jsonnet"
grep -n "total\\|products" "$MINE/my-workflow.jsonnet"
cd "$BUILD"
phlex -c "$MINE/my-workflow.jsonnet" --stage "$ME" 2>&1 | tail -4
""")
md("""
## 4.3 Write the README

Code without a description is a puzzle for the next person, and the next person is often you.
Open `contributions/<you>/README.md` and fill it in:

- **What this does**, in one or two sentences
- **How to run it**: the exact command, written so someone else can copy it (no `/home/you/…` paths)
- **What you should see**: paste the `Processed layers:` lines
- **One thing you learned today**
- **One word for today**: at the end, everyone's word goes into the room's word cloud

> 🧭 **Analogy:** a README is the label on a sample jar. Without it, the next person has to open
> the jar and guess what's inside, and whether it's safe to touch.

Your `NOTES.md` is for you; the README is for everyone else. Some of your notes will move into
the README. That's normal.

## 4.4 Commit

Ask git what it sees:

```bash
cd ~/phlex-work/phlex-india-sandbox
git status
```

Your folder is **untracked**: git can see it but isn't recording it yet. Committing is two steps:

```mermaid
flowchart LR
    W["<b>working directory</b><br/>files as you edit them"]
    S["<b>staging area</b><br/>what goes in the next commit"]
    H["<b>history</b><br/>commits, for ever"]
    W -- "git add" --> S
    S -- "git commit" --> H
```

> 🧭 **Analogy:** `git add` puts things in a shopping cart. `git commit` is the checkout, and the
> receipt is dated and signed. You can fill the cart in several trips and take things out before
> you pay.

```bash
git add contributions/<you>
git status                     # now "Changes to be committed"
git diff --staged              # exactly what you're about to commit
git commit -m "Add my first Phlex workflow: 20 spills, FORM keeps only sum"
git log --oneline -3
```

A good commit message says **what the change does**, so that `git log` reads like a list of
what happened. "Add …", "Fix …", "Change … to …". Not "stuff".
""")
xkcd(1296, "git_commit", "Git Commit",
     "Commit messages get worse as a project gets longer. Write the one you'll want to read in six months.")
code("""
%%bash
# Catch-up: commit your folder (fill in the README first!)
cd "$SRC"
git add "contributions/$ME"
git commit -m "Add my first Phlex workflow: 20 spills, FORM keeps only sum" || echo "Nothing new to commit."
git log --oneline -3
""")
md("""
## 4.5 (Rung 3, optional) Add your own C++ algorithm

If you have time, add a C++ transform that multiplies `i` by `j`, with an observer that checks the
answer. Copy the two files from `_stretch`:

```bash
cd ~/phlex-work/phlex-india-sandbox
cp contributions/_stretch/* contributions/<you>/
less contributions/<you>/multiply_and_verify.cpp
```

Read the `.cpp` file next to `add_and_verify.cpp`: a **transform** with two inputs and one
output, and an **observer** that reads the transform's output. The small `CMakeLists.txt` names
your plugin after your folder, so it's `multiply_<you>` (a `-` in your username becomes `_`).

Rebuild. CMake notices the new `CMakeLists.txt` and reconfigures by itself:

```bash
cd ~/phlex-work/build-sandbox
cmake --build . -j 4           # look for: contributions/<you>: plugin multiply_<you>
```

Add a module to your `my-workflow.jsonnet`, next to `add_cpp`:

```jsonnet
    multiply_cpp: {
      cpp: 'multiply_<you>',
      layer: 'spill',
    },
```

Run the job again, then commit the new files with a good message.

> 🧭 **Analogy:** `concurrency::unlimited` in the code is a supermarket that opens as many
> checkout lanes as there are customers. That's safe because each cashier works alone. If
> everyone had to write in the same ledger (one shared histogram), you'd want one lane:
> `concurrency::serial`.
""")
code("""
%%bash
# Catch-up (rung 3): add the multiply algorithm, build and run it
cd "$SRC"
cp -n contributions/_stretch/* "$MINE/"
plugin="multiply_$(echo "$ME" | sed 's/[^A-Za-z0-9_]/_/g')"
grep -q multiply_cpp "$MINE/my-workflow.jsonnet" || \\
  sed -i "s|    // FORM writes these products|    multiply_cpp: {\\n      cpp: '$plugin',\\n      layer: 'spill',\\n    },\\n    // FORM writes these products|" "$MINE/my-workflow.jsonnet"
cd "$BUILD"
cmake --build . -j 4 2>&1 | grep -E "contributions/|error" ; ls -l "$plugin.so"
phlex -c "$MINE/my-workflow.jsonnet" --stage "$ME" 2>&1 | tail -4
cd "$SRC"
git add "contributions/$ME"
git commit -m "Add a multiply transform and an observer that checks it" || echo "Nothing new to commit."
""")

# ---------------------------------------------------------------- part 5
md("""
# Part 5: Share it, and review (20 min)

Your commits are in your clone on the hub. Nobody else can see them yet. Two steps make them
visible: **push** to your fork, then open a **pull request** (PR) to upstream.

## 5.1 Push

GitHub needs to know it's you. It doesn't accept your password from the terminal; it wants a
**personal access token** instead. If you made one before the workshop, use it. If not:

1. On GitHub: your picture (top right) → **Settings** → **Developer settings** →
   **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**.
2. Note: `phlex workshop`. Expiration: 7 days. Tick only **public_repo**. Click **Generate**.
3. Copy the token now (it starts with `ghp_`). GitHub shows it only once. **Never put it in a
   file in the repository.**

Then:

```bash
cd ~/phlex-work/phlex-india-sandbox
git config --global credential.helper 'cache --timeout=28800'   # remember the token for 8 hours
git push -u origin my-first-contribution
```

Username: your GitHub username. Password: **paste the token**. Nothing appears as you paste; that's
normal.

## 5.2 Open the pull request

Open your fork on GitHub. A yellow bar says your branch had recent pushes: click
**Compare & pull request**. Check the arrow says

`nuRiceLab/phlex-india-sandbox: main  ←  <you>/phlex-india-sandbox: my-first-contribution`

Give it a clear title, fill in the checklist in the description, and click **Create pull request**.

A **contribution check** runs on your PR and gives it a ✅ or a ❌. A ❌ isn't a disaster: click
**Details**, read the message, fix it in your branch, commit, and push again.

> **No terminal? Or the push won't work?** Do it in the browser. On your fork, open
> `contributions/`, click **Add file → Create new file**, name it `<you>/README.md`, write your
> README, choose **Create a new branch** and click **Propose changes**. GitHub then opens the
> pull request for you. That's rung 1, and it counts.
""")
code("""
%%bash
# Catch-up: there's no catch-up for pushing; it needs your token.
# This shows what would be pushed.
cd "$SRC"
git log --oneline main..HEAD
git diff --stat main..HEAD
""")
md("""
## 5.3 Review: the most important step

On DUNE, **no code is merged until someone else has read it.** Reviewing isn't a formality. It's
how mistakes get caught before they reach a production run, and how you learn other people's
code. A good review is as valuable as good code.

**First, everyone reviews the same PR.** Find the open PR called **"pls merge"** by
`gavinsdavies` in https://github.com/nuRiceLab/phlex-india-sandbox/pulls. It has a lot of
problems, on purpose. Go to **Files changed** and see how many you can find, using the checklist
in [`contributions/README.md`](https://github.com/nuRiceLab/phlex-india-sandbox/blob/main/contributions/README.md):

- Only one folder changed?
- A README that says what, how to run, and what to expect?
- Clear commit messages? (Look at the **Commits** tab.)
- No build products, personal notes or passwords?
- Do the names in the `.jsonnet` match the code?
- Do the comments and `assert`s make sense?

**Leave at least one comment on a line.** Hover over the line, click the blue **+**, write your
comment, and click **Start a review**. When you're done, **Review changes → Comment**.

Be kind and specific: "This `CMakeCache.txt` is a build product; could you remove it and add it to
`.gitignore`?" helps. "bad" doesn't.

**Then review a classmate.** Find the PR whose number is **one more than yours** (the newest one
reviews the oldest). Check it against the list. If it's good, **Approve** it. If something needs
fixing, **Request changes** and say what.

## 5.4 Answer your review

If your reviewer asks for a change, **don't** open a new PR. Fix it in the same branch:

```bash
# edit the file, then:
git add contributions/<you>
git commit -m "README: add the expected output"
git push
```

Refresh the PR page: your new commit is there, and the reviewer can see exactly what changed.
That loop (push, review, fix, push) is how all of Phlex and DUNE software gets written.
""")
xkcd(1513, "code_quality", "Code Quality",
     "Reviews exist so that this conversation happens before the code is merged, not after.")

# ---------------------------------------------------------------- part 6
md("""
# Part 6: What's next (5 min)

## What you did today

| Skill | Commands and tools |
|---|---|
| Terminal | `pwd`, `ls`, `cd`, `mkdir`, `less`, Tab, ↑, Ctrl-C, `apptainer shell` |
| git | `clone`, `remote`, `switch -c`, `status`, `diff`, `restore`, `add`, `diff --staged`, `commit`, `log`, `push` |
| GitHub | fork, pull request, the contribution check, line comments, approve / request changes |
| CMake | configure vs build, a separate build directory, targets, incremental rebuilds, reading the first error, SHARED libraries vs plugins |
| Phlex | jsonnet configuration (`driver`, `sources`, `modules`), `--stage`, `PHLEX_PLUGIN_PATH`, providers, transforms, observers, C++ and Python algorithms |
| FORM | `form_module` and its `products` list |
| Habits | a notes file, a README, clear commit messages, reviewing |

## Move on to the official repository

Today you used a trimmed copy. The real one is
**[Framework-R-D/phlex-examples](https://github.com/Framework-R-D/phlex-examples)**. It has
everything we left out: an unfold example (one product split into many), the GausHitFinder
migration from LArSoft in four designs with tests, and a branch for each Phlex release. Clone the
branch that matches your `phlex --version`, next to your sandbox:

```bash
cd ~/phlex-work
git clone -b phlex-v0.4 https://github.com/Framework-R-D/phlex-examples.git
less phlex-examples/README.md
```

You already know how to build and run it: same commands, different directory names. You won't
push to this one. If you find a problem in it, open an **issue** on GitHub and describe it; the
Phlex developers want to hear.

## Keep going

- **Your fork is your workspace for the rest of the week.** Later sessions use the same loop:
  branch, commit, push, PR, review.
- **Later sessions** go deeper into Phlex: the GausHitFinder migration from LArSoft, and its tests.
- **Andrew Olivier's FORM tutorial** shows writing and reading products with FORM.
- **For more depth**, the notebook `phlex-examples-tutorial.ipynb` has the rest: how CMake
  targets and plugins really work, unfolds, using git to undo a mistake, a Python observer, and a
  mock neutrino analysis with plots.
- **To stay up to date with upstream:** `git fetch upstream` and `git merge upstream/main`.

## Today, in one word

Once your pull request is merged, the "One word for today" in your README joins everyone else's.
At the end of the session we put the room's word cloud on the screen. It's made by
`tools/word-cloud.py` in the sandbox, from the merged READMEs.

> 📝 **Write it down:** one thing that confused you today. Ask about it tomorrow.
""")
xkcd(927, "standards", "Standards",
     "Why DUNE wants one framework that everyone uses, and why your review comments on it matter.")

nb = nbf.v4.new_notebook()
nb.cells = cells
# Fixed cell IDs, so rebuilding an unchanged notebook gives an identical file and a clean git diff
for i, cell in enumerate(nb.cells):
    cell.id = f"cell-{i:02d}"
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb.metadata["language_info"] = {"name": "python"}
nbf.validate(nb)
out = sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).with_name("phlex-first-steps.ipynb")
nbf.write(nb, out)
print(f"{len(cells)} cells -> {out}")
