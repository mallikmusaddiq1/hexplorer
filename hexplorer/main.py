this script should be run with Python 3.

# Import required modules for the script.
import random  # For generating random numbers (used in random color generation).
import re      # For regular expression to validate hex color codes.
import json    # For exporting color data to JSON files.
import os      # For file and directory operations (e.g., creating folders, setting environment variables). # For converting RGB values to CSS3 color names.
import sys
import time
import platform

def ensure_termux_storage():
    """
    Ensures That Termux Has Storage Permission.
    If Not, It Requests It Using `termux-setup-storage`.
    """
    shared_path = "/storage/emulated/0"

    # Only attempt if running inside Termux
    if platform.system() == "Linux" and "com.termux" in os.environ.get("PREFIX", ""):
        if not os.path.exists(shared_path):
            print("🔐 Requesting Termux Storage Permission...")
            os.system("termux-setup-storage")
            print("📁 Please Allow The Permission Lopup...")

            input("📌 Press Enter Pfter Granting Storage Permission...")
            time.sleep(1)

            if not os.path.exists(shared_path):
                print("❌ Storage Access Still Not Granted. Please Allow It Manually From Termux > App Info > Permissions.")
                exit(1)
            else:
                print("✅ Storage Access Granted Successfully.")

__version__ = "1.0.0"

# Handle version and help flags early
if len(sys.argv) > 1:
    if sys.argv[1] in ("--help", "-h"):
        print(f"""
HEXPLORER - Terminal HEX Color Explorer (v{__version__})

Usage:
  hexplorer             Start The Interactive Color Tool
  hexplorer --help      Show This Help Message
  hexplorer --version   Show Version Info

Features:
  • View HEX & RGB colors
  • Mix, Gradient, Color Schemes
  • Export to JSON
  • Simulate Color Blindness
  • 24-bit Truecolor Terminal Output

Interactive Commands (inside the tool):

  n, p, j, i, r, m, mixr, mixi, grad, cs, export, cb, rcs, help, q
   n       → Move To Next Color
   p       → Move To Previous Color
   j       → Jump To Custom HEX
   i       → Jump to Decimal Index (0 To 16777215)
   r       → Jump To Random Color
   m       → Mix Color With HEX
   mixr    → Mix With Random Color
   mixi    → Mix With Decimal Index (0 To 16777215)
   grad    → Gradient From Current To Specific HEX
   cs      → Show Color Harmony Scheme For Current Color
   export  → Export Current Color To JSON (path: /storage/emulated/0/hexplorer.json/filename.json)
   cb      → Color Blindness Simulation Of Current Color
   rcs     → Generate Random Color Schemes
   help    → Show This Help Menu
   q       → Quit Or CTRL+C + Enter
        """)
        sys.exit(0)

    elif sys.argv[1] in ("--version", "-v"):
        print(f"hexplorer version {__version__}")
        sys.exit(0)

VERSION = "1.0.0"

def print_cli_help():
    print(f"""
🎨 Hexplorer v{VERSION} - A Terminal-Based HEX Color Explorer

Usage:
    hexplorer                  Start interactive color explorer
    hexplorer --help          Show this help menu
    hexplorer --version       Show version info

Features:
    ▪ Explore HEX and Decimal RGB colors
    ▪ Mix, Generate Gradients, Color Schemes
    ▪ Simulate Color Blindness
    ▪ Export JSON color info

Visit: https://github.com/mallikmusaddiq1/hexplorer
""")

# Define constant for maximum decimal value of a 24-bit color (0xFFFFFF = 16777215).
MAX_DEC = 16777215  # Represents the total number of possible colors in a 24-bit RGB system.

# Create a folder to store exported JSON files if it doesn't already exist.
folder_path = "/storage/emulated/0/hexplorer.json"  # Path for storing JSON exports, typically for Android storage.
os.makedirs(folder_path, exist_ok=True)  # Creates the directory, does nothing if it already exists.

