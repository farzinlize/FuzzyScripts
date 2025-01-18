#include <stdatomic.h>
#include <stdio.h>
#include <pthread.h>
#include <time.h>
#include <stdbool.h>

/*
   comparing atomic operation and lock mechanism for counter
   overhead is measured as speed-down from not-safe operation
   (not-safe operation always returns wrong answer)
*/

#define REACH 100000
#define NUM_THREAD 100
bool starting_line = false;
atomic_uint atom   = 0;
unsigned int not   = 0;
unsigned int locky = 0;
pthread_mutex_t lock;

void* safe_function(void* arg){
    while(!starting_line);
    for(int i=0;i<REACH;i++){
        atomic_fetch_add(&atom, 1);
    }
}

void* lock_function(void *arg){
    while(!starting_line);
    for(int i=0;i<REACH;i++){
        pthread_mutex_lock(&lock);
        locky++;
        pthread_mutex_unlock(&lock);
    }
}

void* notsafe_function(void *arg){
    while(!starting_line);
    for(int i=0;i<REACH;i++){
        not++;
    }
}

int main(){    
    pthread_t threads[NUM_THREAD];
    clock_t now;
    double atomic_time, lock_time, not_time;
    pthread_mutex_init(&lock, NULL);

    starting_line = false;
    for(int i=0;i<10;i++) pthread_create(&threads[i], NULL, lock_function, NULL);
    now = clock();starting_line=true;
    for(int i=0;i<10;i++) pthread_join(threads[i], NULL);
    lock_time = (double) (clock() - now);
    
    starting_line = false;
    for(int i=0;i<10;i++) pthread_create(&threads[i], NULL, safe_function, NULL);
    now = clock();starting_line=true;
    for(int i=0;i<10;i++) pthread_join(threads[i], NULL);
    atomic_time = (double) (clock() - now);

    starting_line = false;
    for(int i=0;i<10;i++) pthread_create(&threads[i], NULL, notsafe_function, NULL);
    now = clock();starting_line=true;
    for(int i=0;i<10;i++) pthread_join(threads[i], NULL);
    not_time = (double) (clock() - now);

    printf("REACH->%d, safe:%u | lock:%u | not:%u\n", REACH*NUM_THREAD, atomic_load(&atom), locky, not);
    printf("atomic-time:%f, lock-time:%f, not-time:%f\n", atomic_time, lock_time, not_time);
    printf("atomic-speed-down:%f, lock-speed-down:%f\n", not_time/atomic_time, not_time/lock_time);
    printf("atomic-speedup (compare to lock): %f\n", lock_time/atomic_time);
    return 0;
}
