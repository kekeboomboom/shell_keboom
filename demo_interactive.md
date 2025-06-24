# 🎯 Interactive Statistics Calculator Demo

## How to Use the Interactive Mode

### Step 1: Start the Interactive Script

```bash
python3 interactive_statistics.py
```

### Step 2: Follow the Guided Process

The script will guide you through these steps:

#### 📁 **STEP 1: Base Data File**
```
📁 STEP 1: Base Data File
   This file contains MD5 hash to model mappings (TSV format)
   💡 Tip: You can drag and drop the file into the terminal, or type the full path

➤ Enter base data file path: /path/to/yilian_output.txt
   ✅ File is valid
   📋 File info: yilian_output.txt
   📏 Size: 1,234,567 bytes (1.18 MB)
```

#### 📊 **STEP 2: Excel Data File**
```
📁 STEP 2: Excel Data File
   This file should contain sheets '接通' and 'A' with phone number data
   💡 Tip: You can drag and drop the file into the terminal, or type the full path

➤ Enter Excel file path: /path/to/phone_data.xlsx
   ✅ File is valid
   📋 File info: phone_data.xlsx
   📏 Size: 2,345,678 bytes (2.24 MB)
   📊 Excel sheets found: 接通, A, Sheet1
   ✅ All required sheets found: 接通, A
```

#### 📂 **STEP 3: Output Directory**
```
📂 OUTPUT DIRECTORY
   Choose a prefix for your output directory (optional)
   💡 Default: 'results' → creates 'results_YYYYMMDD_HHMMSS_hash'

➤ Enter output prefix (or press Enter for default 'results'): my_analysis
```

#### 📋 **STEP 4: Confirmation**
```
============================================================
📋 SUMMARY - Please confirm your settings:
============================================================
📄 Base data file:    /path/to/yilian_output.txt
📊 Excel file:        /path/to/phone_data.xlsx
📂 Output prefix:     my_analysis
============================================================

➤ Proceed with these settings? (y/n): y
```

#### 🚀 **STEP 5: Processing**
```
🚀 STARTING PROCESSING...
============================================================
Running command: python3 statistic_model_success_order_rate.py --base_data /path/to/yilian_output.txt --need_statistic /path/to/phone_data.xlsx --output_prefix my_analysis

⏳ Processing... Please wait...

✅ PROCESSING COMPLETED SUCCESSFULLY!
============================================================
📄 Processing Output:
[Processing details and statistics will be shown here]
```

#### 🎉 **STEP 6: Results**
```
🎉 RESULTS READY!
============================================================
📂 Output directory: my_analysis_20241201_143022_abc123

📁 Generated files:
   📊 Main results: my_analysis_20241201_143022_abc123/order_success_rate_results.csv
      Size: 15,432 bytes
   📋 Processing info: my_analysis_20241201_143022_abc123/processing_info.txt
   📁 Intermediate files: 6 CSV files in my_analysis_20241201_143022_abc123/intermediate

💡 To view results:
   📊 Main results: open my_analysis_20241201_143022_abc123/order_success_rate_results.csv
   📁 All files: open my_analysis_20241201_143022_abc123

🎯 SUCCESS! Your analysis is complete.
   Check the output directory for detailed results.
```

## 🔧 Interactive Features

### ✅ **File Validation**
- Automatically checks if files exist
- Validates file permissions
- Shows file size and basic information
- For Excel files: lists all sheets and checks for required ones

### 🛡️ **Error Handling**
- Clear error messages for missing files
- Validation of output directory names
- Graceful handling of processing errors

### 🎮 **User-Friendly Controls**
- Type `quit`, `exit`, or `q` to exit at any time
- Drag and drop files directly into terminal
- Press Enter for default values
- Clear confirmation before processing

### 📊 **Excel Sheet Validation**
The script automatically checks for required Excel sheets:
- ✅ Sheet '接通' (call_connected)
- ✅ Sheet 'A' (A_intention)
- ⚠️ Warns if sheets are missing

### 📁 **Smart Output Management**
- Creates unique timestamped directories
- Shows all generated files with sizes
- Provides direct paths for easy access
- Organizes intermediate files separately

## 💡 Tips for Best Experience

1. **Prepare your files first** - Have both input files ready before starting
2. **Use full paths** - Absolute paths work best for file inputs
3. **Check Excel sheets** - Ensure your Excel file has the required sheets
4. **Choose meaningful prefixes** - Use descriptive output directory names
5. **Keep terminal open** - Don't close the terminal until processing completes

## 🆚 Interactive vs Command Line

| Feature | Interactive Mode | Command Line Mode |
|---------|------------------|-------------------|
| **Ease of use** | ⭐⭐⭐⭐⭐ Beginner-friendly | ⭐⭐⭐ Advanced users |
| **File validation** | ✅ Automatic | ❌ Manual |
| **Error guidance** | ✅ Step-by-step help | ❌ Technical errors |
| **Automation** | ❌ Manual input required | ✅ Scriptable |
| **Batch processing** | ❌ One pair at a time | ✅ Multiple file pairs |

Choose **Interactive Mode** if you're new to the tool or prefer guided assistance.
Choose **Command Line Mode** for automation or processing multiple file pairs. 
