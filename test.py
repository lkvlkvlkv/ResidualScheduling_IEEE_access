import torch
from params import get_args
from env.env import JSP_Env
from model.REINFORCE import REINFORCE
import time
import os
import pandas as pd

def test():
    data_frame = pd.DataFrame(columns=['instance', 'makespan', 'time', 'terminate', 'exceed_q_time'])
    
    for instance in os.listdir(args.test_dir):
        file = os.path.join(args.test_dir, instance)
        avai_ops = env.load_instance(file)
        st = time.time()
        q_time_limit_exceed = False

        while True:
            data, op_unfinished= env.get_graph_data()
            action_idx, action_prob = policy(avai_ops, data, op_unfinished, env.jsp_instance.graph.max_process_time, greedy=True)
            avai_ops, _, done, terminate, exceed_q_time = env.step(avai_ops[action_idx])

            if terminate:
                q_time_limit_exceed = True
            
            if done:
                ed = time.time()
                policy.clear_memory()

                new_row = pd.DataFrame([{'instance': file, 'makespan': env.get_makespan(), 'time': ed - st, 'terminate': 0 if q_time_limit_exceed else 1, 'exceed_q_time': exceed_q_time}])
                data_frame = pd.concat([data_frame, new_row], ignore_index=True)
                print("instance : {}, ms : {}, time : {}, q_time_limit_exceed : {}, exceed_q_time : {}".format(file, env.get_makespan(), ed - st, q_time_limit_exceed, exceed_q_time))

                with open("./result/{}/test_result.txt".format(args.date),"a") as outfile:
                    outfile.write(f'instance : {file:60}, policy : {env.get_makespan():10}\t')
                    outfile.write(f'time : {ed - st:10}\t terminate : {terminate}\n')
                break
    print(f'{args.date}, avg_ms : {data_frame["makespan"].mean()}, avg_time : {data_frame["time"].mean()}, terminate : {data_frame["terminate"].sum()}, terminate_ratio : {data_frame["terminate"].sum() / len(data_frame)}')
    file_name = args.test_dir.replace('./datasets/FJSP/', '').replace('/Text', '')
    os.makedirs(f"./result/{args.date}/{file_name}/", exist_ok=True)
    data_frame.to_csv(f"./result/{args.date}/{file_name}/test_result.csv", index=False)

if __name__ == '__main__':
    args = get_args()
    print(args)
    env = JSP_Env(args)
    policy = REINFORCE(args).to(args.device)
    os.makedirs('./result/{}/'.format(args.date), exist_ok=True)
    
    policy.load_state_dict(torch.load(args.load_weight, map_location=args.device), False)
    with torch.no_grad():
        test()
                    