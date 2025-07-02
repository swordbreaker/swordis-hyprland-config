#!/usr/bin/env python3

import argparse
import subprocess
import datetime
import os
import sys
import time

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
        result = subprocess.run(["pkill", "-INT", "-x", "wf-recorder"])
        if result.returncode == 0:
            subprocess.run(["notify-send", "⏹️ Recording Stopped", "Recording has been stopped and saved", "-t", "3000"])
            print("Recording stopped")
        else:
            subprocess.run(["notify-send", "ℹ️ No Recording", "No active recording found", "-t", "2000"])
            print("No active recording found")
        return True
    except Exception as e:
        subprocess.run(["notify-send", "❌ Error", f"Error stopping recording: {e}", "-t", "3000"])
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
    parser.add_argument('--status', action='store_true', help='Check if recording is currently running')
    args = parser.parse_args()

    # Check recording status if requested
    if args.status:
        if is_recorder_running():
            print("📹 Recording is currently active")
            subprocess.run(["notify-send", "📹 Recording Status", "Recording is currently active", "-t", "2000"])
        else:
            print("⭕ No recording is currently active")
            subprocess.run(["notify-send", "⭕ Recording Status", "No recording is currently active", "-t", "2000"])
        sys.exit(0)

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
    
    # Send notification that recording is starting
    subprocess.run(["notify-send", "wf-recorder", "Select a screen or region to record", "-t", "2000"])

    if args.region:
        # Use slurp to select a region and get the geometry
        print("Please select a region to record...")
        try:
            slurp_result = subprocess.run(["slurp"], capture_output=True, text=True)
            if slurp_result.returncode != 0:
                print("Region selection cancelled or failed")
                return
            geometry = slurp_result.stdout.strip()
            cmd.extend(["-g", geometry])
            
            # Give time for slurp UI to disappear
            print("Starting recording in 2 seconds...")
            subprocess.run(["notify-send", "⏱️ Recording Starts Soon", "Recording will start in 2 seconds...", "-t", "2000"])
            time.sleep(2)
            
        except Exception as e:
            print(f"Error getting region geometry: {e}")
            return
    else:
        # Use slurp to select which screen to record
        print("Please select a screen to record...")
        try:
            slurp_result = subprocess.run(["slurp", "-o", "-f", "%o"], capture_output=True, text=True)
            if slurp_result.returncode != 0:
                print("Screen selection cancelled or failed")
                return
            output_name = slurp_result.stdout.strip()
            cmd.extend(["--output", output_name])
            
            # Give time for slurp UI to disappear
            print("Starting recording in 2 seconds...")
            subprocess.run(["notify-send", "⏱️ Recording Starts Soon", "Recording will start in 2 seconds...", "-t", "2000"])
            time.sleep(2)
            
        except Exception as e:
            print(f"Error getting screen output: {e}")
            return
    
    if args.audio:
        cmd.append("--audio")
    
    cmd.append(f"--file={filename}")
    
    # Execute the command
    print(f"Starting recording to {filename}...")
    print(f"Press Ctrl+C to stop recording or run this script again")
    
    try:
        # Start the recording process
        process = subprocess.Popen(cmd)
        
        # Send notification that recording has started
        subprocess.run(["notify-send", "🔴 Recording Started", f"Recording in progress...\nFile: {os.path.basename(filename)}", "-t", "3000"])
        
        # Wait for the process to complete
        process.wait()
        
        # Send notification that recording has finished
        subprocess.run(["notify-send", "✅ Recording Completed", f"Recording saved as:\n{filename}", "-t", "5000"])
        print(f"Recording saved as {filename}")
        
    except KeyboardInterrupt:
        print("\nRecording stopped by user")
        subprocess.run(["notify-send", "⏹️ Recording Stopped", "Recording stopped by user", "-t", "3000"])
    except Exception as e:
        print(f"Error during recording: {e}")
        subprocess.run(["notify-send", "❌ Recording Error", f"Error: {e}", "-t", "5000"])

if __name__ == "__main__":
    main()