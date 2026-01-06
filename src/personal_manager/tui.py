#!/usr/bin/env python3

import subprocess
import sys
from typing import List

try:
    from textual.app import App, ComposeResult
    from textual.containers import Horizontal, Vertical
    from textual.widgets import Button, Input, Static, Footer, Header
    from textual.reactive import reactive
    from textual.binding import Binding
except ImportError:
    print("Error: textual package not found. Please install it with: pip install textual")
    sys.exit(1)


class OutputDisplay(Static):
    """Widget to display command output"""
    
    def clear_output(self):
        """Clear the output display"""
        self.update("")


class PersonalManagerTUI(App):
    """Textual TUI for Personal Manager"""
    
    CSS_PATH = "styles.tcss"
    TITLE = "Personal Manager"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("c", "clear", "Clear Output"),
        Binding("escape", "focus_menu", "Focus Menu"),
    ]
    
    current_output = reactive("")
    
    def compose(self) -> ComposeResult:
        """Compose the UI"""
        yield Header()
        with Horizontal():
            with Vertical(id="menu-container"):
                yield Static("Menu", classes="title")
                yield Button("Shell Commands", id="shell-btn", variant="primary")
                yield Button("Task List", id="task-list-btn")
                yield Button("Add Task", id="add-task-btn")
                yield Button("Time Summary", id="time-summary-btn")
                yield Button("Start Time", id="start-time-btn")
                yield Button("Stop Time", id="stop-time-btn")
            with Vertical(id="main-container"):
                with Vertical(id="shell-container", classes="hidden"):
                    yield Static("Shell Command Input", classes="title")
                    yield Input(placeholder="Enter shell command...", id="shell-input")
                    yield Button("Execute", id="execute-btn", variant="success")
                yield Static("Output", classes="title")
                yield OutputDisplay(id="output-display", classes="output")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        button_id = event.button.id
        
        if button_id == "shell-btn":
            self.show_shell_interface()
        elif button_id == "execute-btn":
            self.execute_shell_command()
        elif button_id == "task-list-btn":
            self.execute_task_command("list")
        elif button_id == "add-task-btn":
            self.show_message("Add task functionality - integrate with taskwarrior")
        elif button_id == "time-summary-btn":
            self.execute_time_command("summary")
        elif button_id == "start-time-btn":
            self.show_message("Time start functionality - integrate with timewarrior")
        elif button_id == "stop-time-btn":
            self.show_message("Time stop functionality - integrate with timewarrior")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission"""
        if event.input.id == "shell-input":
            self.execute_shell_command()
    
    def show_shell_interface(self) -> None:
        """Show the shell command interface"""
        shell_container = self.query_one("#shell-container")
        shell_input = self.query_one("#shell-input")
        
        # Hide all other containers
        self.hide_all_interfaces()
        
        # Show shell container
        shell_container.remove_class("hidden")
        shell_input.focus()
    
    def hide_all_interfaces(self) -> None:
        """Hide all interface containers"""
        shell_container = self.query_one("#shell-container")
        shell_container.add_class("hidden")
    
    def execute_shell_command(self) -> None:
        """Execute shell command and display output"""
        shell_input = self.query_one("#shell-input")
        output_display = self.query_one("#output-display")
        
        command = shell_input.value.strip()
        if not command:
            self.show_message("Please enter a shell command")
            return
        
        # Parse command
        cmd_parts = command.split()
        
        try:
            result = subprocess.run(
                cmd_parts,
                check=True,
                text=True,
                capture_output=True
            )
            
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += f"STDERR:\n{result.stderr}"
            
            if not output:
                output = "Command executed successfully (no output)"
            
            output_display.update(f"$ {command}\n{output}")
            
        except subprocess.CalledProcessError as e:
            output = f"Command failed with exit code {e.returncode}\n"
            if e.stdout:
                output += f"STDOUT:\n{e.stdout}\n"
            if e.stderr:
                output += f"STDERR:\n{e.stderr}"
            output_display.update(f"$ {command}\n{output}")
        except FileNotFoundError:
            output_display.update(f"$ {command}\nCommand not found: {cmd_parts[0]}")
        except Exception as e:
            output_display.update(f"$ {command}\nError: {e}")
    
    def execute_task_command(self, action: str) -> None:
        """Execute task-related commands"""
        output_display = self.query_one("#output-display")
        
        if action == "list":
            cmd_parts = ["task", "list"]
            self._execute_and_display(cmd_parts, output_display)
    
    def execute_time_command(self, action: str) -> None:
        """Execute time-related commands"""
        output_display = self.query_one("#output-display")
        
        if action == "summary":
            cmd_parts = ["timew", "summary"]
            self._execute_and_display(cmd_parts, output_display)
    
    def _execute_and_display(self, cmd_parts: List[str], output_display: OutputDisplay) -> None:
        """Execute command and display output"""
        try:
            result = subprocess.run(
                cmd_parts,
                check=True,
                text=True,
                capture_output=True
            )
            
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += f"STDERR:\n{result.stderr}"
            
            if not output:
                output = f"Command {' '.join(cmd_parts)} executed successfully (no output)"
            
            output_display.update(f"$ {' '.join(cmd_parts)}\n{output}")
            
        except subprocess.CalledProcessError as e:
            output = f"Command failed with exit code {e.returncode}\n"
            if e.stdout:
                output += f"STDOUT:\n{e.stdout}\n"
            if e.stderr:
                output += f"STDERR:\n{e.stderr}"
            output_display.update(f"$ {' '.join(cmd_parts)}\n{output}")
        except FileNotFoundError:
            output_display.update(f"$ {' '.join(cmd_parts)}\nCommand not found: {cmd_parts[0]}")
        except Exception as e:
            output_display.update(f"$ {' '.join(cmd_parts)}\nError: {e}")
    
    def show_message(self, message: str) -> None:
        """Show a message in the output display"""
        output_display = self.query_one("#output-display")
        output_display.update(message)
    
    def action_clear(self) -> None:
        """Clear the output display"""
        output_display = self.query_one("#output-display")
        output_display.clear_output()
    
    def action_focus_menu(self) -> None:
        """Focus back to the menu"""
        self.hide_all_interfaces()
        shell_btn = self.query_one("#shell-btn")
        shell_btn.focus()


def main():
    """Main entry point for the TUI"""
    app = PersonalManagerTUI()
    app.run()


if __name__ == "__main__":
    main()