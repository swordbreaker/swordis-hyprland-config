#!/usr/bin/env python3

import argparse
import subprocess
import datetime
import os
import sys

def is_recorder_running():
    """Check if wf-recorder is already running"""
    try:
        result = subprocess.run(["pgrep", "-x", "wf-recorder"], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def stop_recording():
    """Stop any running wf-recorder process"""
    try:
        subprocess.run(["pkill", "-INT", "-x", "wf-recorder"])
        subprocess.run(["notify-send", "wf-recorder", "Recording stopped"])
        print("Recording stopped")
        return True
    except Exception as e:
        print(f"Error stopping recording: {e}")
        return False

def main():
    # Check if recording is already running
    if is_recorder_running():
        stop_recording()
        sys.exit(0)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Screen recorder script')
    parser.add_argument('--audio', action='store_true', help='Record with audio (default: False)')
    parser.add_argument('--region', action='store_true', help='Record a specific region (default: False)')
    args = parser.parse_args()

    # Generate timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Create proper path with expanded home directory
    save_dir = os.path.expanduser("~/Videos/Screencasting")
    
    # Ensure the directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Create absolute path for the output file
    filename = os.path.join(save_dir, f"recording-{timestamp}.mp4")

    # Build the wf-recorder command based on arguments
    cmd = ["wf-recorder"]
    
    if args.region:
        # Use slurp to select a region
        cmd.extend(["-g", "$(slurp)"])
    else:
        # Use slurp to select which screen to record
        cmd.extend(["--output", "$(slurp -o -f \"%o\")"])
    
    if args.audio:
        cmd.append("--audio")
    
    cmd.append(f"--file={filename}")
    
    # Send notification that recording is starting
    subprocess.run(["notify-send", "wf-recorder", "Select a screen or region to record"])
    
    # Execute the command
    print(f"Starting recording to {filename}...")
    print(f"Press Ctrl+C to stop recording or run this script again")
    
    # Convert the command list to a shell command string for proper expansion of $(slurp)
    shell_cmd = " ".join(cmd)
    
    try:
        subprocess.run(shell_cmd, shell=True)
        print(f"Recording saved as {filename}")
    except KeyboardInterrupt:
        print("\nRecording stopped")
    except Exception as e:
        print(f"Error during recording: {e}")

if __name__ == "__main__":
    main()