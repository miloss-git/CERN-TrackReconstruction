# Track Reconstruction using GraphBLAS
This repository contains code, analysis scripts, and visualizations developed during my **CERN Summer Student Project (2025)**.  
The project explores **graph-theoretic methods for track reconstruction** in the ATLAS detector using **GraphBLAS primitives**.

---

## Project Overview
- **Goal**: Investigate how adjacency-matrix–based algorithms can be applied to charged particle track reconstruction.  
- **Core Idea**: Represent detector hits and their connections as sparse matrices, and apply semiring-based operations to extract track candidates.
- **Highlights**:
  - Construction of adjacency matrices from simulated detector hit data
  - Derivation of line graphs (`dub` → `tri` datasets)
  - Exploration of $k$-paths, matrix powers, connected components, and semiring formulations
  - Visualization utilities for paths, curvature, and reconstructed tracks

---

## Repository Structure
  - **data** > Includes csv files that correspond to the dataset of muons collision.
  - **initial_analysis** > The initial approach that was refined later, but still provided useful insight about the problem. In this approach, the weakly connected component was extracted for each root in the graph.
  - **main_algorithm** > Provides files where the final-result algorithm is implemented. The algorithm principles are explored and explained in the report (link beneath).
  - **make_plots** > Functions for plots and graphs drawing.
  - **semi_rings** > Custom classes of numbers corresponding to different semi-ring. Each class is implemented in the main_algorithm-appropriate manner.
  - **sparse_matrix** > Implementation of some operations for sparse matrices in CSR fromat.

---

## Installation
Clone the repository and install dependencies:
git clone https://github.com/username/cern-track-reconstruction.git
cd cern-track-reconstruction
pip install -r requirements.txt

## Report is available at the link:
...(to be included)
