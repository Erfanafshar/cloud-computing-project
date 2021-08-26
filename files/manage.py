import threading
from queue import Queue
import time
import docker
import re

def cli_in_from_user(cli_q=None):
    while(True):
        inp = input()
        if inp == "status":
            cli_q.put(inp)
            continue
        if re.search("{(<.*>)+}", inp) == None:
            print("bad input")
        else:
            cli_q.put(inp)



def manage_containers(containers_q=[], cli_q=None):
    contaners_status = {0:0 , 1:0, 2:0}
    tasks = []
    task_counter = 0
    while(True):
        print_status = False
        for i, (q_to_c, q_from_c) in enumerate(containers_q):
            if q_from_c.empty():
                status = 1
            else:
                status = q_from_c.get()
                # print("from ", i,"got this: " , status)
            contaners_status[i] = int(status)

        
        if not cli_q.empty():
            cli_inp = cli_q.get()
            if cli_inp == "status":
                print_status = True
            else:
                task_counter += 1
                tasks.append((task_counter, cli_inp))

        if len(tasks) > 0:
            for c_num, status in contaners_status.items():
                if status != 1:
                    task = tasks.pop(0)
                    containers_q[c_num][0].put(task[1])
                    contaners_status[0] = 1 
                    print(f"Task {str(task[0])} assigned to container {c_num}")
                    break
            
            

            # print("job for:" , container_num)
            # if container_num == 0 and contaners_status[0] != 1:
            #     containers_q[0][0].put(1)
            #     contaners_status[0] = 1 
            # if container_num == 1 and contaners_status[1] != 1:
            #     containers_q[1][0].put(1)
            #     contaners_status[1] = 1
            # if container_num == 2 and contaners_status[2] != 1:
            #     containers_q[2][0].put(1)
            #     contaners_status[2] = 1
        if print_status:
            print("tasks:", [x[0] for x in tasks])
            print(contaners_status)


        
        time.sleep(0.1)   



def container(q_in, q_out, container_num=-1, container_obj=None, job=""):
    while(True):
        if q_out.empty():
            q_out.put(0)
        if not q_in.empty():
            while not q_out.empty():
                q_out.get()
            job = q_in.get()
            time.sleep(10)
            job = '\"' + job +'\"'
            exec_num, output = container_obj.exec_run("python3 worker.py "+job)
            output = output.decode("utf-8").strip('\n')
            print(f"container {container_num} job done: code:{exec_num}, {output}")










if __name__ == "__main__":


    client = docker.from_env()
    container0 = None
    container1 = None
    container2 = None
    for c in client.containers.list():
        if c.name == "c1":
            container0 = c
        if c.name == "c2":
            container1 = c
        if c.name == "c3":
            container2 = c



    c0_q_in = Queue()
    c0_q_out = Queue()
    c1_q_in = Queue()
    c1_q_out = Queue()
    c2_q_in = Queue()
    c2_q_out = Queue()
    cli_manager_q = Queue()
    container0_thread = threading.Thread(target=container, args=(c0_q_in, c0_q_out, 0, container0 ))
    container1_thread = threading.Thread(target=container, args=(c1_q_in, c1_q_out, 1, container1 ))
    container2_thread = threading.Thread(target=container, args=(c2_q_in, c2_q_out, 2, container2 ))
    cli_thread = threading.Thread(target=cli_in_from_user, args=(cli_manager_q, ))
    manager_thread = threading.Thread(target=manage_containers,\
        args=([(c0_q_in, c0_q_out), (c1_q_in, c1_q_out), (c2_q_in, c2_q_out)], cli_manager_q))

    cli_thread.start()
    manager_thread.start()
    container0_thread.start()
    container1_thread.start()
    container2_thread.start()

