"""Main entry point for the Move Automation application.

This module orchestrates the user interface, input validation, directory scanning,
file filtering, and file movement operations.
"""

import os
import sys
from collections.abc import Callable
import time
# Import components from your project modules
from files_scanner import iter_files
from filter import ExtensionFileFilter
from move_operation import move_file, MoveStatus
from ui import (
	Menu,
	MenuItem,
	MessageType,
	display_divider,
	display_header,
	display_menu,
	display_message,
	prompt_menu_selection,
	get_validated_input,
)
from utility import clear_screen, pause
from validation import (
	is_not_blank,
	is_valid_srcdir,
	is_different_from_source,
	is_not_existing_file,
)
# ====================
# Global Configuration
# ====================
APPLICATION_TITLE: str = "Move Automation"

# ==================
# UI Pages & Actions
# ==================
def run_automation_page() -> None:
	"""The workflow page for scanning, filtering, and moving files."""
	display_header("Run Move Automation")

	# 1. Acquire Source Directory
	source_dir = get_validated_input(
		"\nEnter the Source Path (Absolute or Relative): ", 
		[is_not_blank, is_valid_srcdir]
	)
	print("\nSource Directory is:", os.path.abspath(source_dir))
	time.sleep(0.5)
	display_divider()
	
	# 2. Acquire Destination Directory
	
	dest_dir = get_validated_input(
		"\nEnter the Destination Path: ", 
		[is_not_blank, is_not_existing_file, is_different_from_source(source_dir)]
	)
	time.sleep(0.5)
	display_divider()

	# 4. Execution Pipeline
	try:
		clear_screen()
		display_header("Processing Files")

		# Lazy file scanning
		scanned_files = iter_files(source_dir)

		# File filtering configuration
		file_filter = ExtensionFileFilter(["jpg"])
		matched_files = list(file_filter.apply(scanned_files))

		if not matched_files:
			display_message("No files matching your criteria were found in the source directory.", MessageType.NOTE)
			pause()
			return

		display_message(f"Found {len(matched_files)} matching file(s). Initiating transfer...\n", MessageType.INFO)

		# File movement loop execution
		success_count = 0
		for file_path in matched_files:
			file_name = os.path.basename(file_path)
			
			
			result = move_file(file_path, dest_dir, overwrite=False)

			match result.status:
				case MoveStatus.SUCCESS:
					display_message(f"Successfully Moved: {file_name}", MessageType.SUCCESS)
					success_count += 1

				case MoveStatus.CONFLICT_ALREADY_EXISTS:
					
					display_message(f"Conflict detected for {file_name}. Resolving by renaming...", MessageType.WARNING)
					
					name, ext = os.path.splitext(file_name)
					timestamped_name = f"{name}_backup_{int(time.time())}{ext}"
					
					
					temp_source_path = os.path.join(os.path.dirname(file_path), timestamped_name)
					os.rename(file_path, temp_source_path)
					
					
					retry_result = move_file(temp_source_path, dest_dir)
					if retry_result.status == MoveStatus.SUCCESS:
						display_message(f"Successfully resolved conflict. Moved as: {timestamped_name}", MessageType.SUCCESS)
						success_count += 1
					else:
						display_message(f"Failed to resolve conflict for {file_name}: {retry_result.message}", MessageType.ERROR)

				case MoveStatus.PERMISSION_DENIED:
					display_message(f"Skipped [{file_name}]: Admin/Permission privileges required.", MessageType.ERROR)

				case MoveStatus.SOURCE_NOT_FOUND:
					display_message(f"Skipped [{file_name}]: File vanished during processing.", MessageType.WARNING)

				case MoveStatus.SYSTEM_ERROR:
					display_message(f"Critical System Failure on [{file_name}]: {result.message}", MessageType.ERROR)

		# Summary reports
		display_message(
			f"\nAutomation Completed. Moved {success_count} out of {len(matched_files)} files.",
			MessageType.SUCCESS if success_count == len(matched_files) else MessageType.WARNING
		)

	except Exception as general_error:
		
		display_message(f"An unexpected technical failure occurred: {general_error}", MessageType.ERROR)

	pause()


def show_guidelines_page() -> None:
	"""Display simple operating instructions to the end-user."""
	
	display_header("Guidelines & Manual")
	print("Welcome to the Move Automation Assistant!\n")
	print("This utility helps you safely migrate files based on their formats.")
	print("Key Rules:")
	print("  * Source Paths must point to existing directories on your machine.")
	print("  * If the destination directory does not exist, the app creates it dynamically.")
	print("  * You can filter formats globally or target specific types like 'txt' or 'png'.")
	print("  * To safely abort the application at any prompt, press Ctrl+C.")
	print("\n" + "=" * 20)
	pause()


def terminate_application() -> None:
	"""Exit the running runtime loop cleanly."""
	
	display_message("Thank you for using Move Automation. Goodbye!")
	sys.exit(0)


# ===============================
# Application Lifecycle Core Loop
# ===============================
def main() -> None:
	"""Bootstrap and maintain the primary execution loop of the app."""
	# Instantiate the structural main menu component configuration
	main_menu = Menu(
		title="Main Menu",
		options=(
			MenuItem("Start Automation Process", run_automation_page),
			MenuItem("Read Operational Guidelines", show_guidelines_page),
			MenuItem("Exit Application Instance", terminate_application),
		)
	)

	while True:
		clear_screen()
		display_header(APPLICATION_TITLE)
		display_menu(main_menu)
		
		# Interactively prompt and execute callbacks dynamically
		selected_item = prompt_menu_selection(main_menu)
		if selected_item.action:
			clear_screen()
			selected_item.action()


if __name__ == "__main__":
	main()

