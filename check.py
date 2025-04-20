from itertools import accumulate
from ortools.sat.python import cp_model
from params import get_args
import time
import os
import pandas as pd

def test(test_dir, q_time_limit_ratio=1.5, time_limit=10.0):
    data_frame = pd.DataFrame(columns=['instance', 'makespan', 'time', 'exceeded', 'exceed_q_time'])

    for instance in os.listdir(test_dir):
        file_path = os.path.join(test_dir, instance)
        jobs_data, num_machines = load_fjsp_instance(file_path)
        continue

        model = cp_model.CpModel()
        horizon = sum(max(opt[1] for opt in task) for job in jobs_data for task in job)

        all_tasks = {}
        machine_to_intervals = [[] for _ in range(num_machines)]
        task_ends = []
        exceed_q_time_flag = False

        # 計算每個 job 的 Q-time 限制
        q_time_limits = []
        for job in jobs_data:
            expected_process_times = [sum(opt[1] for opt in task) / len(task) for task in job]
            acc_expected = list(accumulate(expected_process_times[::-1]))[::-1]
            q_time_limit = acc_expected[0] * q_time_limit_ratio
            q_time_limits.append(q_time_limit)

        for job_id, job in enumerate(jobs_data):
            previous_end = None
            for task_id, options in enumerate(job):
                suffix = f'_{job_id}_{task_id}'
                start_var = model.NewIntVar(0, horizon, 'start' + suffix)
                end_var = model.NewIntVar(0, horizon, 'end' + suffix)

                is_selected = []
                for alt_id, (machine, duration) in enumerate(options):
                    selected = model.NewBoolVar(f'selected_{suffix}_{alt_id}')
                    interval = model.NewOptionalIntervalVar(start_var, duration, end_var, selected, f'interval{suffix}_{alt_id}')
                    is_selected.append(selected)
                    machine_to_intervals[machine].append(interval)

                model.Add(sum(is_selected) == 1)

                all_tasks[(job_id, task_id)] = (start_var, end_var)
                task_ends.append(end_var)

                if previous_end:
                    model.Add(start_var >= previous_end)
                previous_end = end_var

        for machine in range(num_machines):
            model.AddNoOverlap(machine_to_intervals[machine])


        for job_id, job in enumerate(jobs_data):
            first_start = all_tasks[(job_id, 0)][0]
            last_end = all_tasks[(job_id, len(job) - 1)][1]
            q_span = model.NewIntVar(0, horizon, f'q_span_{job_id}')
            model.Add(q_span == last_end - first_start)
            model.Add(q_span <= int(q_time_limits[job_id]))

        makespan = model.NewIntVar(0, horizon, 'makespan')
        model.AddMaxEquality(makespan, task_ends)
        model.Minimize(makespan)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit

        st = time.time()
        status = solver.Solve(model)
        ed = time.time()

        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            computed_makespan = solver.Value(makespan)
            for job_id, job in enumerate(jobs_data):
                first_start = solver.Value(all_tasks[(job_id, 0)][0])
                last_end = solver.Value(all_tasks[(job_id, len(job) - 1)][1])
                if last_end - first_start > q_time_limits[job_id]:
                    exceed_q_time_flag = True
        else:
            computed_makespan = -1  # infeasible

        exceeded = 1 if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE] else 0

        new_row = pd.DataFrame([{
            'instance': instance,
            'makespan': computed_makespan,
            'time': ed - st,
            'exceeded': exceeded,
            'exceed_q_time': int(exceed_q_time_flag)
        }])

        data_frame = pd.concat([data_frame, new_row], ignore_index=True)
        print(f"instance: {instance}, makespan: {computed_makespan}, time: {ed - st:.2f}s, exceeded: {exceeded}, exceed_q_time: {exceed_q_time_flag}")

    os.makedirs("./result/or-tools/", exist_ok=True)
    data_frame.to_csv(f"./result/or-tools/test_result.csv", index=False)


def load_fjsp_instance(file_path):
    jobs_data = []
    with open(file_path, 'r') as f:
        print(file_path)
        num_jobs, num_machines = map(int, f.readline().split()[:2])
        for _ in range(num_jobs):
            parts = list(map(int, f.readline().split()))
            task_count = parts[0]
            job = []
            idx = 1
            for _ in range(task_count):
                num_options = parts[idx]
                idx += 1
                options = []
                for _ in range(num_options):
                    machine_id = parts[idx]
                    duration = parts[idx + 1]
                    options.append((machine_id, duration))
                    idx += 2
                job.append(options)
            jobs_data.append(job)
    return jobs_data, num_machines

if __name__ == '__main__':
    test_dirs=['./datasets/FJSP/Brandimarte_Data',
              './datasets/FJSP/data_dev/1005', './datasets/FJSP/data_dev/1510', './datasets/FJSP/data_dev/2005', './datasets/FJSP/data_dev/2010',\
            './datasets/FJSP/Hurink_Data/Text/edata','./datasets/FJSP/Hurink_Data/Text/rdata','./datasets/FJSP/Hurink_Data/Text/vdata']
    q_time_limit_ratio=10000.0
    time_limit = 100.0
    for test_dir in test_dirs:
        print(f"Testing directory: {test_dir}")
        test(test_dir, q_time_limit_ratio=q_time_limit_ratio, time_limit=time_limit)