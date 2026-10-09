#!/bin/bash
# Local benchmark: sequential, OpenMP and MPI on WSL.
# Run from anywhere; expects the project in ~/pgc_project with compiled binaries in src/.
cd ~/pgc_project
BIN=data/trip_distance_all.bin
OUT=results/local_results.csv
REPS=${REPS:-5}
SIZES="1000000 5000000 10000000 25000000 47248723"

echo "model,mode,N,p,run,io_s,compute_s,comm_s,mean,std,count,logmean,logstd" > $OUT
cat $BIN > /dev/null    # load the file into the OS cache first

run() {
    for r in $(seq 1 $REPS); do
        line=$("$@" | grep '^CSV,')
        echo "${line#CSV,}" | awk -F, -v r=$r 'BEGIN{OFS=","}{print $1,$2,$3,$4,r,$5,$6,$7,$8,$9,$10,$11,$12}' >> $OUT
    done
}

for N in $SIZES; do
  for M in 0 1; do
    echo "=== N=$N mode=$M ==="
    run ./src/seq $BIN $N $M
    for T in 1 2 4 8 12; do
        run ./src/omp $BIN $N $M $T
    done
    for P in 1 2 4 8 12; do
        run mpirun --use-hwthread-cpus -np $P ./src/mpi_stats $BIN $N $M
    done
  done
done
echo "DONE. Results in $OUT"
