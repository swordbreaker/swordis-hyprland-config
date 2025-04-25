from enum import Enum
import subprocess
import argparse

class Modes(Enum):
    Output = "output" # take screenshot of an entire monitor
    Region = "region" # take screenshot of a selected region
    Window = "window" # take screenshot of a selected window
    Active = "active" # take screenshot of the active window

class Methods(Enum):
    HyprShot = "hyprshot" # use hyprshot and satty
    Grim = "grim" # use slurp, grim, and wl-copy

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Take screenshots with hyprshot and satty')
    parser.add_argument('-m', '--mode', 
                        choices=[m.value for m in Modes], 
                        default='region',
                        help='Screenshot mode: output (entire monitor), region (selected area), window (selected window), or active (active window)')
    parser.add_argument('--method',
                        choices=[m.value for m in Methods],
                        default='grim',
                        help='Screenshot method: hyprshot (hyprshot+satty) or grim (slurp+grim+wl-copy)')
    
    args = parser.parse_args()
    
    # Get the mode from arguments or use default
    mode_value = args.mode
    method_value = args.method
    
    # Convert string to Enum
    mode = next((m for m in Modes if m.value == mode_value), Modes.Region)
    method = next((m for m in Methods if m.value == method_value), Methods.HyprShot)
    
    print(f"Taking screenshot in {mode.value} mode using {method.value} method...")
    
    if method == Methods.HyprShot:
        # Using shell=True because we need to pipe the output
        subprocess.run(f"hyprshot -m {mode.value} --raw --clipboard-only | satty --filename -", shell=True)
    elif method == Methods.Grim:
        if mode == Modes.Region:
            # Use slurp, grim, and wl-copy for region captures
            subprocess.run("region=$(slurp) && sleep 0.4 && grim -g \"$region\" - | wl-copy", shell=True, executable="/bin/bash")
        else:
            subprocess.run("grim - | wl-copy", shell=True, executable="/bin/bash")


if __name__ == "__main__":
    main()