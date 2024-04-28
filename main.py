import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import numpy as np
from multiprocessing import cpu_count
# path donde esta la data
INPUT_DIR = '../ProyectoHiloss/so_data'



def list_files(directory):
    files = os.listdir(directory)
    print("Files in directory:")
    for file in files:
        print(file)

# ver que si estenleyendose los files
list_files(INPUT_DIR)


def calculate_stats(data):
    # datos estadisticos
    numeric_data = data.select_dtypes(include=[np.number])
    return {
        'count': numeric_data.count(),
        'mean': numeric_data.mean(),
        'std': numeric_data.std(),
        'min': numeric_data.min(),
        'max': numeric_data.max()
    }

def process_file(file_path):
    # Process a single file and save stats
    data = pd.read_csv(file_path)
    stats = calculate_stats(data)
    output_filename = f"{os.path.splitext(file_path)[0]}_out.csv"
    pd.DataFrame(stats).to_csv(output_filename, index=False)
    return output_filename

def run_sequential(input_dir):
    # Run all files sequentially
    start_time = time.time()
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv') and not filename.endswith('_out.csv'):
            process_file(os.path.join(input_dir, filename))
    return time.time() - start_time

def run_parallel_files(input_dir, max_workers):
    # Run file processing in parallel
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, os.path.join(input_dir, filename))
                   for filename in os.listdir(input_dir)
                   if filename.endswith('.csv') and not filename.endswith('_out.csv')]
        for future in as_completed(futures):
            future.result()  # Wait for each file to be processed
    return time.time() - start_time

def main():
    # Adjust max_workers based on the threading model and CPU core/thread restrictions
    threading_models = {
        '1core-1thread': 1,
        '1core-4threads': 4,
        '2core-2threads': 2,
        '2core-4threads': 4,
        '2core-8threads': 8,
        '4core-8threads': 8  # You need to ensure your system has 4 cores available for this
    }
    
    all_results = {}

    for model_name, max_workers in threading_models.items():
        print(f"Running model: {model_name}")
        time_results = []
        for _ in range(10):  # Perform 10 iterations
            start_time = time.time()
            results = run_parallel_files(INPUT_DIR, max_workers)
            end_time = time.time()
            time_taken = end_time - start_time
            time_results.append(time_taken)
        all_results[model_name] = time_results

    # Save all timing results to a single CSV file
    df = pd.DataFrame.from_dict(all_results)
    df.to_csv('c:/Users/Javier C/OneDrive - Universidad Francisco Marroquin/Clases/Sistemas operativos/ProyectoHiloss/time_results.csv', index=False)

if __name__ == "__main__":
    main()