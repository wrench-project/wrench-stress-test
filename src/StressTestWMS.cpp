/**
 * Copyright (c) 2017. The WRENCH Team.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */

#include <set>
#include "StressTestWMS.h"

XBT_LOG_NEW_DEFAULT_CATEGORY(stress_test_wms, "Log category for Stress Test WMS");

namespace wrench {

    int StressTestWMS::main() {
        WRENCH_INFO("New WMS starting");

        std::shared_ptr<JobManager> job_manager = this->createJobManager();


        std::set<shared_ptr<WorkflowTask> > tasks_to_do;
        for (auto t : this->workflow->getTasks()) {
            tasks_to_do.insert(t);
        }
        std::set<shared_ptr<WorkflowTask> > tasks_pending;

        //REMOVE//std::set<std::shared_ptr<ComputeService>> compute_services = this->getAvailableComputeServices<ComputeService>();
        //REMOVE//std::set<std::shared_ptr<StorageService>> storage_services = this->getAvailableStorageServices();

        unsigned long max_num_pending_tasks = 10;

        WRENCH_INFO("%lu tasks to run", tasks_to_do.size());

        while ((not tasks_to_do.empty()) or (not tasks_pending.empty())) {

            while ((tasks_to_do.size() > 0) and (tasks_pending.size() < max_num_pending_tasks)) {

                WRENCH_INFO("Looking at scheduling another task");
                shared_ptr<WorkflowTask> to_submit = *(tasks_to_do.begin());
                tasks_to_do.erase(to_submit);
                tasks_pending.insert(to_submit);

                auto input_file = *(to_submit->getInputFiles().begin());
                auto output_file = *(to_submit->getOutputFiles().begin());
                // Pick a random compute
                auto cs_it(compute_services.begin());
                advance(cs_it, rand() % compute_services.size());
                auto target_cs = *cs_it;
                // Pick a random storage_service
                auto ss_it(storage_services.begin());
                advance(ss_it, rand() % storage_services.size());
                auto target_ss = *ss_it;

                auto job = job_manager->createStandardJob(to_submit, {{output_file, wrench::FileLocation::LOCATION(target_ss)}, {input_file, wrench::FileLocation::LOCATION(target_ss)}});
                job_manager->submitJob(job, target_cs);

            }

            std::shared_ptr <wrench::ExecutionEvent> event;
            event = this->waitForNextEvent();
            auto real_event = dynamic_cast<wrench::StandardJobCompletedEvent *>(event.get());
            if (real_event) {
                shared_ptr<WorkflowTask> completed_task = *(real_event->standard_job->getTasks().begin());
                WRENCH_INFO("Task %s has completed", completed_task->getID().c_str());
                if (tasks_to_do.size() % 10 == 0) {
                    //std::cerr << ".";
                }
                tasks_pending.erase(completed_task);
                //job_manager->forgetJob(real_event->standard_job);
            } else {
                throw std::runtime_error("Unexpected Event!");
            }
        }

        return 0;
    }

};
