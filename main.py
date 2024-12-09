# Main
import os
import pandas as pd  # To handle and save the table
import matplotlib.pyplot as plt
from Remove_soft_tissue_function import remove_soft_tissue

def process_folder(folder_path, cell_size, inclusion_criterion, distance_threshold_ratio):
    # Initialize lists to store results
    execution_times = []
    file_names = []

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".stl"):  # Process only .stl files
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_name}")
            try:
                # Process the file and measure execution time
                elapsed_time = remove_soft_tissue(file_path, cell_size, inclusion_criterion, distance_threshold_ratio)
                execution_times.append(elapsed_time)
                file_names.append(file_name)
                print(f"File {file_name} processed in {elapsed_time:.2f} seconds.")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                # Append "ERROR" in case of failure
                execution_times.append("ERROR")
                file_names.append(file_name)

    return file_names, execution_times

def plot_execution_times(file_names, execution_times, output_path):
    valid_files = [file_names[i] for i, t in enumerate(execution_times) if t != "ERROR"]
    valid_times = [t for t in execution_times if t != "ERROR"]

    # Bar Plot
    plt.figure(figsize=(10, max(6, len(valid_files) * 0.5)))
    plt.barh(valid_files, valid_times, color='skyblue')
    plt.xlabel("Execution Time (seconds)")
    plt.ylabel("Processed Files")
    plt.title("Execution Time per File")
    plt.tight_layout()
    plt.savefig(output_path)  # Saving
    plt.show()

def save_results_to_csv(file_names, execution_times, output_path):
    # Table
    results = pd.DataFrame({
        "File Name": file_names,
        "Execution Time (Seconds)": execution_times
    })


    results.to_csv(output_path, index=False)
    print(f"\nResults table saved as: {output_path}")

if __name__ == "__main__":
    # Define the folder containing .stl files
    folder_path = "C:/Program Files/Dental_data/Data/"

    # User inputs for processing parameters
    cell_size = float(input("Enter desired cell size (in mm): "))
    inclusion_criterion = float(input("Enter the inclusion criterion (I): "))
    distance_threshold_ratio = float(input("Set the input ratio (distance threshold): "))

    # Process the folder and get results
    file_names, execution_times = process_folder(folder_path, cell_size, inclusion_criterion, distance_threshold_ratio)

    # Save the results table to a CSV file
    output_directory = r"C:\Users\annag\Desktop\Results"
    table_path = "processing_results.csv"
    save_results_to_csv(file_names, execution_times, table_path)

    # Save and display the execution times plot
    graph_path = "execution_times.png"
    plot_execution_times(file_names, execution_times, graph_path)

    print(f"Graph saved as: {graph_path}")








