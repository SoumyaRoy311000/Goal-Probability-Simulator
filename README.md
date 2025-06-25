# Goal Probability Simulator

A cross-platform desktop application that analyzes football player goal-scoring performance using Expected Goals (xG) statistics and binomial distribution models.

## Features

- **Modern GUI**: Built with tkinter and styled using `sv-ttk` with automatic dark/light theme detection
- **xG-based Analysis**: Analyze player performance using cumulative xG and total shots
- **Binomial Distribution Model**: Calculate goal probabilities using statistical modeling
- **Interactive Visualization**: Embedded matplotlib charts display distributions with real-time updates
- **PDF Export**: Save visual analysis charts as PDF files
- **Dark Mode Toggle**: Manually toggle between dark/light mode in addition to auto-detection

## Installation

### 🛠️ Prerequisites

- Python 3.7 or later (3.10+ recommended)
- Internet access to install dependencies

---

### 🐧 Linux / 🍎 macOS / 🪟 Windows

#### Option 1: 🔒 Virtual Environment (Recommended)

```bash
# 1. Navigate to the project directory
cd path/to/goal-probability-simulator

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python goal_probability_simulator.py
```

#### Option 2: 🌍 Global Installation (Not Recommended)

```bash
pip install numpy scipy matplotlib pillow sv-ttk darkdetect
python goal_probability_simulator.py
```

---

### Platform-Specific Notes

#### 🐧 Linux

- Fedora: `sudo dnf install python3-tkinter`
- Arch: `sudo pacman -S tk`

#### 🍎 macOS

- Avoid using system Python `/usr/bin/python3` — use [python.org](https://www.python.org/downloads/mac-osx/) or Homebrew
- If you encounter GUI issues, change matplotlib backend:

```python
import matplotlib
matplotlib.use('macosx')
```

#### 🪟 Windows

- Use PowerShell or Command Prompt (not Git Bash)
- If `tkinter` errors occur, reinstall Python from [python.org](https://www.python.org/downloads/windows/)

## Usage

Launch the app:

```bash
python goal_probability_simulator.py
```

- Enter player name, total xG, total shots, and actual goals
- Click "📈 Analyze xG Performance" to visualize the probability distribution
- Optionally toggle dark mode and save the chart as a PDF

## How It Works

- **xG per Shot** = xG ÷ Shots
- **Binomial Model**: Computes the probability of scoring each number of goals using scipy's binomial distribution
- Highlights the probability of actual goals scored
- Optionally exports the chart as a PDF for reporting

## Project Structure

```
goal-probability-simulator/
├── goal_probability_simulator.py  # Main GUI logic
├── requirements.txt               # Python dependencies
└── README.md                      # Project instructions
```

## Dependencies

- `tkinter` – GUI framework (included with Python)
- `matplotlib` – Chart rendering
- `numpy`, `scipy` – Statistical modeling
- `pillow` – For image/PDF export (via matplotlib)
- `sv-ttk` – Modern themed widgets
- `darkdetect` – Auto-detects OS light/dark mode

## Default Input Values

For quick testing:

- Player Name: Player
- xG: 5.0
- Shots: 20
- Goals: 3

## Error Handling

The app performs validation for:

- Missing or invalid numerical entries
- Negative or zero inputs where not allowed
- Displays popup errors using `tkinter.messagebox`

## License

MIT License

---

Enjoy analyzing football goal probabilities with visual insights!

