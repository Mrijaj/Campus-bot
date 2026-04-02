from core.processor import FileProcessor
import os

# Initialize the processor
# Note: You don't need the API key for local PDF/Word/PPT extraction
proc = FileProcessor()

# Test with a file (change 'sample.docx' to your file name)
filename = "sample.docx"
if os.path.exists(filename):
    print(f"--- Extracting {filename} ---")
    content = proc.process(filename)
    print(content[:500]) # Print first 500 characters
else:
    print("Please put a sample.docx or sample.pdf in this folder first!")