# Define lines to be added to the user's .bashrc file to enable true color support in the terminal.
bashrc_lines = [
    "export COLORTERM=truecolor\n",  # Enables true color (24-bit) support in the terminal.
    "export TERM=xterm-256color\n"   # Sets terminal type to support 256 colors.
]

# Specify the path to the .bashrc file in the user's home directory.
bashrc_path = os.path.expanduser("~/.bashrc")  # Expands ~ to the user's home directory path.

try:
    # Check if .bashrc exists and read its contents.
    if os.path.exists(bashrc_path):  # Check if the .bashrc file exists.
        with open(bashrc_path, "r") as f:  # Open the file in read mode.
            existing = f.readlines()  # Read all lines into a list.
    else:
        existing = []  # If the file doesn't exist, initialize an empty list.

    # Append the color support lines to .bashrc if they are not already present.
    with open(bashrc_path, "a") as f:  # Open the file in append mode.
        for line in bashrc_lines:  # Iterate through the lines to add.
            if line not in existing:  # Check if the line is not already in the file.
                f.write(line)  # Append the line to the .bashrc file.

    # Set environment variables for the current script session to enable true color support.
    os.environ["COLORTERM"] = "truecolor"  # Set COLORTERM environment variable.
    os.environ["TERM"] = "xterm-256color"  # Set TERM environment variable.
    print("✅ Variables Exported And Added to .bashrc")  # Confirm successful addition.

    # Display the current values of the environment variables to confirm they are active.
    print(f"🟢 COLORTERM = {os.environ.get('COLORTERM')}")  # Show COLORTERM value.
    print(f"🟢 TERM = {os.environ.get('TERM')}")  # Show TERM value.

except Exception as e:
    print(f"❌ Error: {e}")  # Print any errors that occur during .bashrc modification.

# Function to convert a 6-digit hex color code to RGB values.
def hex_to_rgb(hex_code):
    r = int(hex_code[0:2], 16)  # Extract and convert red component (first 2 chars) to integer.
    g = int(hex_code[2:4], 16)  # Extract and convert green component (next 2 chars).
    b = int(hex_code[4:6], 16)  # Extract and convert blue component (last 2 chars).
    return r, g, b  # Return RGB values as a tuple.

# Function to convert RGB values back to a 6-digit hex color code.
def rgb_to_hex(r, g, b):
    return f"{r:02X}{g:02X}{b:02X}"  # Format RGB values as a 6-digit hex string (uppercase).

# Function to validate if a string is a valid 6-digit hexadecimal color code.
def is_valid_hex(h):
    return re.fullmatch(r"[0-9A-Fa-f]{6}", h) is not None  # Check if the string matches the pattern for a 6-digit hex code.

# Function to compute luminance component for a single color channel (used in luminance calculation).
def lum_comp(c):
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4  # Apply luminance formula based on sRGB standard.

