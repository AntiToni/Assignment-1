# 2D Turing Machine Simulator
## Information
This is a basic 2D turing machine generator/simulator program inspired by Langton's Ant and The Platypus Game. It generates non-halting 2 dimensional turing machines, and supports multiple heads.

## Instructions
1. Ensure python is downloaded and run ```pip install pygame``` and ```pip install numpy```.
2. Set desired parameters in simulator.py.
3. If loading from a save, set LOAD_FILE and LOAD_FROM_FILE values.
4. Run simulator.py in python.

## CONTROLS
- H - Hide turing machine heads.
- ESC - End simulation.
- -/= - Decrease/increase simulation speed.
- S - Save currently running turing machines to file (auto-generated).

## Turmite Converter Instructions
1. Enter turmite table in nested list form in turmite.py.
2. Set name of file to save to.
3. Run turmite.py in python.