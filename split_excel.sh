#!/bin/bash

# Print colorful messages
print_info() {
  echo -e "\033[1;34m[信息]\033[0m $1"
}

print_success() {
  echo -e "\033[1;32m[成功]\033[0m $1"
}

print_error() {
  echo -e "\033[1;31m[错误]\033[0m $1"
}

print_progress() {
  echo -e "\033[1;36m[进度]\033[0m $1"
}

clear
echo "================================"
echo " Excel 文件按照地区分割工具 "
echo "================================"
echo ""

# Get input file from user if not provided
if [ -z "$1" ]; then
  read -p "请输入 Excel 文件路径: " INPUT_FILE
else
  INPUT_FILE="$1"
  print_info "使用提供的文件: $INPUT_FILE"
fi

# Remove any surrounding quotes if present
INPUT_FILE=$(printf "%s" "$INPUT_FILE" | sed -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/" | sed 's/[[:space:]]*$//')

print_info "检查文件: $INPUT_FILE"

# Keep asking until a valid file is provided
while [ ! -f "$INPUT_FILE" ] || [[ ! "$INPUT_FILE" =~ \.xlsx$ ]]; do
  if [ ! -f "$INPUT_FILE" ]; then
    print_error "文件未找到: '$INPUT_FILE'"
    print_info "请检查文件是否存在以及路径是否正确"
    print_info "提示: 您可以将文件拖放到此终端窗口中"
  elif [[ ! "$INPUT_FILE" =~ \.xlsx$ ]]; then
    print_error "文件必须是 .xlsx 文件: '$INPUT_FILE'"
  fi
  read -p "请输入有效的 Excel 文件路径: " INPUT_FILE
  # Remove any surrounding quotes if present
  INPUT_FILE=$(printf "%s" "$INPUT_FILE" | sed -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/" | sed 's/[[:space:]]*$//')
done

# Get input file details for output naming
INPUT_DIR=$(dirname "$INPUT_FILE")
FILENAME=$(basename "$INPUT_FILE")
FILENAME_NO_EXT="${FILENAME%.*}"

# Set output files with new naming convention
USABLE_OUTPUT="${INPUT_DIR}/${FILENAME_NO_EXT}_usable.xlsx"
BLOCKED_OUTPUT="${INPUT_DIR}/${FILENAME_NO_EXT}_blocked.xlsx"

# Default blocked areas
DEFAULT_AREAS="宣城,南宁,宜春,阿坝藏族羌族自治州,海南藏族自治州,漳州,神农架林区,厦门,海东,抚州,宁波,东莞,濮阳,黔南布依族苗族自治州,济源,景德镇,安庆,珠海,海北藏族自治州,商洛,福州,龙岩,上饶,果洛藏族自治州,乐山,吉安,常州,广州,银川,连云港,南京,安康,甘孜藏族自治州,金昌,玉树藏族自治州,丽江,天门,延安,温州,榆林,成都,淮北,萍乡,江门,遵义,镇江,防城港,固原,深圳,汕头,西宁,池州,西安,资阳,扬州,苏州,佛山"

# Get blocked areas from command line or ask user
if [ -n "$2" ]; then
  BLOCKED_AREAS="$2"
  print_info "使用提供的屏蔽区域: $BLOCKED_AREAS"
else
  print_info "默认屏蔽区域: $DEFAULT_AREAS"
  read -p "是否使用这些默认区域? (y/n) [y]: " USE_DEFAULT
  if [[ "$USE_DEFAULT" == "n" || "$USE_DEFAULT" == "N" ]]; then
    read -p "请输入需要屏蔽的地区列表（中文逗号分割）: " BLOCKED_AREAS
    if [ -z "$BLOCKED_AREAS" ]; then
      print_error "未指定任何区域。正在退出。"
      exit 1
    fi
  else
    BLOCKED_AREAS="$DEFAULT_AREAS"
  fi
fi

echo ""
print_info "=== 处理概要 ==="
print_info "输入文件: $INPUT_FILE"
print_info "屏蔽区域: $BLOCKED_AREAS"
print_info "输出文件将是:"
print_info "  - 可用数据: $USABLE_OUTPUT"
print_info "  - 屏蔽数据: $BLOCKED_OUTPUT"
echo ""

# Confirm with user
read -p "是否继续处理? (y/n) [y]: " CONFIRM
if [[ "$CONFIRM" == "n" || "$CONFIRM" == "N" ]]; then
  print_info "用户取消了操作。"
  exit 0
fi

# Test file readability one last time
if [ ! -r "$INPUT_FILE" ]; then
  print_error "无法读取文件: '$INPUT_FILE'"
  print_error "请检查文件权限"
  exit 1
fi

# Convert comma-separated string to Python set format
PYTHON_AREAS=$(echo "$BLOCKED_AREAS" | sed "s/,/', '/g")
PYTHON_AREAS="{'$PYTHON_AREAS'}"

echo ""
print_progress "开始 Excel 处理..."

# Run Python script for Excel processing with progress indicators
python3 -c "
import pandas as pd
import sys
import time
import os

# Define blocked areas from shell argument
blocked_areas_str = sys.argv[1]
# print(f'DEBUG: Received blocked_areas_str: {blocked_areas_str}')
try:
    blocked_areas = eval(blocked_areas_str) # Evaluate the blocked areas string
    if not isinstance(blocked_areas, set):
        # print(f'DEBUG: Warning - eval did not result in a set. Type is {type(blocked_areas)}. Value: {blocked_areas}')
        # Fallback if eval doesn't produce a set, e.g. if input was just "area1,area2"
        blocked_areas = set(a.strip() for a in blocked_areas_str.replace(\"{\",\"\").replace(\"}\",\"\").replace(\"'\",\"\").split(\",\"))

except Exception as e:
    # print(f'DEBUG: Error evaluating blocked_areas_str: {e}. Attempting fallback parsing.')
    # Fallback parsing if eval fails
    raw_areas = blocked_areas_str.replace(\"{\", \"\").replace(\"}\", \"\")
    blocked_areas = set(a.strip().replace(\"'\", \"\") for a in raw_areas.split(',') if a.strip())


# print(f'DEBUG: Parsed blocked_areas set: {blocked_areas}')


try:
    # Show progress indicator
    print('正在读取 Excel 文件...')
    
    # Check file exists in Python as well
    file_path = sys.argv[2]
    if not os.path.exists(file_path):
        print(f'错误：Python 未找到文件：\"{file_path}\"')
        print(f'当前工作目录：{os.getcwd()}')
        sys.exit(1)
        
    # Read the Excel file
    df = pd.read_excel(file_path, header=None)
    
    # Log the total number of rows
    total_rows = len(df)
    print(f'总行数：{total_rows}')
    
    # Ensure we have at least 3 columns
    if df.shape[1] < 3:
        print('错误：Excel 文件必须至少有3列')
        sys.exit(1)

    # Clean the target column: strip whitespace from strings if the column is of object type
    if df[2].dtype == 'object':
        df[2] = df[2].astype(str).str.strip() # Convert to string first, then strip
    
    # DEBUG: Print unique values from the relevant column (e.g., first 20 unique values)
    unique_values_in_column = df[2].unique()
    # print(f'DEBUG: Unique values in column 2 (sample of first 20): {list(unique_values_in_column[:20])}')
    # if len(unique_values_in_column) > 20:
    #     print(f'DEBUG: (Total {len(unique_values_in_column)} unique values in column 2)')

    # Print some sample data for verification
    print('示例数据 (前3行):')
    for i in range(min(3, len(df))):
        print(f'  行 {i+1}: {df.iloc[i, 0]}, {df.iloc[i, 1]}, {df.iloc[i, 2]}')
    
    # Filter rows based on the area column (third column, index 2)
    print('正在筛选数据... 0%')
    time.sleep(0.5)
    print('正在筛选数据... 25%')
    # Ensure blocked_areas contains strings for comparison, especially after potential eval issues
    str_blocked_areas = {str(area) for area in blocked_areas}
    # print(f'DEBUG: Using stringified blocked_areas for filtering: {str_blocked_areas}')

    usable_rows = df[~df[2].isin(str_blocked_areas)]
    time.sleep(0.5)
    print('正在筛选数据... 50%')
    blocked_rows = df[df[2].isin(str_blocked_areas)]
    time.sleep(0.5)
    print('正在筛选数据... 75%')
    time.sleep(0.5)
    print('正在筛选数据... 100%')
    
    # Write to output files
    print(f'正在将可用数据写入输出文件... 0%')
    time.sleep(0.5)
    print(f'正在将可用数据写入输出文件... 50%')
    usable_rows.to_excel(sys.argv[3], index=False, header=False)
    print(f'正在将可用数据写入输出文件... 100%')
    
    print(f'正在将屏蔽数据写入输出文件... 0%')
    time.sleep(0.5)
    print(f'正在将屏蔽数据写入输出文件... 50%')
    blocked_rows.to_excel(sys.argv[4], index=False, header=False)
    print(f'正在将屏蔽数据写入输出文件... 100%')
    
    print(f'\\n结果:')
    print(f'- 总行数: {total_rows}')
    print(f'- 可用行数: {len(usable_rows)}')
    print(f'- 屏蔽行数: {len(blocked_rows)}')
    
    # Check if any area had no matches
    found_areas = set(df[2].unique())
    matched_areas = blocked_areas.intersection(found_areas)
    if len(matched_areas) < len(blocked_areas):
        missing = blocked_areas - matched_areas
        print(f'\\n注意：数据中未找到某些屏蔽区域：{missing}')
    
    print('\\n处理完成！')
    
except Exception as e:
    print(f'处理 Excel 文件时出错：{e}')
    sys.exit(1)
" "$PYTHON_AREAS" "$INPUT_FILE" "$USABLE_OUTPUT" "$BLOCKED_OUTPUT"

# Check if processing was successful
if [ $? -eq 0 ]; then
  echo ""
  print_success "Excel 文件已成功分割。"
  print_success "可用数据: $USABLE_OUTPUT"
  print_success "屏蔽数据: $BLOCKED_OUTPUT"
else
  echo ""
  print_error "处理 Excel 文件失败。"
  exit 1
fi

echo ""
print_info "感谢使用 Excel 文件分割工具！" 
