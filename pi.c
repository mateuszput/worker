#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
  MPI_Init(&argc, &argv);
  int world_rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
  int world_size;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);

 
  long long n, i; 
 
  double stime, etime;
  long long sum, in_circle;
  double x, y;

  in_circle = 0;
  srand(time(NULL));

  n = atoll(argv[1]);

  MPI_Barrier(MPI_COMM_WORLD);  
  stime = MPI_Wtime();

  MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

  sum = 0;
  for (i = world_rank; i < n; i += world_size) {
    x = rand() / (double) RAND_MAX;
    y = rand() / (double) RAND_MAX;
    if(x*x + y*y <= 1.0){
      sum++;
    }
  }

  MPI_Reduce(&sum, &in_circle, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

  etime = MPI_Wtime();

  if (world_rank == 0) {
//    printf("pi is approximately %.16f\n", 4*(in_circle / (double) n));
//    printf("%f\n", etime - stime);  //time
      printf("%.16f\n", 4*(in_circle / (double) n));

  }
  
  MPI_Finalize();
}

