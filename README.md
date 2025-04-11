# Container Scheduler

This project implements a single-node container scheduling system designed to execute user-submitted jobs across a pool of Docker containers. The system uses a command-line interface (CLI) to receive and process job requests, schedule them onto available containers, and manage input/output operations.

## System Overview

- The scheduler runs on an Ubuntu 20.04 virtual machine with Docker installed.
- Three Docker containers are launched from a custom-built image containing predefined programs.
- Each job request is formatted as a command specifying:
  - An operation (e.g., `min`, `max`, `average`, `sort`, `wordcount`, or a custom executable)
  - An input file path
  - An output directory

## Behavior and Features

- The system maintains a pool of exactly three containers.
- Job requests are processed through a CLI thread which queues them for execution.
- An execution thread assigns jobs to available containers as they become free.
- Jobs are run in isolation, and their outputs are written to the specified output directory.
- Operations include statistical processing (min, max, average), text sorting, word counts, and support for running compiled C++ or Python programs within the container.
- Each container executes in single-threaded mode and handles one job at a time.
- The CLI supports batch submission of multiple job requests at once, using the format:
  
  ```
  {<operation, input_file_path>, <operation, input_file_path>, ..., <output_directory>}
  ```

- Example input:
  ```
  {<min, /tmp/grades.txt>, <max, /tmp/grades.txt>, </tmp/gradeStat>}
  ```

- Example output (in `/tmp/gradeStat/`):
  ```
  min.txt
  max.txt
  ```

- Jobs remain in a pending queue if all containers are busy. Once a container becomes available, it picks the next job in the queue automatically.

## Notes

- The system supports execution of external programs stored inside the container image. Outputs are written to files named as `program-name.out`.
