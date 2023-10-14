#include "Simulator.h"


int main(int argc, char **argv) {

  auto simulator = new wrench::Simulator();
  return simulator->main(argc, argv);
}