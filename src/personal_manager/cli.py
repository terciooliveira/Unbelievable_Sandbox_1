#!/usr/bin/env python3

import argparse
import subprocess
import sys
from typing import List


class PersonalManager:
    def __init__(self):
        self.parser = self._setup_parser()
    
    def _setup_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Personal Manager - CLI task and project organizer",
            prog="pm"
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Shell command
        shell_parser = subparsers.add_parser("shell", help="Execute shell commands")
        shell_parser.add_argument("cmd", nargs="+", help="Shell command to execute")
        
        # Task commands (placeholder for taskwarrior integration)
        task_parser = subparsers.add_parser("task", help="Task management")
        task_subparsers = task_parser.add_subparsers(dest="task_action")
        
        task_subparsers.add_parser("list", help="List tasks")
        task_subparsers.add_parser("add", help="Add task")
        
        # Time commands (placeholder for timewarrior integration)
        time_parser = subparsers.add_parser("time", help="Time tracking")
        time_subparsers = time_parser.add_subparsers(dest="time_action")
        
        time_subparsers.add_parser("start", help="Start time tracking")
        time_subparsers.add_parser("stop", help="Stop time tracking")
        time_subparsers.add_parser("summary", help="Show time summary")
        
        return parser
    
    def execute_shell_command(self, cmd: List[str]) -> int:
        """Execute shell command using fish and display output with terminal colors"""
        try:
            # Check if fish is available
            fish_check = subprocess.run(["which", "fish"], capture_output=True, text=True)
            shell_cmd = "fish" if fish_check.returncode == 0 else "bash"
            
            # Execute command with fish to preserve colors
            full_cmd = [shell_cmd, "-c", " ".join(cmd)]
            
            result = subprocess.run(
                full_cmd,
                check=True,
                text=False,  # Keep binary to preserve ANSI color codes
                capture_output=True
            )
            
            # Print stdout with colors preserved
            if result.stdout:
                sys.stdout.buffer.write(result.stdout)
                sys.stdout.flush()
            
            # Print stderr with colors preserved
            if result.stderr:
                sys.stderr.buffer.write(result.stderr)
                sys.stderr.flush()
            
            return result.returncode
            
        except subprocess.CalledProcessError as e:
            # Print stdout with colors preserved
            if e.stdout:
                sys.stdout.buffer.write(e.stdout)
                sys.stdout.flush()
            # Print stderr with colors preserved
            if e.stderr:
                sys.stderr.buffer.write(e.stderr)
                sys.stderr.flush()
            return e.returncode
        except FileNotFoundError:
            print(f"Command not found: {cmd[0]}", file=sys.stderr)
            return 1
    
    def handle_task_command(self, args):
        """Handle task-related commands"""
        if args.task_action == "list":
            self.execute_shell_command(["task", "list"])
        elif args.task_action == "add":
            print("Task add functionality - integrate with taskwarrior")
        else:
            print("Unknown task action")
    
    def handle_time_command(self, args):
        """Handle time-related commands"""
        if args.time_action == "start":
            print("Time start functionality - integrate with timewarrior")
        elif args.time_action == "stop":
            print("Time stop functionality - integrate with timewarrior")
        elif args.time_action == "summary":
            self.execute_shell_command(["timew", "summary"])
        else:
            print("Unknown time action")
    
    def run(self, args: List[str] | None = None) -> int:
        """Main entry point"""
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return 0
        
        try:
            if parsed_args.command == "shell":
                return self.execute_shell_command(parsed_args.cmd)
            elif parsed_args.command == "task":
                self.handle_task_command(parsed_args)
            elif parsed_args.command == "time":
                self.handle_time_command(parsed_args)
            else:
                print(f"Unknown command: {parsed_args.command}")
                return 1
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 130
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        
        return 0


def main():
    """Main entry point for the CLI"""
    try:
        from .tui import main as tui_main
        tui_main()
    except ImportError as e:
        print(f"Error importing TUI: {e}")
        print("Falling back to CLI mode...")
        pm = PersonalManager()
        sys.exit(pm.run())


if __name__ == "__main__":
    main()