wavecalcs is a collection of Python scripts designed for power quality analysis, specifically focused on Fast Fourier Transform (FFT) calculations for harmonics and unbalance calculations in three-phase power systems.

📋 Description
This project provides lightweight and straightforward tools to process power waveform data (voltage and current) and obtain key metrics for electrical system diagnosis:
Harmonics Analysis (fft.py): Performs spectral decomposition of signals to identify harmonic content and distortion.
Unbalance Calculation (unb.py): Determines system unbalance, using vector methods or symmetrical components to evaluate asymmetry between phases.

📂 Project Structure
fft.py: Main script for FFT calculation.
unb.py: Script for phase unbalance calculation.
waves.csv: Sample file with waveform data (time domain) for testing.
waves_unbV.csv / unb.csv: Sample files with specific data for unbalance calculation validation.

🚀 Requirements
To run these scripts, you will need Python 3.x and the following standard scientific libraries:
```
pip install numpy pandas matplotlib scipy
```

⚙️ Usage
1. Harmonics Analysis (FFT)
Run the fft.py script to process the waveform data. The script reads the input data and generates the frequency spectrum.
```
python fft.py
```

3. Unbalance Calculation
Use unb.py to calculate the percentage of voltage or current unbalance from vector or waveform data.
```
python unb.py
```

📄 Input Data Format
Input CSV files are expected to follow a standard time-series structure.
Example structure (waves.csv):
| Time | PhaseA | PhaseB | PhaseC |
|------|--------|--------|--------|
| 0.00 | 220.1 | 219.5 | 220.3 |
| 0.01 | 225.2 | 215.1 | 224.8 |
| ... | ... | ... | ... |


Time: Timestamp or sample index.
PhaseA/B/C: Instantaneous voltage or current values.

🤝 Contributions
Contributions are welcome. If you wish to improve the efficiency of the FFT algorithm, add visualizations with Matplotlib, or implement new unbalance standards (IEEE/IEC), please feel free to open a Pull Request.

📝 License
This project is available under the MIT license. See the LICENSE file for more details.
