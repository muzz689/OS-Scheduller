import sys
import json
import queue 
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Define the process data clas
class Process:
    def __init__(self, name, duration, arrival_time, io_frequency,process_time,io_flag):
        self.name = name
        self.duration = duration
        self.arrival_time = arrival_time
        self.io_frequency = io_frequency
        self.time = process_time
        self.waiting_time = duration
        self.io_flag =io_flag
        self.scheduled = False




def stcf3(sorted_data):

    #Variable to keep track of stuff 
    output = ""
    current_time = 0 #To keep track of the time
    current_process = None #To keep track of the current running Process 
    counter_index =0 
    UnProcess_queue = []#Queue for ready but unscheduled processes

    while sorted_data or current_process:
        # Filter out all the processes that have arrived till current time
        ready_processes = [proc for proc in sorted_data if proc.arrival_time <= current_time]

        # Add all the  unscheduled processes which are  ready  to queue
        for proc in ready_processes:
            if not proc.scheduled:
                UnProcess_queue.append(proc)

        # If we have ready processes which are unprocessed do them first this helps to reduce response time
        if UnProcess_queue:
            current_process = UnProcess_queue.pop(0)     
            current_process.scheduled = True  

        #  Else do stcf 
        else:
            # Choose the shortest Process 
            current_process = min(ready_processes, key=lambda x: x.duration)
            min_duration = current_process.duration

            #If we have many shortest Processes  , processes them in a broken round robin fashion
            tied_processes = [proc for proc in ready_processes if proc.duration == min_duration]
            if len(tied_processes) > 1:
                    current_process = tied_processes[current_time % len(tied_processes)]

        # PROCESSING PART   
        # If the current process is finished remove it and continue
        if current_process.duration == 0:
            sorted_data.remove(current_process)
            current_process = None
            continue

        # If we our current Process has io frequency 
        if(current_process !=None and current_process.io_frequency !=0  ):
            #Basically checks if io shud happen and does relevent outputing and continue
            if( current_process.time % current_process.io_frequency  == 0 and current_process.time >0 and not current_process.io_flag):
                output  += "!" +current_process.name + " "
                current_process.io_flag = True
                current_time += 1 
                counter_index +=1
                continue
        
        #Basically does the normal outputing
        output += current_process.name + " "
        current_process.duration -= 1
        current_process.time +=1
        current_time += 1
        counter_index +=1
        current_process.io_flag = False

    return output

def main():
    # Check if the correct number of arguments is provided
    import sys
    if len(sys.argv) != 2:
        return 1

    # Extract the input file name from the command line arguments
    input_file_name = f"Process_List/{config['dataset']}/{sys.argv[1]}"

    # Define the number of processes
    num_processes = 0

    # Initialize an empty list for process data
    data_set = []

    # Open the file for reading
    try:
        with open(input_file_name, "r") as file:
            # Read the number of processes from the file
            num_processes = int(file.readline().strip())

            # Read process data from the file and populate the data_set list
            for _ in range(num_processes):
                line = file.readline().strip()
                name, duration, arrival_time, io_frequency = line.split(',')
                process = Process(name, int(duration), int(arrival_time), int(io_frequency),int(0),False)
                data_set.append(process)

    except FileNotFoundError:
        print("Error opening the file.")
        return 1


    """
    TODO Your Algorithm - assign your output to the output variable
    """

    output = stcf3(data_set)
    
    """
    End of your algorithm
    """

    

    # Open a file for writing
    try:
        output_path = f"Schedulers/template/{config['dataset']}/template_out_{sys.argv[1].split('_')[1]}"
        with open(output_path, "w") as output_file:
            # Write the final result to the output file
            output_file.write(output)

    except IOError:
        print("Error opening the output file.")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
