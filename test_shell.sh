#!/bin/bash

# 定義資料夾路徑陣列
dirs=(
  "./datasets/FJSP/Brandimarte_Data"
  "./datasets/FJSP/data_dev/1005"
  "./datasets/FJSP/data_dev/1510"
  "./datasets/FJSP/data_dev/2005"
  "./datasets/FJSP/data_dev/2010"
  "./datasets/FJSP/Hurink_Data/Text/edata"
  "./datasets/FJSP/Hurink_Data/Text/rdata"
  "./datasets/FJSP/Hurink_Data/Text/vdata"
)

# 迴圈遍歷每個目錄並運行 test.py
for dir in "${dirs[@]}"; do
  echo "Running test.py on $dir"
  # python3 test.py --date=best --instance_type=FJSP --delete_node=true --test_dir="$dir" --load_weight='./weight/RS_FJSP/best' --q_time_limit_ratio=2
  # python3 test.py --date=0217 --instance_type=FJSP --delete_node=true --test_dir="$dir" --load_weight='./weight/0217/300000' --q_time_limit_ratio=2
  # python3 test.py --date=0319 --instance_type=FJSP --delete_node=true --test_dir="$dir" --load_weight='./weight/0319/300000' --q_time_limit_ratio=2
  python3 test.py --date=0326 --instance_type=FJSP --delete_node=true --test_dir="$dir" --load_weight='./weight/0326/300000' --q_time_limit_ratio=2
done

echo "All tests completed!"
