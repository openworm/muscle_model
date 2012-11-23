#include <Python.h>
#include <iostream>
#include <PyramidalSimulation.h>

using namespace std;

int main(){

  PyramidalSimulation simulation;
  simulation.setup();

  //example usage, run 10 simulation steps with the default value (set in python)
  simulation.run();
  double potential;
  int i;
  i = 0;
  while (i < 10) {
    potential = simulation.run();
    cout << potential<<endl;
    i++;
  }
  
  //I suppose this needs to somehow end up in the simulation destructor?
  Py_Finalize();
  return 0;
}
