#!/usr/bin/env python3
"""
Model Success Order Rate Statistics Calculator

This script processes Excel data and calculates order success rates by model.
Supports processing multiple file pairs with unique output directories.

Input Files:
1. Base data file(s) (yilian_output): Contains MD5 hash to model mappings
   Format: TSV with columns [mobile_id_md5, model_name, ...]
2. Excel file(s) (need_statistic): Contains phone number data in two sheets
   - Sheet '接通' (call_connected): Phone numbers that connected
   - Sheet 'A' (A_intention): Phone numbers with purchase intention

Output Structure:
For each processing run, a unique directory is created with timestamp:
results_YYYYMMDD_HHMMSS_<hash>/
├── intermediate/
│   ├── call_connect.csv
│   ├── A_intention.csv
│   ├── call_connect_model.csv
│   ├── call_connect_model_count.csv
│   ├── A_intention_model.csv
│   └── A_intention_model_count.csv
├── order_success_rate_results.csv (final results)
└── processing_info.txt (metadata about the run)

Usage:
    # Single file pair
    python statistic_model_success_order_rate.py --base_data yilian_output.txt --need_statistic data.xlsx
    
    # Multiple file pairs
    python statistic_model_success_order_rate.py --base_data file1.txt file2.txt --need_statistic data1.xlsx data2.xlsx
    
    # Custom output directory prefix
    python statistic_model_success_order_rate.py --base_data file1.txt --need_statistic data1.xlsx --output_prefix my_analysis
"""

import pandas as pd
import os
import hashlib
import csv
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import shutil

class FileManager:
    """Manages input and output file paths with unique directory creation"""
    
    def __init__(self, base_data_file: str, excel_file: str, output_prefix: str = "results"):
        # Input files
        self.base_data_file = base_data_file
        self.excel_file = excel_file
        
        # Create unique output directory
        self.output_dir = self._create_unique_output_dir(output_prefix)
        self.intermediate_dir = os.path.join(self.output_dir, "intermediate")
        
        # Create directories
        os.makedirs(self.intermediate_dir, exist_ok=True)
        
        # Output files (all in the unique directory)
        self.final_output_file = os.path.join(self.output_dir, "order_success_rate_results.csv")
        self.processing_info_file = os.path.join(self.output_dir, "processing_info.txt")
        
        # Intermediate files (in intermediate subdirectory)
        self.call_connect_csv = os.path.join(self.intermediate_dir, "call_connect.csv")
        self.a_intention_csv = os.path.join(self.intermediate_dir, "A_intention.csv")
        self.call_connect_model_csv = os.path.join(self.intermediate_dir, "call_connect_model.csv")
        self.call_connect_count_csv = os.path.join(self.intermediate_dir, "call_connect_model_count.csv")
        self.a_intention_model_csv = os.path.join(self.intermediate_dir, "A_intention_model.csv")
        self.a_intention_count_csv = os.path.join(self.intermediate_dir, "A_intention_model_count.csv")
    
    def _create_unique_output_dir(self, prefix: str) -> str:
        """Create a unique output directory with timestamp and hash"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create a short hash from input file names for uniqueness
        file_info = f"{self.base_data_file}_{self.excel_file}"
        file_hash = hashlib.md5(file_info.encode()).hexdigest()[:8]
        
        dir_name = f"{prefix}_{timestamp}_{file_hash}"
        # Ensure the directory is created relative to current working directory
        return os.path.join(".", dir_name)
    
    def get_input_files(self) -> Dict[str, str]:
        """Get all input file paths"""
        return {
            'base_data': self.base_data_file,
            'excel_data': self.excel_file
        }
    
    def get_output_files(self) -> Dict[str, str]:
        """Get all output file paths"""
        return {
            'output_directory': self.output_dir,
            'intermediate_directory': self.intermediate_dir,
            'call_connect_csv': self.call_connect_csv,
            'a_intention_csv': self.a_intention_csv,
            'call_connect_model_csv': self.call_connect_model_csv,
            'call_connect_count_csv': self.call_connect_count_csv,
            'a_intention_model_csv': self.a_intention_model_csv,
            'a_intention_count_csv': self.a_intention_count_csv,
            'final_results': self.final_output_file,
            'processing_info': self.processing_info_file
        }
    
    def write_processing_info(self, start_time: datetime, end_time: datetime, success: bool):
        """Write processing metadata to info file"""
        duration = end_time - start_time
        
        info_content = f"""Processing Information