# Function to gather metadata about a color, including hex, RGB, luminance, contrast, and name.
def get_color_metadata(hex_code, dec_index=None):
    r, g, b = hex_to_rgb(hex_code)  # Convert hex to RGB.
    rl, gl, bl = r / 255, g / 255, b / 255  # Normalize RGB values to range [0, 1].
    # Calculate relative luminance using the sRGB luminance formula.
    l = 0.2126 * lum_comp(rl) + 0.7152 * lum_comp(gl) + 0.0722 * lum_comp(bl)
    contrast = round((1 + 0.05) / (l + 0.05), 2)  # Calculate contrast ratio against white.

    try:
        color_name = webcolors.rgb_to_name((r, g, b))  # Try to get the color name for the RGB values.
    except ValueError:
        color_name = "Unknown"  # If no name is found, use "Unknown".

    return {
        "hex": f"#{hex_code}",  # Return hex code with # prefix.
        "rgb": {"r": r, "g": g, "b": b},  # Return RGB values as a dictionary.
        "luminance": round(l, 6),  # Return rounded luminance value.
        "contrast_vs_white": f"{contrast} : 1",  # Return contrast ratio formatted as a string.
        "decimal_index": dec_index if dec_index is not None else int(hex_code, 16),  # Return decimal index or convert hex to decimal.
        """
    }

# Function to display a colored block in the terminal for a given hex color.
def print_color_block(hex_code):
    r, g, b = hex_to_rgb(hex_code)  # Convert hex to RGB.
    print(f"                  \033[48;2;{r};{g};{b}m        \033[0m #{hex_code}")  # Print a colored block using ANSI escape codes.

# Function to display technical information about a color (RGB, luminance, contrast).
def show_tech_info(hex_code):
    r, g, b = hex_to_rgb(hex_code)  # Convert hex to RGB.
    rl, gl, bl = r / 255, g / 255, b / 255  # Normalize RGB values.
    # Calculate luminance using the sRGB formula.
    l = 0.2126 * lum_comp(rl) + 0.7152 * lum_comp(gl) + 0.0722 * lum_comp(bl)
    contrast = (1 + 0.05) / (l + 0.05)  # Calculate contrast ratio against white.
    index = int(hex_code, 16)  # Convert hex to decimal index.

    print(f"🔢 Mixed Color Index  : {index} / {MAX_DEC}")  # Show the decimal index of the color.
    print("🧪 Technical Info:")  # Header for technical details.
    print(f"   RGB              : {r}, {g}, {b}")  # Display RGB values.
    print(f"   Luminance        : {l:.6f}")  # Display luminance rounded to 6 decimals.
    print(f"   Contrast vs White: {contrast:.2f} : 1")  # Display contrast ratio against white.

# Function to export color data to a JSON file.
def export_json(filename, data):
    path = f"{folder_path}/{filename}"  # Construct the full file path for the JSON file.
    try:
        with open(path, "w") as f:  # Open the file in write mode.
            json.dump(data, f, indent=4)  # Write the data as formatted JSON with indentation.
        print(f"✅ Exported To: {path}")  # Confirm successful export.
    except Exception as e:
        print(f"❌ Failed to export JSON: {e}")  # Print any errors that occur during export.

# Function to export metadata for a single color to a JSON file.
def export_color(hex_code, dec_index):
    data = get_color_metadata(hex_code, dec_index)  # Get metadata for the color.
    export_json(f"hexplorer_{hex_code}.json", data)  # Export the metadata to a JSON file.

# Function to export metadata for a color mix (two input colors and the result) to a JSON file.
def export_mix(hex1, hex2, mixed):
    data = {
        "mix_input_1": get_color_metadata(hex1),  # Metadata for the first input color.
        "mix_input_2": get_color_metadata(hex2),  # Metadata for the second input color.
        "mixed_result": get_color_metadata(mixed)  # Metadata for the mixed color.
    }
    export_json(f"hexplorer_mix_{hex1}_{hex2}.json", data)  # Export the mix data to a JSON file.

# Function to export a gradient (list of colors between two hex codes) to a JSON file.
def export_gradient(hex1, hex2, steps_list, steps):
    data = {
        "gradient_from": f"#{hex1}",  # Starting hex color.
        "gradient_to": f"#{hex2}",  # Ending hex color.
        "steps": steps + 1,  # Number of steps in the gradient (including start and end).
        "colors": [get_color_metadata(h) for h in steps_list]  # Metadata for each color in the gradient.
    }
    export_json(f"hexplorer_gradient_{hex1}{hex2}{steps}.json", data)  # Export the gradient data to a JSON file.

# Function to prompt the user for a valid starting 6-digit hex color code.
def ask_start_hex():
    while True:
        start = input("🎯 Start By Entering A 6-digit HEX (Without #, e.g., FF0000): ").strip()  # Prompt user for hex code.
        if is_valid_hex(start):  # Validate the input.
            return int(start.upper(), 16)  # Convert valid hex to decimal and return.
        print("❌ Invalid hex. Try again.")  # Prompt again if input is invalid.

# Function to mix two colors by averaging their RGB components.
def mix_colors(hex1, hex2):
    r1, g1, b1 = hex_to_rgb(hex1)  # Convert first hex to RGB.
    r2, g2, b2 = hex_to_rgb(hex2)  # Convert second hex to RGB.
    rm, gm, bm = (r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2  # Average the RGB components.
    mixed = f"{rm:02X}{gm:02X}{bm:02X}"  # Convert averaged RGB back to hex.

    print(f"\n🔗 Mixing #{hex1} + #{hex2} => #{mixed}")  # Display the mixing operation.
    print_color_block(hex1)  # Show the first color block.
    print_color_block(hex2)  # Show the second color block.
    print("➡️ Result:")  # Header for the mixed result.
    print_color_block(mixed)  # Show the mixed color block.

    neg_hex = f"{MAX_DEC - int(mixed, 16):06X}"  # Calculate the negative (complementary) color.
    print(f"🔄 Negative Color     : #{neg_hex}")  # Display the negative color.
    print_color_block(neg_hex)  # Show the negative color block.

    show_tech_info(mixed)  # Display technical info for the mixed color.
    export_mix(hex1, hex2, mixed)  # Export the mix data to a JSON file.

# Function to generate a gradient between two hex colors with a specified number of steps.
def generate_gradient(hex1, hex2, steps=5):
    r1, g1, b1 = hex_to_rgb(hex1)  # Convert first hex to RGB.
    r2, g2, b2 = hex_to_rgb(hex2)  # Convert second hex to RGB.
    steps_list = []  # List to store the hex codes of the gradient steps.

    print(f"\n🌈 Gradient: #{hex1} ➡️ #{hex2} ({steps} steps)")  # Display gradient information.
    for i in range(steps + 1):  # Iterate through the number of steps (including start and end).
        r = int(r1 + (r2 - r1) * i / steps)  # Interpolate red component.
        g = int(g1 + (g2 - g1) * i / steps)  # Interpolate green component.
        b = int(b1 + (b2 - b1) * i / steps)  # Interpolate blue component.
        code = f"{r:02X}{g:02X}{b:02X}"  # Convert interpolated RGB to hex.
        print_color_block(code)  # Display the color block for this step.
        steps_list.append(code)  # Add the hex code to the steps list.

    export_gradient(hex1, hex2, steps_list, steps)  # Export the gradient data to a JSON file.

# Function to generate a color scheme (complementary, analogous, triadic, tetradic) for a given hex color.
def generate_scheme(hex_code):
    print(f"\n🎨 Generating color scheme for #{hex_code}")  # Display the color being used.
    print_color_block(hex_code)  # Show the original color block.

    r, g, b = hex_to_rgb(hex_code)  # Convert hex to RGB.
    schemes = {
        "Complementary": (255 - r, 255 - g, 255 - b),  # Opposite color on the color wheel.
        "Analogous 1": (r, min(g + 30, 255), b),  # Slightly shift green component up for similar hue.
        "Analogous 2": (r, max(g - 30, 0), b),  # Slightly shift green component down for similar hue.
        "Triadic 1": (b, r, g),  # Rotate RGB components for triadic harmony.
        "Triadic 2": (g, b, r),  # Rotate RGB components for triadic harmony.
        "Tetradic 1": (255 - r, 255 - g, b),  # Complementary + analogous for rectangular harmony.
        "Tetradic 2": (r, g, 255 - b)  # Complementary + analogous for rectangular harmony.
    }

    for name, (r2, g2, b2) in schemes.items():  # Iterate through the schemes.
        h = rgb_to_hex(r2, g2, b2)  # Convert scheme RGB to hex.
        print(f"{name} ➡️ #{h}")  # Display the scheme name and hex code.
        print_color_block(h)  # Show the color block for the scheme.

# Function to simulate how a color appears under different types of color blindness.
def simulate_color_blindness(hex_code):
    """ Simulate common color blindness types on the input color.
        Returns a dict with types and simulated hex colors. """
    # Define transformation matrices for color blindness simulation (approximations from literature).
    cb_matrices = {
        "Protanopia": [  # Red blindness (L-cone deficiency).
            [0.56667, 0.43333, 0],
            [0.55833, 0.44167, 0],
            [0, 0.24167, 0.75833]
        ],
        "Deuteranopia": [  # Green blindness (M-cone deficiency).
            [0.625, 0.375, 0],
            [0.70, 0.30, 0],
            [0, 0.30, 0.70]
        ],
        "Tritanopia": [  # Blue blindness (S-cone deficiency).
            [0.95, 0.05, 0],
            [0, 0.43333, 0.56667],
            [0, 0.475, 0.525]
        ],
    }

    r, g, b = hex_to_rgb(hex_code)  # Convert hex to RGB.

    # Helper function to apply a color blindness matrix to RGB values.
    def apply_matrix(r, g, b, m):
        rr = r * m[0][0] + g * m[0][1] + b * m[0][2]  # Apply matrix for red component.
        gg = r * m[1][0] + g * m[1][1] + b * m[1][2]  # Apply matrix for green component.
        bb = r * m[2][0] + g * m[2][1] + b * m[2][2]  # Apply matrix for blue component.
        # Clamp the resulting RGB values to the valid range (0-255).
        rr = max(0, min(255, int(rr)))
        gg = max(0, min(255, int(gg)))
        bb = max(0, min(255, int(bb)))
        return rr, gg, bb

    results = {}  # Dictionary to store simulated hex codes for each color blindness type.
    for cb_type, matrix in cb_matrices.items():  # Iterate through each color blindness type.
        rr, gg, bb = apply_matrix(r, g, b, matrix)  # Apply the transformation matrix.
        results[cb_type] = rgb_to_hex(rr, gg, bb)  # Convert transformed RGB to hex.

    # Display the simulation results with color blocks.
    print(f"\n🧩 Color Blindness Simulation For #{hex_code}:")
    for cb_type, cb_hex in results.items():
        print(f"{cb_type:<12} ➡️ #{cb_hex} ", end="")  # Display the color blindness type and hex code.
        print_color_block(cb_hex)  # Show the simulated color block.
    return results  # Return the dictionary of simulated colors.

# Function to generate a random color and its associated color schemes.
def generate_random_scheme():
    """ Generate a random base color and multiple color schemes from it. """
    base_dec = random.randint(0, MAX_DEC)  # Generate a random decimal index for the base color.
    base_hex = f"{base_dec:06X}"  # Convert to 6-digit hex code.
    print(f"\n🎲 Random Base Color: #{base_hex}")  # Display the random base color.
    print_color_block(base_hex)  # Show the base color block.

    r, g, b = hex_to_rgb(base_hex)  # Convert base hex to RGB.

    # Generate various color schemes based on the random base color.
    schemes = {}

    # Complementary: Opposite color on the color wheel.
    comp = (255 - r, 255 - g, 255 - b)
    schemes["Complementary"] = comp

    # Helper function to clamp RGB values to the valid range (0-255).
    def clamp_color(val): return max(0, min(255, val))
    # Analogous: Adjust green component by ±30 for similar hues.
    schemes["Analogous 1"] = (r, clamp_color(g + 30), b)
    schemes["Analogous 2"] = (r, clamp_color(g - 30), b)

    # Triadic: Rotate RGB components for triadic harmony.
    schemes["Triadic 1"] = (b, r, g)
    schemes["Triadic 2"] = (g, b, r)

    # Tetradic: Complementary color + analogous shift.
    schemes["Tetradic 1"] = comp
    schemes["Tetradic 2"] = (comp[0], clamp_color(comp[1] + 30), comp[2])

    print("\n🎨 Random Color Schemes:")  # Header for the schemes.
    for name, (rr, gg, bb) in schemes.items():  # Iterate through the schemes.
        h = rgb_to_hex(rr, gg, bb)  # Convert scheme RGB to hex.
        print(f"{name:<12} ➡️ #{h}")  # Display the scheme name and hex code.
        print_color_block(h)  # Show the color block for the scheme.

    return base_hex, schemes  # Return the base hex and the schemes dictionary.

# Function to display the help menu with available commands.
def show_help():
    print("\n▶ Available Commands:")  # Header for the command list.
    print(" ")
    print("   n       → Move To Next Color")  # Increment the current color index by 1.
    print("   p       → Move To Previous Color")  # Decrement the current color index by 1.
    print("   j       → Jump To Custom HEX")  # Jump to a user-specified hex color.
    print("   i       → Jump to Decimal Index (0 To 16777215)")  # Jump to a user-specified decimal index.
    print("   r       → Jump To Random Color")  # Jump to a random color.
    print("   m       → Mix Color With HEX")  # Mix the current color with a user-specified hex color.
    print("   mixr    → Mix With Random Color")  # Mix the current color with a random color.
    print("   mixi    → Mix With Decimal Index (0 To 16777215)")  # Mix the current color with a color from a decimal index.
    print("   grad    → Gradient From Current To Specific HEX")  # Generate a gradient from the current color to another hex.
    print("   cs      → Show Color Harmony Scheme For Current Color")  # Generate a color scheme for the current color.
    print("   export  → Export Current Color To JSON (path: /storage/emulated/0/hexplorer.json/filename.json)")  # Export current color data to JSON.
    print("   cb      → Color Blindness Simulation Of Current Color")  # Simulate color blindness for the current color.
    print("   rcs     → Generate Random Color Schemes")  # Generate a random color and its schemes.
    print("   help    → Show This Help Menu")  # Display this help menu.
    print("   q       → Quit Or CTRL+C + Enter")  # Exit the program.

# Main function to run the interactive Hexplorer tool.
def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("""
HEXPLORER - Terminal HEX Color Explorer

Usage:
  hexplorer           Start the interactive color tool
  hexplorer --help    Show this help message

Features:
  • View HEX & RGB colors
  • Mix, Gradient, Color Schemes
  • Export to JSON
  • Simulate Color Blindness
  • 24-bit Truecolor Terminal Output

Interactive Commands (Inside The Tool):
  n, p, j, i, r, m, mixr, mixi, grad, cs, export, cb, rcs, help, q
        """)
        sys.exit(0)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")  # Display a decorative header.
    print("\n📘 Welcome To HEXPLORER - A Tool To Explore Colors By HEX And Decimal")  # Welcome message.
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")  # Another decorative header.
    show_help()  # Display the help menu.
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")  # Separator.
    print(f"🔢 Color Index Range: 0 to {MAX_DEC} (Total: 16777216 colors)")  # Show the range of possible colors.
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")  # Separator.
    current_dec = ask_start_hex()  # Prompt the user for a starting hex color and convert to decimal.

    while True:  # Main loop for user interaction.
        current_hex = f"{current_dec:06X}"  # Convert current decimal index to hex.
        neg_hex = f"{MAX_DEC - current_dec:06X}"  # Calculate the negative (complementary) color.

        print(f"\n🎨 Current Color   : #{current_hex}")  # Display the current color.
        print_color_block(current_hex)  # Show the current color block.
        print(f"🔄 Negative Color  : #{neg_hex}")  # Display the negative color.
        print_color_block(neg_hex)  # Show the negative color block.
        print(f"🔢 Decimal Index   : {current_dec} / {MAX_DEC}")  # Show the current decimal index.
        show_tech_info(current_hex)  # Display technical info for the current color.

        cmd = input("\nType [n/p/j/i/r/m/mixr/mixi/name/grad/cs/export/cb/rcs/help/q]: ").strip().lower()  # Prompt for a command.

        if cmd == "n":  # Move to the next color.
            current_dec = min(current_dec + 1, MAX_DEC)  # Increment index, but don't exceed MAX_DEC.
        elif cmd == "p":  # Move to the previous color.
            current_dec = max(current_dec - 1, 0)  # Decrement index, but don't go below 0.
        elif cmd == "j":  # Jump to a specific hex color.
            hx = input("Jump To Hex (Without #, e.g., FF0000): ").strip().lstrip("#")  # Prompt for hex code.
            if is_valid_hex(hx):  # Validate the input.
                current_dec = int(hx.upper(), 16)  # Convert to decimal and update current index.
            else:
                print("❌ Invalid HEX entered.")  # Display error for invalid input.
        elif cmd == "i":  # Jump to a specific decimal index.
            idx = input("Jump To Index (0 To 16777215): ").strip()  # Prompt for decimal index.
            if idx.isdigit():  # Check if input is a valid number.
                current_dec = min(max(int(idx), 0), MAX_DEC)  # Clamp index to valid range.
            else:
                print("❌ Invalid index entered.")  # Display error for invalid input.
        elif cmd == "r":  # Jump to a random color.
            current_dec = random.randint(0, MAX_DEC)  # Set index to a random value.
        elif cmd == "m":  # Mix with a specific hex color.
            hx2 = input("Second HEX To Mix (Without #, e.g., FF0000): ").strip().lstrip("#")  # Prompt for second hex.
            if is_valid_hex(hx2):  # Validate the input.
                mix_colors(current_hex, hx2.upper())  # Mix the colors.
            else:
                print("❌ Invalid HEX entered.")  # Display error for invalid input.
        elif cmd == "mixr":  # Mix with a random color.
            rand_hex = f"{random.randint(0, MAX_DEC):06X}"  # Generate a random hex color.
            print(f"🎲 Random HEX to Mix: #{rand_hex}")  # Display the random color.
            mix_colors(current_hex, rand_hex)  # Mix the colors.
        elif cmd == "mixi":  # Mix with a color from a decimal index.
            idx2 = input("Enter Decimal Index To Mix (0 To 16777215): ").strip()  # Prompt for index.
            if idx2.isdigit():  # Check if input is a valid number.
                mix_colors(current_hex, f"{int(idx2):06X}")  # Mix with the specified index color.
            else:
                print("❌ Invalid index entered.")  # Display error for invalid input.
        elif cmd == "grad":  # Generate a gradient to another hex color.
            hx2 = input("Second HEX For Gradient (Without #, e.g., FF0000): ").strip().lstrip("#")  # Prompt for second hex.
            if is_valid_hex(hx2):  # Validate the input.
                steps = input("Steps (default 5): ").strip()  # Prompt for number of steps.
                steps = int(steps) if steps.isdigit() else 5  # Use default of 5 if input is invalid.
                generate_gradient(current_hex, hx2.upper(), steps)  # Generate the gradient.
            else:
                print("❌ Invalid HEX entered.")  # Display error for invalid input.
        elif cmd == "cs":  # Generate a color scheme.
            generate_scheme(current_hex)  # Generate and display the color scheme.
        elif cmd == "export":  # Export the current color to JSON.
            export_color(current_hex, current_dec)  # Export the current color data.
        elif cmd == "cb":  # Simulate color blindness.
            simulate_color_blindness(current_hex)  # Run the color blindness simulation.
        elif cmd == "rcs":  # Generate random color schemes.
            generate_random_scheme()  # Generate and display random color schemes.
        elif cmd == "help":  # Show the help menu.
            show_help()  # Display the command list.
        elif cmd == "q":  # Quit the program.
            print("👋 Goodbye From Hexplorer!")  # Display goodbye message.
            break  # Exit the loop and end the program.
        else:
            print("❓ Unknown Command, Type `help` To List All Commands.")  # Handle invalid commands.

# Standard Python idiom to run the main function when the script is executed directly.
if __name__ == "__main__":
    ensure_termux_storage()
    if "--help" in sys.argv:
        print_cli_help()
    elif "--version" in sys.argv:
        print(f"Hexplorer version {VERSION}")
    else:
        main()
