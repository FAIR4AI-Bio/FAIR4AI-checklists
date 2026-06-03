"""
FAIR4AI Agent - Graphical User Interface

A user-friendly GUI for running FAIR4AI dataset evaluations.
Allows selection of metadata files, configuration of settings, and
displays progress in real-time.

Usage:
    python fair4ai_agent_ui.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import os
import sys
import threading
from pathlib import Path
from fair4ai_agent import FAIR4AIAgent


class FAIR4AIAgentUI:
    """Graphical user interface for the FAIR4AI evaluation agent."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("FAIR4AI Dataset Evaluation Agent")
        self.root.geometry("900x800")
        
        # Variables
        self.metadata_files = []
        self.running = False
        
        # Create UI
        self.create_widgets()
        
        # Load defaults from environment variables
        self.load_defaults()
    
    def create_widgets(self):
        """Create all UI widgets."""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Title
        title = ttk.Label(main_frame, text="FAIR4AI Dataset Evaluation Agent", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # ===== Input Files Section =====
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(main_frame, text="INPUT SOURCE", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # Input mode selection
        self.input_mode_var = tk.StringVar(value="files")
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        ttk.Radiobutton(mode_frame, text="Metadata Files", variable=self.input_mode_var, 
                       value="files", command=self.toggle_input_mode).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Dataset URL", variable=self.input_mode_var, 
                       value="url", command=self.toggle_input_mode).pack(side=tk.LEFT, padx=10)
        row += 1
        
        # Metadata files (shown when mode is "files")
        self.files_label = ttk.Label(main_frame, text="Metadata Files:")
        self.files_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.metadata_listbox = tk.Listbox(main_frame, height=4, width=60)
        self.metadata_listbox.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.files_btn_frame = ttk.Frame(main_frame)
        self.files_btn_frame.grid(row=row, column=2, sticky=tk.W, padx=5)
        ttk.Button(self.files_btn_frame, text="Add Files...", command=self.add_metadata_files).pack(side=tk.TOP, pady=2)
        ttk.Button(self.files_btn_frame, text="Clear", command=self.clear_metadata_files).pack(side=tk.TOP, pady=2)
        row += 1
        
        # Dataset URL (shown when mode is "url")
        self.url_row = row
        self.url_label = ttk.Label(main_frame, text="Dataset URL:")
        self.dataset_url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.dataset_url_var, width=50)
        self.url_hint_label = ttk.Label(main_frame, text="(landing page)")

        self.url_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.url_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        self.url_hint_label.grid(row=row, column=2, sticky=tk.W, padx=5)
        # Default to hidden until URL mode is selected
        self.url_label.grid_remove()
        self.url_entry.grid_remove()
        self.url_hint_label.grid_remove()
        row += 1
        
        # Form questions file
        ttk.Label(main_frame, text="Form Questions CSV:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.form_csv_var = tk.StringVar(value="form_ai_checklist_automated.csv")
        ttk.Entry(main_frame, textvariable=self.form_csv_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.browse_form_csv).grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        # ===== Configuration Section =====
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        ttk.Label(main_frame, text="CONFIGURATION", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # LLM Provider
        ttk.Label(main_frame, text="LLM Provider:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.provider_var = tk.StringVar(value="azure")
        provider_frame = ttk.Frame(main_frame)
        provider_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(provider_frame, text="OpenAI", variable=self.provider_var, value="openai").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(provider_frame, text="Azure OpenAI", variable=self.provider_var, value="azure").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(provider_frame, text="Anthropic Claude", variable=self.provider_var, value="anthropic").pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Model/Deployment name
        ttk.Label(main_frame, text="Model/Deployment:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.model_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(main_frame, text="(optional)").grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        # Azure endpoint
        ttk.Label(main_frame, text="Azure Endpoint:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.azure_endpoint_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.azure_endpoint_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(main_frame, text="(optional)").grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        # Azure API version
        ttk.Label(main_frame, text="Azure API Version:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.azure_api_version_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.azure_api_version_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(main_frame, text="(optional)").grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        # Dataset name
        ttk.Label(main_frame, text="Dataset Name:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.dataset_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.dataset_name_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(main_frame, text="(auto-detect)").grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        # ===== Output Section =====
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        ttk.Label(main_frame, text="OUTPUT", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # Output directory
        ttk.Label(main_frame, text="Output Directory:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        ttk.Entry(main_frame, textvariable=self.output_dir_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        output_dir_btn_frame = ttk.Frame(main_frame)
        output_dir_btn_frame.grid(row=row, column=2, sticky=tk.W, padx=5)
        ttk.Button(output_dir_btn_frame, text="Browse...", command=self.browse_output_dir).pack(side=tk.TOP, pady=2)
        ttk.Button(output_dir_btn_frame, text="New Folder...", command=self.create_new_folder).pack(side=tk.TOP, pady=2)
        row += 1
        
        # Output prefix
        ttk.Label(main_frame, text="Output File Prefix:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.output_prefix_var = tk.StringVar(value="fair4ai_evaluation")
        ttk.Entry(main_frame, textvariable=self.output_prefix_var, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(main_frame, text="(filename)").grid(row=row, column=2, sticky=tk.W, padx=5)
        row += 1
        
        # Output info
        self.output_info_label = ttk.Label(main_frame, text="", foreground="gray")
        self.output_info_label.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        # ===== Progress Section =====
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        ttk.Label(main_frame, text="PROGRESS", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100, length=400)
        self.progress_bar.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Progress text
        self.progress_text = scrolledtext.ScrolledText(main_frame, height=12, width=80, wrap=tk.WORD)
        self.progress_text.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.progress_text.config(state=tk.DISABLED)
        main_frame.rowconfigure(row, weight=1)
        row += 1
        
        # ===== Action Buttons =====
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=10)
        
        self.run_button = ttk.Button(button_frame, text="Run Evaluation", command=self.run_evaluation, width=20)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_evaluation, state=tk.DISABLED, width=20)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log, width=20).pack(side=tk.LEFT, padx=5)
        
        # Update output info when prefix changes
        self.output_prefix_var.trace('w', self.update_output_info)
        self.output_dir_var.trace('w', self.update_output_info)
        
        # Set initial input mode
        self.toggle_input_mode()
    
    def toggle_input_mode(self):
        """Toggle between file and URL input modes."""
        mode = self.input_mode_var.get()
        
        if mode == "files":
            # Show file controls
            self.files_label.grid()
            self.metadata_listbox.grid()
            self.files_btn_frame.grid()
            # Hide URL controls
            self.url_label.grid_remove()
            self.url_entry.grid_remove()
            self.url_hint_label.grid_remove()
        else:
            # Hide file controls
            self.files_label.grid_remove()
            self.metadata_listbox.grid_remove()
            self.files_btn_frame.grid_remove()
            # Show URL controls
            self.url_label.grid()
            self.url_entry.grid()
            self.url_hint_label.grid()
    
    def load_defaults(self):
        """Load default values from environment variables."""
        # Azure OpenAI defaults
        if os.getenv("OPENAI_ENDPOINT"):
            self.azure_endpoint_var.set(os.getenv("OPENAI_ENDPOINT"))
        
        if os.getenv("OPENAI_DEPLOYMENT"):
            self.model_var.set(os.getenv("OPENAI_DEPLOYMENT"))
        
        if os.getenv("OPENAI_API_VERSION"):
            self.azure_api_version_var.set(os.getenv("OPENAI_API_VERSION"))
        
        # Check which provider is configured
        if os.getenv("OPENAI_SUBSCRIPTION_KEY") or os.getenv("AZURE_OPENAI_API_KEY"):
            self.provider_var.set("azure")
        elif os.getenv("OPENAI_API_KEY"):
            self.provider_var.set("openai")
        elif os.getenv("ANTHROPIC_API_KEY"):
            self.provider_var.set("anthropic")
        
        self.log_message("Loaded defaults from environment variables")
        self.update_output_info()
    
    def add_metadata_files(self):
        """Open file dialog to add metadata files."""
        files = filedialog.askopenfilenames(
            title="Select Metadata Files",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        for file in files:
            if file not in self.metadata_files:
                self.metadata_files.append(file)
                self.metadata_listbox.insert(tk.END, Path(file).name)
        
        if files:
            self.log_message(f"Added {len(files)} metadata file(s)")
    
    def clear_metadata_files(self):
        """Clear all selected metadata files."""
        self.metadata_files.clear()
        self.metadata_listbox.delete(0, tk.END)
        self.log_message("Cleared metadata files")
    
    def browse_form_csv(self):
        """Browse for form questions CSV file."""
        file = filedialog.askopenfilename(
            title="Select Form Questions CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=self.form_csv_var.get()
        )
        if file:
            self.form_csv_var.set(file)
            self.log_message(f"Selected form: {Path(file).name}")
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir_var.get()
        )
        if directory:
            self.output_dir_var.set(directory)
            self.log_message(f"Output directory: {directory}")
    
    def create_new_folder(self):
        """Create a new folder in the output directory."""
        # Simple dialog to get folder name
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Folder")
        dialog.geometry("400x120")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter new folder name:").pack(pady=10)
        folder_name_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=folder_name_var, width=40)
        entry.pack(pady=5)
        entry.focus()
        
        def create_folder():
            folder_name = folder_name_var.get().strip()
            if not folder_name:
                messagebox.showwarning("Invalid Name", "Please enter a folder name")
                return
            
            new_path = Path(self.output_dir_var.get()) / folder_name
            try:
                new_path.mkdir(parents=True, exist_ok=False)
                self.output_dir_var.set(str(new_path))
                self.log_message(f"Created and selected folder: {new_path}")
                dialog.destroy()
            except FileExistsError:
                messagebox.showerror("Error", f"Folder '{folder_name}' already exists")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create folder: {e}")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Create", command=create_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        entry.bind('<Return>', lambda e: create_folder())
    
    def update_output_info(self, *args):
        """Update the output file info label."""
        prefix = self.output_prefix_var.get()
        out_dir = self.output_dir_var.get()
        if prefix:
            json_file = Path(out_dir) / f"{prefix}.json"
            csv_file = Path(out_dir) / f"{prefix}.csv"
            self.output_info_label.config(
                text=f"Will create: {json_file.name} and {csv_file.name}\nin {out_dir}"
            )
    
    def log_message(self, message, tag=None):
        """Add a message to the progress log."""
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, message + "\n")
        if tag:
            # Apply tag formatting if needed
            pass
        self.progress_text.see(tk.END)
        self.progress_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the progress log."""
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.config(state=tk.DISABLED)
        self.progress_var.set(0)
    
    def validate_inputs(self):
        """Validate all inputs before running."""
        mode = self.input_mode_var.get()
        
        if mode == "files":
            if not self.metadata_files:
                messagebox.showerror("Error", "Please select at least one metadata file")
                return False
            
            for metadata_file in self.metadata_files:
                if not Path(metadata_file).exists():
                    messagebox.showerror("Error", f"Metadata file not found: {metadata_file}")
                    return False
        else:  # URL mode
            if not self.dataset_url_var.get():
                messagebox.showerror("Error", "Please enter a dataset URL")
                return False
            
            # Basic URL validation
            url = self.dataset_url_var.get()
            if not url.startswith(('http://', 'https://')):
                messagebox.showerror("Error", "URL must start with http:// or https://")
                return False
        
        if not self.form_csv_var.get():
            messagebox.showerror("Error", "Please select a form questions CSV file")
            return False
        
        if not Path(self.form_csv_var.get()).exists():
            messagebox.showerror("Error", f"Form CSV file not found: {self.form_csv_var.get()}")
            return False
        
        if not self.output_prefix_var.get():
            messagebox.showerror("Error", "Please specify an output file prefix")
            return False
        
        if not self.output_dir_var.get():
            messagebox.showerror("Error", "Please specify an output directory")
            return False
        
        return True
    
    def run_evaluation(self):
        """Run the evaluation in a separate thread."""
        if not self.validate_inputs():
            return
        
        # Disable run button
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.running = True
        
        # Clear log and reset progress
        self.clear_log()
        
        # Run in thread to keep UI responsive
        thread = threading.Thread(target=self._run_evaluation_thread, daemon=True)
        thread.start()
    
    def _run_evaluation_thread(self):
        """Execute the evaluation (runs in separate thread)."""
        try:
            self.log_message("=" * 70)
            self.log_message("Starting FAIR4AI Evaluation")
            self.log_message("=" * 70)
            self.log_message("")
            
            # Get configuration
            provider = self.provider_var.get()
            model = self.model_var.get() if self.model_var.get() else None
            azure_endpoint = self.azure_endpoint_var.get() if self.azure_endpoint_var.get() else None
            azure_api_version = self.azure_api_version_var.get() if self.azure_api_version_var.get() else None
            
            self.log_message(f"Provider: {provider}")
            if model:
                self.log_message(f"Model/Deployment: {model}")
            if provider == "azure":
                self.log_message(f"Azure Endpoint: {azure_endpoint or 'from environment'}")
                self.log_message(f"Azure API Version: {azure_api_version or 'default'}")
            self.log_message("")
            
            # Initialize agent
            self.log_message("Initializing agent...")
            agent = FAIR4AIAgent(
                llm_provider=provider,
                model=model,
                azure_endpoint=azure_endpoint,
                azure_api_version=azure_api_version
            )
            
            # Load form questions
            self.log_message(f"Loading form questions from: {self.form_csv_var.get()}")
            agent.load_form_questions(self.form_csv_var.get())
            self.log_message(f"Loaded {len(agent.form_questions)} questions")
            self.progress_var.set(10)
            
            # Create output directory
            output_dir = Path(self.output_dir_var.get())
            output_dir.mkdir(parents=True, exist_ok=True)
            self.log_message(f"Output directory: {output_dir}")
            
            # Load metadata from URL or files
            mode = self.input_mode_var.get()
            if mode == "url":
                self.log_message("")
                self.log_message(f"Extracting metadata from URL: {self.dataset_url_var.get()}")
                agent.extract_metadata_from_url(self.dataset_url_var.get(), output_dir)
                self.log_message(f"Extracted {len(agent.metadata_content)} metadata source(s)")
            else:
                self.log_message("")
                self.log_message("Loading metadata files:")
                for mf in self.metadata_files:
                    self.log_message(f"  - {Path(mf).name}")
                agent.load_metadata_files(self.metadata_files)
                self.log_message(f"Loaded {len(agent.metadata_content)} metadata file(s)")
            
            self.progress_var.set(20)
            
            # Get dataset name
            dataset_name = self.dataset_name_var.get() if self.dataset_name_var.get() else None
            if not dataset_name:
                # Try to auto-detect
                for content in agent.metadata_content.values():
                    if isinstance(content, list) and len(content) > 0:
                        if '@type' in content[0] and content[0]['@type'] == 'Dataset':
                            dataset_name = content[0].get('name', 'Unknown Dataset')
                            break
                    elif isinstance(content, dict):
                        if content.get('@type') == 'Dataset':
                            dataset_name = content.get('name', 'Unknown Dataset')
                            break
                if dataset_name:
                    self.log_message(f"Auto-detected dataset: {dataset_name}")
            
            self.log_message("")
            self.log_message(f"Evaluating: {dataset_name or 'Unknown Dataset'}")
            self.log_message("")
            
            # Build context
            metadata_context = agent._build_context_prompt()
            
            # Process questions
            self.log_message("Processing questions...")
            responses = []
            total_questions = len(agent.form_questions)
            processed = 0
            
            for idx, row in agent.form_questions.iterrows():
                if not self.running:
                    self.log_message("")
                    self.log_message("Evaluation stopped by user")
                    return
                
                result = agent.answer_question(row, metadata_context)
                
                if result is None:
                    continue
                
                response_entry = {
                    "section": row.get('section', ''),
                    "question": row.get('title', ''),
                    "response_choices": row.get('options', ''),
                    "response": result["response"],
                    "evidence": result["evidence"],
                    "notes": result["notes"]
                }
                
                responses.append(response_entry)
                processed += 1
                
                # Update progress
                progress = 20 + (processed / total_questions) * 70
                self.progress_var.set(progress)
                
                if processed % 5 == 0:
                    self.log_message(f"Processed {processed}/{total_questions} questions...")
            
            self.log_message(f"Completed: {len(responses)} responses generated")
            self.progress_var.set(90)
            
            # Generate summary
            self.log_message("")
            self.log_message("Generating evaluation summary...")
            summary = agent.generate_summary(responses, dataset_name or "Unknown Dataset")
            self.log_message("Summary generated")
            self.progress_var.set(95)
            
            # Save outputs
            self.log_message("")
            self.log_message("Saving outputs...")
            output_prefix = self.output_prefix_var.get()
            
            json_path = agent.save_json_output(responses, output_prefix, dataset_name or "Unknown Dataset", output_dir, summary)
            csv_path = agent.save_csv_output(responses, output_prefix, output_dir)
            
            self.log_message(f"JSON saved to: {json_path}")
            self.log_message(f"CSV saved to: {csv_path}")
            self.progress_var.set(100)
            
            self.log_message("")
            self.log_message("=" * 70)
            self.log_message("Evaluation Complete!")
            self.log_message("=" * 70)
            
            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Evaluation complete!\n\nResults saved to:\n{json_path}\n{csv_path}"
            ))
            
        except Exception as e:
            self.log_message("")
            self.log_message(f"ERROR: {str(e)}")
            self.log_message("")
            import traceback
            self.log_message(traceback.format_exc())
            
            self.root.after(0, lambda: messagebox.showerror(
                "Error",
                f"Evaluation failed:\n{str(e)}"
            ))
        
        finally:
            # Re-enable run button
            self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
            self.running = False
    
    def stop_evaluation(self):
        """Stop the running evaluation."""
        self.running = False
        self.log_message("")
        self.log_message("Stopping evaluation...")


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = FAIR4AIAgentUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
