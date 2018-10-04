
#include <iostream>
#include <wrench-dev.h>
#include "Simulator.h"
#include "StressTestWMS.h"

XBT_LOG_NEW_DEFAULT_CATEGORY(stress_test_simulator, "Log category for Stress Test Simulator");

using namespace wrench;

unsigned long Simulator::sequence_number = 0;

int Simulator::main(int argc, char **argv) {

  // Create and initialize a simulation
  auto simulation = new wrench::Simulation();
  simulation->init(&argc, argv);

  // Parse command-line arguments
  unsigned long num_jobs;
  unsigned long num_cs;
  unsigned long num_ss;
  unsigned long num_nps;

  if ((argc != 5) or
          ((sscanf(argv[1], "%lu", &num_jobs) != 1) or (num_jobs < 1)) or
          ((sscanf(argv[2], "%lu", &num_cs) != 1)   or (num_cs < 1)) or
          ((sscanf(argv[3], "%lu", &num_ss) != 1)   or (num_ss < 1)) or
          ((sscanf(argv[4], "%lu", &num_nps) != 1))
          ) {
    std::cerr << "Usage: " << argv[0] << " <num jobs> <num compute services> <num storage services> <num network proximity services>" << "\n";
    exit(1);
  }

  // Setup the simulation platform
  setupSimulationPlatform(simulation, num_cs, num_ss);

  // Create the Compute Services
  std::set<ComputeService *> compute_services;
  for (unsigned int i=0; i < num_cs; i++) {
    std::string hostname = "CS_host_" + std::to_string(i);
    compute_services.insert(simulation->add(new MultihostMulticoreComputeService(hostname, {hostname}, 0, {}, {})));
  }

  // Create the Storage Services
  std::set<StorageService *> storage_services;
  for (unsigned int i=0; i < num_ss; i++) {
    std::string hostname = "SS_host_" + std::to_string(i);
    storage_services.insert(simulation->add(new SimpleStorageService(hostname, pow(2,40), {}, {})));
  }
  // Create the Network Proximity Services
  std::set<NetworkProximityService *> network_proximity_services;
  for (unsigned int i=0; i < num_nps; i++) {
    std::string hostname = "CS_host_0";
    std::vector<std::string> participating_hosts;
    for (auto cs : compute_services) {
      participating_hosts.push_back(cs->getHostname());
    }
    for (auto ss : storage_services) {
      participating_hosts.push_back(ss->getHostname());
    }

    network_proximity_services.insert(simulation->add(new NetworkProximityService(hostname, participating_hosts, {}, {})));
  }

  // Create a File Registry Service
  FileRegistryService *file_registry_service = simulation->add(new FileRegistryService("CS_host_0"));

  // Create the WMS
  WMS *wms = simulation->add(new StressTestWMS(compute_services, storage_services, network_proximity_services, file_registry_service, "CS_host_0"));


  // Create the Workflow
  Workflow *workflow = createWorkflow(num_jobs);
  wms->addWorkflow(workflow, 0);

  // Launch the simulation
  try {
    WRENCH_INFO("Launching simulation!");
    simulation->launch();
  } catch (std::runtime_error &e) {
    std::cerr << "Simulation failed: " << e.what() << "\n";
    exit(1);
  }
  WRENCH_INFO("Simulation done!");

  return 0;
}

void Simulator::setupSimulationPlatform(Simulation *simulation, unsigned long num_cs, unsigned long num_ss) {

  // Create a the platform file
  std::string xml = "<?xml version='1.0'?>\n";
  xml += "<!DOCTYPE platform SYSTEM \"http://simgrid.gforge.inria.fr/simgrid/simgrid.dtd\">\n";
  xml += "<platform version=\"4.1\">\n";
  xml += "   <zone id=\"AS0\" routing=\"Full\">\n";

  // CS hosts
  xml += "         <cluster id=\"cluster_cs\" prefix=\"CS_host_\" suffix=\"\" radical=\"0-";
  xml += std::to_string(num_cs-1) + "\" speed=\"1f\" core=\"16\" bw=\"125GBps\" lat=\"0us\" router_id=\"cluster_cs_router\"/>\n";

  // SS hosts
  xml += "         <cluster id=\"cluster_ss\" prefix=\"SS_host_\" suffix=\"\" radical=\"0-";
  xml += std::to_string(num_ss-1) + "\" speed=\"1f\" core=\"16\" bw=\"125GBps\" lat=\"0us\" router_id=\"cluster_ss_router\"/>\n";

  // Connecting CS cluster to SS cluster
  xml += "      <link id=\"wide_area_link\" bandwidth=\"10GBps\" latency=\"100ms\"/>\n";
  xml += "      <zoneRoute src=\"cluster_cs\" dst=\"cluster_ss\" gw_src=\"cluster_cs_router\" gw_dst=\"cluster_ss_router\">\n";
  xml += "         <link_ctn id=\"wide_area_link\" />\n";
  xml += "      </zoneRoute>\n";
  xml += "   </zone>\n";
  xml += "</platform>\n";

  FILE *platform_file = fopen("/tmp/platform.xml", "w");
  fprintf(platform_file, "%s", xml.c_str());
  fclose(platform_file);

  try {
    simulation->instantiatePlatform("/tmp/platform.xml");
  } catch (std::invalid_argument &e) {  // Unfortunately S4U doesn't throw for this...
    throw std::runtime_error("Invalid generated XML platform file");
  }
}

wrench::Workflow *Simulator::createWorkflow(unsigned long num_jobs) {
  Workflow *workflow = new Workflow();
  // One task per job, all independent
  for (unsigned int i=0; i < num_jobs; i++) {
    WorkflowTask *task = workflow->addTask("task_" + std::to_string(i), 10.0, 1, 1, 1.0, 0);
    task->addOutputFile(workflow->addFile("file_" + std::to_string(i), 10000));
  }
  return workflow;
}
