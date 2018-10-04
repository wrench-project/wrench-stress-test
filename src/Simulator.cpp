
#include <iostream>
#include <wrench-dev.h>
#include "Simulator.h"

XBT_LOG_NEW_DEFAULT_CATEGORY(task_clustering_simulator, "Log category for Stress Test Simulator");

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
  unsigned long num_frs;

  if ((argc != 6) or
          ((sscanf(argv[1], "%lu", &num_jobs) != 1) or (num_jobs < 1)) or
          ((sscanf(argv[2], "%lu", &num_cs) != 1) or (num_cs < 1)) or
          ((sscanf(argv[3], "%lu", &num_ss) != 1) or (num_ss < 1)) or
          ((sscanf(argv[4], "%lu", &num_nps) != 1) or (num_nps < 1)) or
          ((sscanf(argv[4], "%lu", &num_frs) != 1) or (num_frs < 1))
          ) {
    std::cerr << "Usage: " << argv[0] << " <num jobs> <num compute services> <num storage services> <num network proximity services> <num file registry services>" << "\n";
    exit(1);
  }

  // Setup the simulation platform
  setupSimulationPlatform(simulation, num_cs, num_ss);

  // Create the Compute Services
  std::vector<ComputeService *> compute_services;
  for (unsigned int i=0; i < num_cs; i++) {
    std::string hostname = "CS_host_" + std::to_string(i);
    compute_services.push_back(simulation->add(new MultihostMulticoreComputeService(hostname, {hostname}, 0, {}, {})));
  }

  // Create the Storage Services
  std::vector<StorageService *> storage_services;
  for (unsigned int i=0; i < num_cs; i++) {
    std::string hostname = "SS_host_" + std::to_string(i);
    storage_services.push_back(simulation->add(new SimpleStorageService(hostname, pow(2,40), {}, {})));
  }

#if 0
  // Create the WMS
  WMS *wms = nullptr;
  try {
    wms = createWMS("Login", batch_service, max_num_jobs, scheduler_spec);
  } catch (std::invalid_argument &e) {
    std::cerr << "Cannot instantiate WMS: " << e.what() << "\n";
    exit(1);
  }

  try {
    simulation->add(wms);
  } catch (std::invalid_argument &e) {
    std::cerr << "Cannot add WMS to simulation: " << e.what() << "\n";
    exit(1);
  }


  // Create the Workflow
  Workflow *workflow = nullptr;
  try {
    workflow = createWorkflow(argv[4]);
  } catch (std::invalid_argument &e) {
    std::cerr << "Cannot create workflow: " << e.what() << "\n";
    exit(1);
  }
  wms->addWorkflow(workflow, workflow_start_time);

  // Launch the simulation
  try {
    WRENCH_INFO("Launching simulation!");
    simulation->launch();
  } catch (std::runtime_error &e) {
    std::cerr << "Simulation failed: " << e.what() << "\n";
    exit(1);
  }
  WRENCH_INFO("Simulation done!");


  std::cout << "MAKESPAN=" << (workflow->getCompletionDate() - workflow_start_time) << "\n";
  std::cout << "NUM PILOT JOB EXPIRATIONS=" << this->num_pilot_job_expirations_with_remaining_tasks_to_do << "\n";
  std::cout << "TOTAL QUEUE WAIT SECONDS=" << this->total_queue_wait_time << "\n";
  std::cout << "USED NODE SECONDS=" << this->used_node_seconds << "\n";
  std::cout << "WASTED NODE SECONDS=" << this->wasted_node_seconds << "\n";
  std::cout << "CSV LOG FILE=" << csv_batch_log << "\n";

#endif

  return 0;
}

void Simulator::setupSimulationPlatform(Simulation *simulation, unsigned long num_cs, unsigned long num_ss) {

  // Create a the platform file
  std::string xml = "<?xml version='1.0'?>\n";
  xml += "<!DOCTYPE platform SYSTEM \"http://simgrid.gforge.inria.fr/simgrid/simgrid.dtd\">\n";
  xml += "<platform version=\"4.1\">\n";
  xml += "   <zone id=\"AS0\" routing=\"Full\">\n";

  // CS hosts
  xml += "      <zone id=\"zone_cluster_cs\" routing=\"Cluster\">\n";
  xml += "         <cluster id=\"cluster_cs\" prefix=\"CS_host_\" suffix=\"\" radical=\"0-";
  xml += std::to_string(num_cs-1) + "\" speed=\"1f\" core=\"16\" bw=\"125GBps\" lat=\"0us\"/>\n";
  xml += "         <router id=\"cluster_cs_router\"/>\n";
  xml += "         <backbone id=\"cluster_cs_backbone\" bandwidth=\"100GBps\" latency=\"50us\"/>\n";
  xml += "      </zone>\n";

  // SS hosts
  xml += "      <zone id=\"zone_cluster_ss\" routing=\"Cluster\">\n";
  xml += "         <cluster id=\"cluster_ss\" prefix=\"SS_host_\" suffix=\"\" radical=\"0-";
  xml += std::to_string(num_ss-1) + "\" speed=\"1f\" core=\"16\" bw=\"125GBps\" lat=\"0us\"/>\n";
  xml += "         <router id=\"cluster_ss_router\"/>\n";
  xml += "         <backbone id=\"cluster_ss_backbone\" bandwidth=\"100GBps\" latency=\"50us\"/>\n";
  xml += "      </zone>\n";

  // Connecting CS cluster to SS cluster
  xml += "      <link id=\"wide_area_link\" bandwidth=\"10GBps\" latency=\"100ms\"/>\n";
  xml += "      <zoneRoute src=\"zone_cluster_cs\" dst=\"zone_cluster_ss\" gw_src=\"cluster_cs_router\" gw_dst=\"cluster_ss_router\">\n";
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

Workflow *Simulator::createWorkflow(std::string workflow_spec) {

  #if 0
  std::istringstream ss(workflow_spec);
  std::string token;
  std::vector<std::string> tokens;

  while(std::getline(ss, token, ':')) {
    tokens.push_back(token);
  }

  if (tokens[0] == "indep") {
    if (tokens.size() != 5) {
      throw std::invalid_argument("createWorkflow(): Invalid workflow specification " + workflow_spec);
    }
    try {
      return createIndepWorkflow(tokens);
    } catch (std::invalid_argument &e) {
      throw;
    }

  } else if (tokens[0] == "levels") {
    if ((tokens.size() == 2) or (tokens.size() - 2) % 3) {
      throw std::invalid_argument("createWorkflow(): Invalid workflow specification " + workflow_spec);
    }
    try {
      return createLevelsWorkflow(tokens);
    } catch (std::invalid_argument &e) {
      throw;
    }

  } else if (tokens[0] == "dax") {
    if (tokens.size() != 2) {
      throw std::invalid_argument("createWorkflow(): Invalid workflow specification " + workflow_spec);
    }
    try {
      return createDAXWorkflow(tokens);
    } catch (std::invalid_argument &e) {
      throw;
    }

  } else {
    throw std::invalid_argument("createWorkflow(): Unknown workflow type " + tokens[0]);
  }
  #endif
  return nullptr;
}
