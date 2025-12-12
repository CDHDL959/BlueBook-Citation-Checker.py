# run the application with < python BluebookChecker_GUI.py >
# errors = red, warnings = orange, info = blue, components = cyan. 
# scorabble area given for input and results, accomodates long text

# should work on Windows, MAC, and Linux...
# Set of code that will use Python's tkinter to provide a GUI, rather than a script that runs in a terminal.
# Could use refinement, especially in regards to citation input. 
# I think I would rather have it parse through a .docx or .pdf and make those corrections, but this is a good place to start. 

import re
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
from typing import Dict, Optional

class BluebookChecker:
    """
    This class will validate Bluebook-style case citations
    Will define common reporter abbreviations and courts in a dictionary and list respectively
    """

    REPORTERS = {
        'U.S.': 'Supreme Court',
        'S. Ct.': 'Supreme Court Reporter',
        'L. Ed.': 'Lawyers\' Edition',
        'F.': 'Federal Reporter (1st)',
        'F.2d': 'Federal Reporter (2nd)',
        'F.3d': 'Federal Reporter (3rd)',
        'F.4th': 'Federal Reporter (4th)',
        'F. Supp.': 'Federal Supplement (1st)',
        'F. Supp. 2d': 'Federal Supplement (2nd)',
        'F. Supp. 3d': 'Federal Supplement (3rd)',
        'A.': 'Atlantic Reporter (1st)',
        'A.2d': 'Atlantic Reporter (2nd)',
        'A.3d': 'Atlantic Reporter (3rd)',
        'P.': 'Pacific Reporter (1st)',
        'P.2d': 'Pacific Reporter (2nd)',
        'P.3d': 'Pacific Reporter (3rd)',
        'N.E.': 'Northeastern Reporter (1st)',
        'N.E.2d': 'Northeastern Reporter (2nd)',
        'N.E.3d': 'Northeastern Reporter (3rd)',
        'N.W.': 'Northwestern Reporter (1st)',
        'N.W.2d': 'Northwestern Reporter (2nd)',
        'S.E.': 'Southeastern Reporter (1st)',
        'S.E.2d': 'Southeastern Reporter (2nd)',
        'S.W.': 'Southwestern Reporter (1st)',
        'S.W.2d': 'Southwestern Reporter (2nd)',
        'S.W.3d': 'Southwestern Reporter (3rd)',
        'So.': 'Southern Reporter (1st)',
        'So. 2d': 'Southern Reporter (2nd)',
        'So. 3d': 'Southern Reporter (3rd)',
    }

    COURTS = [
        'U.S.', 'D.C. Cir.', '1st Cir.', '2nd Cir.', '3rd Cir.', '4th Cir.',
        '5th Cir.', '6th Cir.', '7th Cir.', '8th Cir.', '9th Cir.', '10th Cir.',
        '11th Cir.', 'Fed. Cir.', 'D. Del.', 'S.D.N.Y.', 'N.D. Cal.', 'E.D. Va.',
        'W.D. Tex.', 'C.D. Cal.', 'D.D.C.'
    ]

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.components = []

    def check_citation(self, citation: str) -> Dict:
        """Check a citation against Bluebook format rules."""
        self.errors = []
        self.warnings = []
        self.info = []
        self.components = {}
    
        # Two patterns: one with court, one without
        pattern_with_court = r'^(.+?),\s*(\d+)\s+([A-Z][A-Za-z0-9.\s]+?)\s+(\d+)(?:,\s*(\d+))?\s*\(([^)]+)\s+(\d{4})\)\.?$'
        pattern_no_court = r'^(.+?),\s*(\d+)\s+([A-Z][A-Za-z0-9.\s]+?)\s+(\d+)(?:,\s*(\d+))?\s*\((\d{4})\)\.?$'
    
        match = re.match(pattern_with_court, citation)
        court = None
    
        if match:
            case_name, volume, reporter, start_page, pin_cite, court, year = match.groups()
        else:
            match = re.match(pattern_no_court, citation)
            if match:
                case_name, volume, reporter, start_page, pin_cite, year = match.groups()
                court = None
            else:
                self.errors.append(
                    'Citation does not match basic Bluebook format: '
                    'Case Name, Volume Reporter Page (Court Year)'
                )
                return self._build_result()

        # store the components here
        self.components = {
            'case_name': case_name,
            'volume': volume, 
            'reporter': reporter.strip(),
            'start_page': start_page,
            'pin_cite': pin_cite,
            'court': court.strip() if court else 'Not specified',
            'year': year
        }

        #validate each component
        self._check_case_name(case_name)
        self._check_volume(volume)
        self._check_reporter(reporter.strip())
        self._check_page(start_page)
        self._check_pin_cite(pin_cite)
        if court:
            self._check_court(court.strip(), reporter.strip())
        else:
            # no court means it is TYPICALLY a Supreme Court case
            if reporter.strip() == 'U.S.':
                self.info.append('Supreme Court case - court designation not required')
        self._check_year(year)
        self._check_period(citation)
        
        return self._build_result()
    
    def _check_case_name(self, case_name: str):
        """Validate case name formating"""
        if not re.match(r'^[A-Z]', case_name):
            self.warnings.append('Case name should start with a capital letter')

        if ' v. ' not in case_name:
            self.errors.append(
                'Case name must include " v. " (with periods and spaces) between parties'
            )

        else:
            parts = case_name.split(' v. ')
            if len(parts) != 2:
                self.errors.append(
                    'Case name should have exactly two parties separated by " v. "'
                )

            elif not parts[0].strip() or not parts[1].strip():
                self.errors.append('Both party names must be present')

        # check for common words that should be abbreviated. Such as State or People
        common_words = ['United States', 'State', 'People', 'Commonwealth']
        for word in common_words:
            if f'{word} of ' in case_name and f'{word} v.' not in case_name:
                self.info.append(
                    f'Consider abbreviating "{word} of" in party names per Bluebook Rule 10.2.1'
                )

    def _check_volume(self, volume: str):
        """Validate volume number."""
        if not volume.isdigit():
            self.errors.append('Volume number must be numeric')

    def _check_reporter(self, reporter: str):
        """Validates reporter abbreviation"""
        if reporter not in self.REPORTERS:
            self.warnings.append(
                f'Reporter "{reporter}" not recognized. '
                f'Common reporters include: U.S., F.3d, F.4th, S. Ct., etc'
            )
        else:
            self.info.append(f'Reporter: {self.REPORTERS[reporter]}')

    def _check_page(self, page: str):
        """Validates page number"""
        if not page.isdigit():
            self.errors.append('Page number mustbe numeric')

    def _check_pin_cite(self, pin_cite: Optional[str]):
        """Validate pin cite if present."""
        if pin_cite and not pin_cite.isdigit():
            self.errors.append('Pin cite (if present) must be numeric')

    def _check_court(self, court: str, reporter: str):
        """Validates coirt designation"""
        if reporter == 'U.S.' and court != 'U.S.':
            self.warnings.append(
                'U.S. Supreme Court cases in U.S. Reports need only year in parenthetical'
            )
        if court not in self.COURTS and court != 'U.S.':
            self.warnings.append(
                f'Court "{court}" may need verification. Use standard abbreviations.'
            )

    def _check_year(self, year: str):
        """Validate year format"""
        if not re.match(r'^\d{4}$', year):
            self.errors.append('Year must be in YYYY format')
        else:
            year_num = int(year)
            current_year = datetime.now().year
            if year_num < 1700 or year_num > current_year + 1:
                self.warnings.append('Year appears unusual. Please verify')

    def _check_period(self, citation: str):
        """Check for a period at the end"""
        if not citation.strip().endswith('.'):
            self.warnings.append('Citation should end with a period.')

    def _build_result(self) -> Dict:
        """Build the results dictionary"""
        return {
            'is_valid': len(self.errors) == 0, 
            'errors': self.errors,
            'warnings': self.warnings, 
            'info': self.info,
            'components': self.components
        }

