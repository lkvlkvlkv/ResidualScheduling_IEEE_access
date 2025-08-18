import pandas as pd

import os

base_dir = './result/'
dates = ['or-tools']
test_dirs = ['Brandimarte_Data', \
             'data_dev/1005', 'data_dev/1510', 'data_dev/2005', 'data_dev/2010', \
             'Hurink_Data/rdata', 'Hurink_Data/edata', 'Hurink_Data/vdata',]


for date in dates:
    # data_frame = pd.DataFrame(columns=['instance', 'avg_makespan', 'avg_time', 'avg_terminate', 'terminate_ratio', 'avg_q_time_penalty'])
    data_frame = pd.DataFrame(columns=['instance', 'avg_makespan', 'avg_time', 'avg_terminate', 'terminate_ratio', 'avg_q_time_penalty'])

    for test_dir in test_dirs:
        file_path = os.path.join(base_dir, date, test_dir)
        
        if os.path.exists(file_path):
            df = pd.read_csv(os.path.join(file_path, 'test_result.csv'))
            avg_makespan = df['makespan'].mean()
            avg_time = df['time'].mean()
            terminate_count = df['exceeded'].sum()
            terminate_ratio = 100 * terminate_count / len(df)
            avg_q_time_penalty = df['exceed_q_time'].mean()

            instance = test_dir.split('/')[-1]
            new_row = pd.DataFrame([{'instance': instance, 'avg_makespan': avg_makespan, 'avg_time': avg_time, 'avg_terminate': terminate_count, 'terminate_ratio': terminate_ratio, 'avg_q_time_penalty': avg_q_time_penalty}])
            data_frame = pd.concat([data_frame, new_row], ignore_index=True)

    data_frame.to_csv(os.path.join(base_dir, date, 'summary.csv'), index=False)
    print(f"Summary for date {date} saved.")
