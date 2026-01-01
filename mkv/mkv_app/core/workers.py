import os
import shutil
import subprocess
import re
import threading
import psutil
from PyQt6.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    progress = pyqtSignal(int, int, str)  # overall %, file_index, status_text
    finished = pyqtSignal()
    result_ready = pyqtSignal(int, int, list) # success_count, fail_count, failed_files

    def __init__(self, jobs):
        super().__init__()
        self.jobs = jobs
        self.is_aborted = False
        self.current_process = None

    def abort(self):
        self.is_aborted = True
        print(f"DEBUG: WorkerThread.abort() called. PID: {self.current_process.pid if self.current_process else 'None'}")
        if self.current_process:
            try:
                self.kill_process_tree(self.current_process.pid)
            except Exception as e:
                print(f"DEBUG: Error aborting process: {e}")

    def kill_process_tree(self, pid):
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.terminate()
                except psutil.NoSuchProcess:
                    pass
            gone, still_alive = psutil.wait_procs(children, timeout=3)
            for p in still_alive:
                try:
                    p.kill()
                except psutil.NoSuchProcess:
                    pass
            parent.terminate()
            parent.wait(3)
        except psutil.NoSuchProcess:
            pass
        except Exception as e:
            print(f"Error killing process tree: {e}")

    def run(self):
        total_jobs = len(self.jobs)
        success_count = 0
        fail_count = 0
        failed_files = []

        print(f"DEBUG: WorkerThread started with {total_jobs} jobs")

        for index, job in enumerate(self.jobs):
            if self.is_aborted:
                print("DEBUG: Worker aborted inside run loop")
                break
            
            job_type = job.get('type', 'command')
            try:
                # Calculate base progress
                base_progress = int((index / total_jobs) * 100)
                
                # Execute Job based on type
                if job_type == 'to_mkv' or job_type == 'move_and_convert' or job_type == 'to_options':
                    success = self.execute_conversion_job(job, index, total_jobs, base_progress)
                elif job_type == 'command':
                    success = self.execute_command_job(job, index, total_jobs, base_progress)
                else:
                    success = False
                
                if success:
                    success_count += 1
                else:
                    failed_files.append(job.get('source_file', 'unknown'))

            except Exception as e:
                print(f"Job failed: {e}")
                failed_files.append(job.get('source_file', 'unknown'))
        
        self.result_ready.emit(success_count, len(failed_files), failed_files)
        self.finished.emit()

    def execute_conversion_job(self, job, index, total_jobs, base_progress):
        source_file = job['source_file']
        moved_file = job['moved_file_path']
        output_file = job['output_file']
        
        # Ensure directory for moved file exists
        os.makedirs(os.path.dirname(moved_file), exist_ok=True)
        
        try:
            # Move file
            shutil.move(source_file, moved_file)
            
            # Construct command
            if job['type'] == 'to_options':
                cmd = job['command_template'].format(
                    json_file=job['json_file'],
                    output_file=output_file,
                    input_file=moved_file
                )
            else:
                 cmd = f'"{job["mkvmerge_path"]}" --output "{output_file}" "{moved_file}"'

            # Run command
            success = self.run_process(cmd, index, total_jobs, base_progress, os.path.basename(source_file))
            
            if not success:
                # Restore file on failure
                if os.path.exists(moved_file):
                    shutil.move(moved_file, source_file)
                return False
                
            return True

        except Exception as e:
            print(f"Error in conversion job: {e}")
            if os.path.exists(moved_file):
                try:
                    shutil.move(moved_file, source_file)
                except:
                    pass
            return False

    def execute_command_job(self, job, index, total_jobs, base_progress):
        if 'ensure_dir' in job:
            os.makedirs(job['ensure_dir'], exist_ok=True)
            
        cmd = job['command']
        desc = job.get('description', '')
        return self.run_process(cmd, index, total_jobs, base_progress, desc)

    def run_process(self, cmd, index, total_jobs, base_progress, description):
        try:
            self.progress.emit(base_progress, index, f"Processing: {description}")
            
            print(f"DEBUG: Running command: {cmd}")
            
            self.current_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            progress_regex = re.compile(r"Progress: (\d+)%")
            
            all_output = []
            while True:
                if self.is_aborted:
                    self.current_process.terminate()
                    return False
                
                line = self.current_process.stdout.readline()
                if line == '' and self.current_process.poll() is not None:
                    break
                    
                if line:
                    all_output.append(line.strip())
                    print(f"DEBUG OUTPUT: {line.strip()}")
                    match = progress_regex.search(line.strip())
                    if match:
                        file_progress = int(match.group(1))
                        # contribution of this file to total progress
                        overall_progress = base_progress + int((file_progress / 100.0) * (100.0 / total_jobs))
                        self.progress.emit(overall_progress, index, f"{description} ({file_progress}%)")
            
            returncode = self.current_process.poll()
            print(f"DEBUG: Command finished with return code: {returncode}")
            if returncode != 0:
                print(f"DEBUG: Full output was: {''.join(all_output)}")
            return returncode == 0
            
        except Exception as e:
            print(f"Process error: {e}")
            return False