=====================
Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Duration: {duration.total_seconds():.2f} seconds
Status: {'SUCCESS' if success else 'FAILED'}

Input Files:
- Base Data: {self.base_data_file}
- Excel Data: {self.excel_file}

Output Directory: {self.output_dir}

Generated Files:
- Final Results: {os.path.basename(self.final_output_file)}
- Intermediate Files: {len([f for f in os.listdir(self.intermediate_dir) if f.endswith('.csv')])} CSV files

File Sizes:
"""
        
        # Add file size information
        for desc, path in self.get_output_files().items():
            if os.path.exists(path) and os.path.isfile(path):
                size = os.path.getsize(path)
                info_content += f"- {os.path.basename(path)}: {size:,} bytes\n"
        
        with open(self.processing_info_file, 'w', encoding='utf-8') as f:
            f.write(info_content)
    
    def print_file_summary(self):
        """Print summary of all input and output files"""
        print("=" * 80)
        print("FILE SUMMARY")
        print("=" * 80)
        
        print(f"\nOUTPUT DIRECTORY: {self.output_dir}")
        print(f"INTERMEDIATE DIRECTORY: {self.intermediate_dir}")
        
        print("\nINPUT FILES:")
        print("-" * 40)
        input_files = self.get_input_files()
        for desc, path in input_files.items():
            status = "✓ EXISTS" if os.path.exists(path) else "✗ NOT FOUND"
            size = f"({os.path.getsize(path):,} bytes)" if os.path.exists(path) else ""
            print(f"  {desc:15}: {path} [{status}] {size}")
        
        print("\nOUTPUT FILES (will be generated):")
        print("-" * 40)
        output_files = self.get_output_files()
        for desc, path in output_files.items():
            if desc.endswith('_directory'):
                print(f"  {desc:20}: {path} [DIRECTORY]")
            else:
                print(f"  {desc:20}: {os.path.basename(path)}")
        print("=" * 80)

class ModelStatisticsProcessor:
    """Main processor for model statistics calculations"""
    
    def __init__(self, file_manager: FileManager):
        self.fm = file_manager
    
    def generate_md5(self, phone_number: str) -> str:
        """Generate MD5 hash for a phone number"""
        return hashlib.md5(str(phone_number).encode('utf-8')).hexdigest()
    
    def check_excel_sheets(self) -> bool:
        """Check and display information about Excel sheets"""
        print(f"\n=== STEP 1: Checking Excel file structure ===")
        
        if not os.path.exists(self.fm.excel_file):
            print(f"Error: File {self.fm.excel_file} not found!")
            return False
        
        try:
            print(f"Checking Excel file: {self.fm.excel_file}")
            
            excel_file_obj = pd.ExcelFile(self.fm.excel_file)
            sheet_names = excel_file_obj.sheet_names
            
            print(f"\nFound {len(sheet_names)} sheets:")
            for i, sheet_name in enumerate(sheet_names, 1):
                print(f"{i}. '{sheet_name}'")
            
            # Show preview of each sheet
            for sheet_name in sheet_names:
                print(f"\n--- Preview of sheet '{sheet_name}' ---")
                df = pd.read_excel(self.fm.excel_file, sheet_name=sheet_name, nrows=3)
                print(f"Shape: {df.shape}")
                print("Columns:", list(df.columns))
                print("First 3 rows:")
                print(df)
                print("-" * 50)
            
            return True
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return False
    
    def convert_excel_to_csv(self) -> bool:
        """Convert Excel sheets to CSV files"""
        print(f"\n=== STEP 2: Converting Excel to CSV ===")
        
        if not os.path.exists(self.fm.excel_file):
            print(f"Error: File {self.fm.excel_file} not found!")
            return False
        
        try:
            print(f"Reading Excel file: {self.fm.excel_file}")
            
            # Read the first sheet: 接通 (call_connected) - skip first line
            print("Reading sheet: 接通")
            call_connected_df = pd.read_excel(self.fm.excel_file, sheet_name='接通', header=None, skiprows=1)
            
            # Read the second sheet: A (A_intention) - keep first line
            print("Reading sheet: A")
            a_intention_df = pd.read_excel(self.fm.excel_file, sheet_name='A', header=None)
            
            # Save to CSV files
            print(f"Saving {self.fm.call_connect_csv}...")
            call_connected_df.to_csv(self.fm.call_connect_csv, index=False, header=False, encoding='utf-8')
            
            print(f"Saving {self.fm.a_intention_csv}...")
            a_intention_df.to_csv(self.fm.a_intention_csv, index=False, header=False, encoding='utf-8')
            
            # Print summary information
            print("\nConversion completed successfully!")
            print(f"Sheet '接通' (call_connected): {len(call_connected_df)} rows, {len(call_connected_df.columns)} columns")
            print(f"Sheet 'A' (A_intention): {len(a_intention_df)} rows, {len(a_intention_df.columns)} columns")
            
            # Show first few rows of each sheet
            print(f"\nFirst 5 rows of call_connected (接通):")
            print(call_connected_df.head())
            
            print(f"\nFirst 5 rows of A_intention (A):")
            print(a_intention_df.head())
            
            return True
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print("Please check if the sheet names are correct and the file is accessible.")
            return False
    
    def load_model_mappings(self) -> Dict[str, str]:
        """Load MD5 to model mappings from base data file"""
        print(f"Reading model data from {self.fm.base_data_file}...")
        md5_model_map = {}
        
        try:
            with open(self.fm.base_data_file, 'r') as f:
                # Skip header line
                next(f)
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        mobile_id = parts[0]
                        model_name = parts[1]
                        md5_model_map[mobile_id] = model_name
        except FileNotFoundError:
            print(f"Error: Could not find file {self.fm.base_data_file}")
            return {}
        
        print(f"Found {len(md5_model_map)} model mappings")
        return md5_model_map
    
    def process_phone_data(self, phone_csv_file: str, output_csv_file: str, data_type: str) -> bool:
        """Generic function to process phone data and match with models"""
        print(f"\n=== Processing {data_type} data ===")
        
        print(f"Reading phone numbers from {phone_csv_file}...")
        phone_numbers = []
        try:
            with open(phone_csv_file, 'r') as f:
                for line in f:
                    phone_number = line.strip()
                    if phone_number:  # Skip empty lines
                        phone_numbers.append(phone_number)
        except FileNotFoundError:
            print(f"Error: Could not find file {phone_csv_file}")
            return False
        
        print(f"Found {len(phone_numbers)} phone numbers")
        
        # Load model mappings
        md5_model_map = self.load_model_mappings()
        if not md5_model_map:
            return False
        
        print("Matching phone numbers with models...")
        output_data = []
        matched_count = 0
        
        for phone in phone_numbers:
            md5_hash = self.generate_md5(phone)
            model_name = md5_model_map.get(md5_hash, "")  # Empty string if no match
            
            if model_name:
                matched_count += 1
            
            output_data.append([phone, md5_hash, model_name])
        
        print(f"Matched {matched_count} out of {len(phone_numbers)} phone numbers")
        
        print(f"Writing results to {output_csv_file}...")
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['phone_number', 'phone_md5', 'model_name'])
            writer.writerows(output_data)
        
        print(f"Successfully created {output_csv_file}")
        print(f"Total records: {len(output_data)}")
        print(f"Matched records: {matched_count}")
        print(f"Unmatched records: {len(output_data) - matched_count}")
        
        return True
    
    def count_data_by_model(self, input_file: str, output_file: str, data_type: str) -> bool:
        """Count phone numbers for each model"""
        print(f"\n=== Counting {data_type} phones by model ===")
        
        if not os.path.exists(input_file):
            print(f"Error: Input file {input_file} not found!")
            return False
        
        try:
            print(f"Reading data from {input_file}...")
            df = pd.read_csv(input_file)
            
            print(f"Total records: {len(df)}")
            
            # Count phones by model, excluding empty model names
            model_counts = df[df['model_name'] != '']['model_name'].value_counts()
            
            print(f"Found {len(model_counts)} different models")
            print(f"Total phones with models: {model_counts.sum()}")
            
            # Convert to DataFrame for easier handling
            count_df = pd.DataFrame({
                'model_name': model_counts.index,
                'count': model_counts.values
            })
            
            # Sort by model name for consistent output
            count_df = count_df.sort_values('model_name')
            
            print(f"Writing results to {output_file}...")
            count_df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"Successfully created {output_file}")
            print(f"Model count summary:")
            print(f"- Total models: {len(count_df)}")
            print(f"- Total phones counted: {count_df['count'].sum()}")
            
            # Show top 10 models by count
            print(f"\nTop 10 models by phone count:")
            top_models = count_df.nlargest(10, 'count')
            for _, row in top_models.iterrows():
                print(f"  {row['model_name']}: {row['count']}")
            
            return True
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return False
    
    def calculate_order_success_rate(self) -> bool:
        """Calculate order success rate for each model"""
        print(f"\n=== STEP 7: Calculating order success rate ===")
        
        try:
            # Read the CSV files
            a_intention_df = pd.read_csv(self.fm.a_intention_count_csv)
            call_connect_df = pd.read_csv(self.fm.call_connect_count_csv)
            
            # Create dictionaries for easy lookup
            a_intention_dict = dict(zip(a_intention_df['model_name'], a_intention_df['count']))
            call_connect_dict = dict(zip(call_connect_df['model_name'], call_connect_df['count']))
            
            # Calculate order success rate for each model in call_connect
            results = []
            
            for model_name, call_connect_count in call_connect_dict.items():
                # Get A_intention count (default to 0 if model not found)
                a_intention_count = a_intention_dict.get(model_name, 0)
                
                # Calculate order success rate
                order_success_rate = a_intention_count / call_connect_count if call_connect_count > 0 else 0
                
                results.append({
                    'model_name': model_name,
                    'a_intention_count': a_intention_count,
                    'call_connect_count': call_connect_count,
                    'order_success_rate': f"{order_success_rate * 100:.2f}%"
                })
            
            # Create DataFrame with results
            results_df = pd.DataFrame(results)
            
            # Sort by model name for better readability
            results_df = results_df.sort_values('model_name')
            
            # Display results
            print("Order Success Rate Calculation Results:")
            print("=" * 80)
            print(f"{'Model Name':<20} {'A_Intention':<12} {'Call_Connect':<12} {'Success Rate (%)':<15}")
            print("-" * 80)
            
            for _, row in results_df.iterrows():
                print(f"{row['model_name']:<20} {row['a_intention_count']:<12} {row['call_connect_count']:<12} {row['order_success_rate']:<15}")
            
            # Save results to CSV
            results_df.to_csv(self.fm.final_output_file, index=False)
            print(f"\nResults saved to '{self.fm.final_output_file}'")
            
            # Show summary statistics
            print(f"\nSummary:")
            print(f"Total models analyzed: {len(results_df)}")
            print(f"Total A_intention count: {results_df['a_intention_count'].sum()}")
            print(f"Total call_connect count: {results_df['call_connect_count'].sum()}")
            
            return True
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return False
    
    def run_full_process(self) -> bool:
        """Run the complete processing pipeline"""
        start_time = datetime.now()
        
        print("=== MODEL SUCCESS ORDER RATE STATISTICS ===")
        print("This script processes Excel data and calculates order success rates by model")
        
        # Print file summary
        self.fm.print_file_summary()
        
        success = True
        
        try:
            # Step 1: Check Excel sheets
            if not self.check_excel_sheets():
                print("Failed to check Excel sheets. Exiting.")
                success = False
                return False
            
            # Step 2: Convert Excel to CSV
            if not self.convert_excel_to_csv():
                print("Failed to convert Excel to CSV. Exiting.")
                success = False
                return False
            
            # Step 3: Process call_connect data
            if not self.process_phone_data(self.fm.call_connect_csv, self.fm.call_connect_model_csv, "call_connect"):
                print("Failed to process call_connect data. Exiting.")
                success = False
                return False
            
            # Step 4: Count call_connect phones by model
            if not self.count_data_by_model(self.fm.call_connect_model_csv, self.fm.call_connect_count_csv, "call_connect"):
                print("Failed to count call_connect phones by model. Exiting.")
                success = False
                return False
            
            # Step 5: Process A_intention data
            if not self.process_phone_data(self.fm.a_intention_csv, self.fm.a_intention_model_csv, "A_intention"):
                print("Failed to process A_intention data. Exiting.")
                success = False
                return False
            
            # Step 6: Count A_intention phones by model
            if not self.count_data_by_model(self.fm.a_intention_model_csv, self.fm.a_intention_count_csv, "A_intention"):
                print("Failed to count A_intention phones by model. Exiting.")
                success = False
                return False
            
            # Step 7: Calculate order success rate
            if not self.calculate_order_success_rate():
                print("Failed to calculate order success rate. Exiting.")
                success = False
                return False

            print("\n=== ALL PROCESSING COMPLETED SUCCESSFULLY ===")
            print(f"Output directory: {self.fm.output_dir}")
            print("Generated files:")
            output_files = self.fm.get_output_files()
            for desc, path in output_files.items():
                if not desc.endswith('_directory'):
                    print(f"- {path}")
            
            return True
            
        finally:
            # Always write processing info
            end_time = datetime.now()
            self.fm.write_processing_info(start_time, end_time, success)

def process_multiple_files(base_data_files: List[str], need_statistic_files: List[str], output_prefix: str) -> List[str]:
    """Process multiple file pairs and return list of output directories"""
    
    if len(base_data_files) != len(need_statistic_files):
        print(f"Error: Number of base_data files ({len(base_data_files)}) must match number of need_statistic files ({len(need_statistic_files)})")
        return []
    
    output_directories = []
    total_files = len(base_data_files)
    
    print(f"\n{'='*80}")
    print(f"PROCESSING {total_files} FILE PAIR(S)")
    print(f"{'='*80}")
    
    for i, (base_data_file, excel_file) in enumerate(zip(base_data_files, need_statistic_files), 1):
        print(f"\n{'='*60}")
        print(f"PROCESSING PAIR {i}/{total_files}")
        print(f"Base data: {base_data_file}")
        print(f"Excel file: {excel_file}")
        print(f"{'='*60}")
        
        # Check if input files exist
        if not os.path.exists(base_data_file):
            print(f"Error: Base data file {base_data_file} not found. Skipping this pair.")
            continue
            
        if not os.path.exists(excel_file):
            print(f"Error: Excel file {excel_file} not found. Skipping this pair.")
            continue
        
        # Initialize file manager and processor for this pair
        file_manager = FileManager(base_data_file, excel_file, output_prefix)
        processor = ModelStatisticsProcessor(file_manager)
        
        # Run processing
        success = processor.run_full_process()
        
        if success:
            output_directories.append(file_manager.output_dir)
            print(f"\n✓ Successfully processed pair {i}/{total_files}")
            print(f"  Output directory: {file_manager.output_dir}")
        else:
            print(f"\n✗ Failed to process pair {i}/{total_files}")
    
    return output_directories

def main():
    """Main function to run all processing steps"""
    parser = argparse.ArgumentParser(
        description='Calculate model success order rate statistics for multiple file pairs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--base_data', required=True, nargs='+',
                       help='Base data file(s) (yilian_output files with MD5 to model mappings)')
    parser.add_argument('--need_statistic', required=True, nargs='+',
                       help='Excel file(s) to analyze (contains phone data in sheets)')
    parser.add_argument('--output_prefix', default='results',
                       help='Output directory prefix (default: results)')
    
    args = parser.parse_args()
    
    # Process multiple files
    output_directories = process_multiple_files(args.base_data, args.need_statistic, args.output_prefix)
    
    # Final summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    print(f"Total file pairs processed: {len(args.base_data)}")
    print(f"Successful processing runs: {len(output_directories)}")
    print(f"Failed processing runs: {len(args.base_data) - len(output_directories)}")
    
    if output_directories:
        print(f"\nGenerated output directories:")
        for i, output_dir in enumerate(output_directories, 1):
            print(f"{i:2d}. {output_dir}")
            
        print(f"\nTo view results:")
        for output_dir in output_directories:
            print(f"  ls -la {output_dir}/")
            print(f"  cat {output_dir}/processing_info.txt")
    else:
        print("\nNo files were successfully processed.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
