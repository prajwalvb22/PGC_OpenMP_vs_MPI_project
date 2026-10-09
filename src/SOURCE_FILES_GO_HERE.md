Put the three C programs and the data-preparation script here:

- seq.c        sequential baseline
- omp.c        OpenMP version
- mpi_stats.c  MPI version
- prepare_data.py  CSV -> binary trip_distance_all.bin

From WSL:   cp ~/pgc_project/src/*.c ~/pgc_project/scripts/prepare_data.py <this folder>/src/
