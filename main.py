# main.py
import tkinter as tk
from gui import ChatGUI
from claude_client import ClaudeClient
import configparser

def main():
    # Read configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get API key from config
    api_key = config['API']['api_key']

    # Create main window
    root = tk.Tk()
    
    # Set window size from config
    initial_width = config.getint('GUI', 'initial_width')
    initial_height = config.getint('GUI', 'initial_height')
    root.geometry(f"{initial_width}x{initial_height}")
    
    # Set minimum window size from config
    min_width = config.getint('GUI', 'min_width')
    min_height = config.getint('GUI', 'min_height')
    root.minsize(min_width, min_height)

    # Create Claude client
    claude_client = ClaudeClient(api_key)

    # Create and run GUI
    chat_gui = ChatGUI(root, claude_client, config)
    root.mainloop()

if __name__ == "__main__":
    main()