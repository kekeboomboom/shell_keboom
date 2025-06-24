# Model Success Order Rate Statistics Calculator - Installation Guide

## Prerequisites

- macOS with Python 3.6 or higher
- Terminal access

## Installation Steps

### Quick Setup (Recommended)

Run the automated setup script:

```bash
./setup.sh
```

This will automatically:
- Check Python installation
- Install required dependencies (pandas, openpyxl) using Tsinghua mirror for faster downloads
- Make the script executable
- Test the installation

### Manual Setup (Alternative)

If you prefer manual installation:

1. **Verify Python Installation**
   ```bash
   python3 --version
   ```

2. **Install Dependencies**
   ```bash
   pip3 install pandas openpyxl
   ```

3. **Make Script Executable**
   ```bash
   chmod +x statistic_model_success_order_rate.py
   ```

## Usage

### 🖱️ Interactive Mode (Recommended)

For a user-friendly experience with step-by-step guidance:

```bash
python3 interactive_statistics.py
```

This interactive mode will:
- Guide you through each step with clear prompts
- Validate your input files automatically
- Show file information and Excel sheet details
- Confirm settings before processing
- Display results with clear file paths

### 💻 Command Line Mode

For advanced users or automation:

```bash
python3 statistic_model_success_order_rate.py --base_data yilian_output.txt --need_statistic data.xlsx
```

### Multiple File Pairs

```bash
python3 statistic_model_success_order_rate.py \
  --base_data file1.txt file2.txt \
  --need_statistic data1.xlsx data2.xlsx
```

### Custom Output Directory Prefix

```bash
python3 statistic_model_success_order_rate.py \
  --base_data yilian_output.txt \
  --need_statistic data.xlsx \
  --output_prefix my_analysis
```

## Input File Requirements

### Base Data File (yilian_output)
- Format: TSV (Tab-separated values)
- Columns: [mobile_id_md5, model_name, ...]
- First line is header (will be skipped)

Example:
```
mobile_id_md5	model_name	other_columns
abc123def456	iPhone 14	...
def789ghi012	Samsung S23	...
```

### Excel File (need_statistic)
- Must contain two sheets:
  - Sheet '接通' (call_connected): Phone numbers that connected
  - Sheet 'A' (A_intention): Phone numbers with purchase intention
- Phone numbers should be in the first column of each sheet

## Output Structure

The script creates a unique directory for each run:

```
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
```

## Troubleshooting

### Common Issues

1. **"No module named 'pandas'"**
   ```bash
   pip3 install pandas openpyxl
   ```

2. **"Permission denied"**
   ```bash
   chmod +x statistic_model_success_order_rate.py
   ```

3. **"File not found"**
   - Ensure input files exist in the current directory
   - Use absolute paths if files are in different directories

4. **Excel sheet names not found**
   - Verify Excel file contains sheets named '接通' and 'A'
   - Check sheet names are exactly as expected (case-sensitive)

### Getting Help

Run the script with `--help` to see all available options:

```bash
python3 statistic_model_success_order_rate.py --help
```

## Example Workflow

1. Prepare your input files:
   - `yilian_output.txt` (base data with MD5 to model mappings)
   - `phone_data.xlsx` (Excel file with call data)

2. Run the script:
   ```bash
   python3 statistic_model_success_order_rate.py \
     --base_data yilian_output.txt \
     --need_statistic phone_data.xlsx
   ```

3. Check the results:
   ```bash
   ls -la results_*/
   cat results_*/order_success_rate_results.csv
   ```

## Performance Notes

- Processing time depends on file sizes
- Large Excel files may take several minutes to process
- The script creates intermediate files for debugging purposes
- All output is saved with timestamps for tracking multiple runs 
