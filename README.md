# MRI Sequence Visualization

This Python script generates visualizations of MRI sequences using Matplotlib and the MRSd library. It reads parameters from a JSON file and creates diagrams for different MRI pulse sequences such as Gradient Echo (GRE), Spin Echo (SE), and Balanced Steady-State Free Precession (BSSFP).

## Usage

To use this script, follow these steps:

1. Make sure you have Python installed on your system.
2. Install the required libraries: `matplotlib` and `mrsd`.
3. Prepare a JSON file (`parameters.json`) containing the parameters for the MRI sequences.
4. Run the Python script.

## MRI Sequence Profiles

The script supports the following MRI sequence profiles:

- Gradient Echo (GRE)
- Spin Echo (SE)
- Balanced Steady-State Free Precession (BSSFP)

You can specify the desired profile in the `parameters.json` file.

## Output

The script generates visualizations of the MRI sequences based on the parameters provided in the JSON file. It creates diagrams showing RF pulses, gradients, and readout signals.

## File Structure

- `MRI_Sequence_Visualization.py`: The Python script for generating MRI sequence visualizations.
- `parameters.json`: JSON file containing the parameters for the MRI sequences.
- `Time_file.txt`: Output file containing the sorted time points for the sequence steps.

## Example

Here's an example of how to run the script:

```bash
python MRI_Sequence_Visualization.py
