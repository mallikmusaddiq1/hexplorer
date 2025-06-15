# 🎨 Hexplorer

**Hexplorer** is a terminal-based interactive HEX color exploration tool written in Python.  
Explore colors by HEX or decimal, view contrast ratios, simulate color blindness, generate gradients, and more — all from your terminal.

---

## ✨ Features

- View colors by HEX code or decimal index (0–16777215)
- Display RGB values, luminance, contrast ratio vs. white, and decimal index
- Mix two HEX colors and preview the result
- Generate smooth gradients between two colors
- Create complementary, triadic, and tetradic color schemes
- Simulate color blindness (protanopia, deuteranopia, tritanopia)
- Export color data to JSON
- Supports 24-bit truecolor terminal display

---

## 🛠️ Prerequisites

- Python 3.6 or higher
- `pip` (Python package manager)
- `git` (for cloning the repository)
- A terminal with 24-bit truecolor support (e.g., iTerm2, Windows Terminal, Alacritty)

---

## 📦 Installation

### Option 1: Install from source

```bash
# Clone the repository
git clone https://github.com/mallikmusaddiq1/hexplorer.git
cd hexplorer

# Build and install
python setup.py sdist bdist_wheel
pip install dist/hexplorer-1.0.0-py3-none-any.whl
```

### Option 2: Install directly via pip (coming soon)

```bash
pip install hexplorer
```

---

## 🚀 Usage

### Interactive mode

Start the tool:

```bash
hexplorer
```

You’ll be asked to enter a 6-digit HEX code (e.g. `FF0000`) to begin.  
Then, use the interactive commands listed below.

### Check version

```bash
hexplorer --version
# or
hexplorer -v
```

### Show help

```bash
hexplorer --help
# or
hexplorer -h
```

> **Note**: `hexplorer` launches an interactive session. It is not meant to be used with command-line flags like `ffmpeg` or `curl`. All commands are entered inside the tool's prompt.

---

## ⌨️ Commands

| Command     | Description                                          |
|-------------|------------------------------------------------------|
| `n`         | Move to the next color                               |
| `p`         | Move to the previous color                           |
| `j`         | Jump to a custom HEX                                 |
| `i`         | Jump to a decimal index (0–16777215)                 |
| `r`         | Jump to a random color                               |
| `m`         | Mix with a given HEX color                           |
| `mixr`      | Mix with a random color                              |
| `mixi`      | Mix with a color by decimal index                    |
| `grad`      | Generate a gradient from current to another HEX      |
| `cs`        | Show color harmony schemes                           |
| `export`    | Export current color data to JSON                    |
| `cb`        | Simulate color blindness types                       |
| `rcs`       | Generate a random color and its schemes              |
| `help`      | Show command help                                    |
| `q`         | Quit the program                                     |

---

## 📂 Exported Files

All export files are saved in:

```
/storage/emulated/0/hexplorer.json
```

Examples:

- `hexplorer_FF0000.json`
- `hexplorer_mix_FF0000_00FF00.json`
- `hexplorer_gradient_FF0000_00FF00_5.json`

---

## 🛡️ Troubleshooting

- **No colors in terminal**: Ensure your terminal supports 24-bit truecolor (e.g., iTerm2, Windows Terminal).
- **Permission denied for exports**: Verify write permissions for `/storage/emulated/0/Hexplorer/`.
- **Python errors**: Confirm you’re using Python 3.6 or higher (`python --version`).
- For further help, check the [GitHub Issues](https://github.com/mallikmusaddiq1/hexplorer/issues) page.

---

## 🔧 Project Structure

```text
hexplorer/
├── hexplorer/
│   ├── __init__.py
│   └── main.py
├── README.md
├── LICENSE
├── setup.py
└── pyproject.toml
```

---

## 📜 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for more info.

---

## 👤 Author

**Mallik Mohammad Musaddiq**  
GitHub: [@mallikmusaddiq1](https://github.com/mallikmusaddiq1)