class BluebookCheckerGUI:
    """The GUI application for Bluebook citation checking. Should be easier to use than a command line for most people"""
    def __init__(self, root):
        self.root = root
        self.root.title("Bluebook Citation Checker")
        self.root.geometry("1000x850")
        self.root.resizable(True, True)

        self.checker = BluebookChecker()

        # configuring styles
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
        # the main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title Framing
        title_label = ttk.Label(
            main_frame,
            text="Bluebook Citation Checker",
            font=('Helvetica', 30, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)
        subtitle_label = ttk.Label(
            main_frame,
            text="Validate your case citations against Bluebook format rules",
            font=('Helvetica', 20)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 15), sticky=tk.W)

        # Input selection screen of GUI
        input_frame = ttk.LabelFrame(main_frame, text="Enter Citation", padding="10")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)

        self.citation_text = scrolledtext.ScrolledText(
            input_frame,
            height=4,
            wrap=tk.WORD,
            font=('Courier', 17)
        )
        self.citation_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.citation_text.insert('1.0', 'Brown v. Board of Education, 347 U.S. 483 (1954).')

        # our check button
        check_button = ttk.Button(
            main_frame,
            text="Check Citation",
            command=self.check_citation
        )
        check_button.grid(row=3, column=0, pady=(0, 10), sticky=tk.E)

        # results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=2)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            wrap=tk.WORD,
            font=('Courier', 18),
            state='disabled'
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # configuring text tags for colored output
        self.results_text.tag_config('valid', foreground='#2d5016', font=('Courier', 10, 'bold'))
        self.results_text.tag_config('invalid', foreground='#b91c1c', font=('Courier', 10, 'bold'))
        self.results_text.tag_config('error', foreground='#b91c1c')
        self.results_text.tag_config('warning', foreground='#b45309')
        self.results_text.tag_config('info', foreground='#1e40af')
        self.results_text.tag_config('component', foreground='#0e7490')
        self.results_text.tag_config('header', font=('Courier', 10, 'bold'))

        # example citations to be displayed
        examples_frame = ttk.LabelFrame(main_frame, text="Example Citations", padding="10")
        examples_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        examples_frame.columnconfigure(0, weight=1)
        
        self.example_citations = [
            "Brown v. Board of Education, 347 U.S. 483 (1954).",
            "Roe v. Wade, 410 U.S. 113, 153 (1973).",
            "Chevron U.S.A. Inc. v. Natural Resources Defense Council, Inc., 467 U.S. 837 (1984).",
            "United States v. Microsoft Corp., 253 F.3d 34 (D.C. Cir. 2001).",
        ]

        for i, citation in enumerate(self.example_citations):
            btn = ttk.Button(
                examples_frame,
                text=citation,
                command=lambda c=citation: self.load_example(c)
            )
            btn.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=2)

        # formatting guide
        guide_frame = ttk.LabelFrame(main_frame, text="Bluebook Format (Rule 10)", padding="10")
        guide_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        guide_frame.columnconfigure(0, weight=1)
        
        guide_text = tk.Text(guide_frame, height=3, wrap=tk.WORD, font=('Courier', 9))
        guide_text.insert('1.0', 
            "Format: Case Name, Volume Reporter Page, Pinpoint (Court Year).\n"
            "Example: Brown v. Board of Education, 347 U.S. 483, 495 (1954)."
        )
        guide_text.config(state='disabled')
        guide_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

    def load_example(self, citation):
        """Load an example citation into the input field"""
        self.citation_text.delete('1.0', tk.END)
        self.citation_text.insert('1.0', citation)
        self.check_citation()

    def check_citation(self):
        """Check the citation and display the results"""
        citation = self.citation_text.get('1.0', tk.END).strip()

        if not citation:
            return
        results = self.checker.check_citation(citation)
        self.display_results(results)

    def display_results(self, results):
        """Displays validation results in the results text area"""
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        
        # Status
        separator = "=" * 70 + "\n"
        self.results_text.insert(tk.END, separator)
        
        if results['is_valid']:
            self.results_text.insert(tk.END, "✓ VALID FORMAT\n", 'valid')
        else:
            self.results_text.insert(tk.END, "✗ FORMAT ISSUES FOUND\n", 'invalid')
        
        self.results_text.insert(tk.END, separator + "\n")
        
        # Errors
        if results['errors']:
            self.results_text.insert(tk.END, "ERRORS:\n", ('header', 'error'))
            for error in results['errors']:
                self.results_text.insert(tk.END, f"  * {error}\n", 'error')
            self.results_text.insert(tk.END, "\n")

        # Warnings
        if results['warnings']:
            self.results_text.insert(tk.END, "⚠ WARNINGS:\n", ('header', 'warning'))
            for warning in results['warnings']:
                self.results_text.insert(tk.END, f"  • {warning}\n", 'warning')
            self.results_text.insert(tk.END, "\n")

        # Info
        if results['info']:
            self.results_text.insert(tk.END, "ℹ INFORMATION:\n", ('header', 'info'))
            for info in results['info']:
                self.results_text.insert(tk.END, f"  • {info}\n", 'info')
            self.results_text.insert(tk.END, "\n")
        
        # Components
        if results['components']:
            self.results_text.insert(tk.END, "CITATION COMPONENTS:\n", ('header', 'component'))
            for key, value in results['components'].items():
                if value:
                    label = key.replace('_', ' ').title()
                    self.results_text.insert(tk.END, f"  {label}: {value}\n", 'component')
            self.results_text.insert(tk.END, "\n")
        
        self.results_text.insert(tk.END, separator)
        self.results_text.config(state='disabled')
        self.results_text.see('1.0')

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = BluebookCheckerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
