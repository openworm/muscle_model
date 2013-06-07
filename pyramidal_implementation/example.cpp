// The MIT License (MIT)
//
// Copyright (c) 2011, 2013 OpenWorm.
// http://openworm.org
//
// All rights reserved. This program and the accompanying materials
// are made available under the terms of the MIT License
// which accompanies this distribution, and is available at
// http://opensource.org/licenses/MIT
//
// Contributors:
//      OpenWorm - http://openworm.org/people.html
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
// OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
// USE OR OTHER DEALINGS IN THE SOFTWARE.

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
