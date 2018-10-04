/**
 * Copyright (c) 2017. The WRENCH Team.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */

#ifndef TASK_CLUSTERING_BATCH_SIMULATOR_STRESSTESTWMS_H
#define TASK_CLUSTERING_BATCH_SIMULATOR_STRESSTESTWMS_H

#include <wrench-dev.h>

namespace wrench {

    class StressTestWMS : public WMS {

    public:

        StressTestWMS(const std::set<ComputeService *> &compute_services,
                      const std::set<StorageService *> &storage_services,
                      const std::set<NetworkProximityService *> &network_proximity_services,
                      FileRegistryService *file_registry_service,
                      const std::string &hostname) :
                WMS(nullptr, nullptr, compute_services, storage_services, network_proximity_services, file_registry_service, hostname, "tresstestwms") {}

        int main() override;

    };

};


#endif //TASK_CLUSTERING_BATCH_SIMULATOR_STRESSTESTWMS_H
