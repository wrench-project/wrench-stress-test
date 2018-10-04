

#ifndef TASK_CLUSTERING_BATCH_SIMULATOR_SIMULATOR_H
#define TASK_CLUSTERING_BATCH_SIMULATOR_SIMULATOR_H

#include "wrench-dev.h"


#define EXECUTION_TIME_FUDGE_FACTOR 1.1

namespace wrench {

    class Simulator {

    public:
        static unsigned long sequence_number;

        unsigned long num_pilot_job_expirations_with_remaining_tasks_to_do = 0;
        double used_node_seconds = 0;
        double wasted_node_seconds = 0;
        double total_queue_wait_time = 0;


        int main(int argc, char **argv);

        void setupSimulationPlatform(wrench::Simulation *simulation, unsigned long num_cs, unsigned long num_ss);

        wrench::Workflow *createWorkflow(std::string workflow_spec);


    };

}

#endif //TASK_CLUSTERING_BATCH_SIMULATOR_SIMULATOR_H
