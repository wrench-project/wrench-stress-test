/**
 * Copyright (c) 2017. The WRENCH Team.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */

#include "StressTestWMS.h"

XBT_LOG_NEW_DEFAULT_CATEGORY(stress_test_wms, "Log category for Stress Test WMS");

namespace wrench {

  int StressTestWMS::main() {
     WRENCH_INFO("New WMS starting");

    std::shared_ptr<JobManager> job_manager = this->createJobManager();


    std::set<WorkflowTask *> tasks_to_do;
    for (auto t : this->getWorkflow()->getTasks()) {
      tasks_to_do.insert(t);
    }
    std::set<WorkflowTask *> pending_tasks;

    while (tasks_to_do.empty()) {

    }




    return 0;
  }

};