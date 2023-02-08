---
  hide:
    - navigation
---

# Modeling Tools

If you would like to contribute to this list, you can use this form or send an email to tc.opt.rob@gmail.com.

## RBDL - Rigid body dynamics library

RBDL contains highly efficient code for both forward and inverse dynamics of rigid multibody systems. It includes the Recursive Newton Euler Algorithm, the Composite Rigid Body Algorithm, and the Articulated Body Algorithm. Furthermore, it contains functions for forward and inverse kinematics and contact handling. The code is written by Martin Felis, University of Heidelberg, and follows the book "Rigid Body Dynamics Algorithms" of Roy Featherstone.

Webpage: https://github.com/rbdl/rbdl (old: https://rbdl.bitbucket.io/)

Licence: zlib free software license

## iDynTree multibody dynamics library

iDynTree is a library of robots dynamics algorithms for control, estimation, and simulation. It is specifically designed for free-floating robots, but it is possible to use it also with fixed-base robots. iDynTree is written in C++ language, but thanks to SWIG it is possible to use the iDynTree algorithms in several other languages. Support and documentation are provided in particular for C++, Matlab and Python. 

Webpage: https://github.com/robotology/idyntree

License: GNU Lesser General Public License v3.0 or v2.1

## Pinocchio - Fast Forward Inverse Dynamic for Multibody Systems

Pinocchio is a C++ library that instantiates the state-of-the-art Rigid Body Algorithms for poly-articulated systems based on revisited Roy Featherstone's algorithms. Besides, Pinocchio provides the analytical derivatives of the main Rigid-Body Algorithms like the Recursive Newton-Euler Algorithm or the Articulated-Body Algorithm. Pinocchio is first tailored for robotics applications, but it can be used in extra contexts (biomechanics, computer graphics, vision, etc.). It is built upon Eigen for linear algebra and FCL for collision detection. Pinocchio comes with a Python interface for fast code prototyping, directly accessible through Conda. Pinocchio is now at the heart of various robotics software as Crocoddyl, an open-source and efficient Differential Dynamic Programming solver for robotics, the Stack-of-Tasks, an open-source and versatile hierarchical controller framework or the Humanoid Path Planner, an open-source software for Motion and Manipulation Planning.

Webpage: https://stack-of-tasks.github.io/pinocchio/

License: BSD-2-Clause license

## HPP-FCL

HPP-FCL is a generic purpose C++ library for efficient and reliable collision detection between geometries. It is an extension of the famous FCL library, including many additional features like security margin, distance lower-bound computations, etc. It supports a large set of geometries: basic shapes, height fields, octrees, etc. and comes with Python bindings for easy code prototyping. HPP-FCL is already connected to many existing robotics libraries, including Pinocchio, OCS2, Crocoddyl and the Humanoid Path Planner.

Webpage: https://github.com/humanoid-path-planner/hpp-fcl

License: BSD-2-Clause license

## RBDyn

RBDyn provides a set of classes and functions to model the dynamics of rigid body systems. The implementation is based on Roy Featherstone Rigid Body Dynamics Algorithms book and other states of the art publications.

Webpage: https://github.com/jrl-umi3218/RBDyn

License: BSD 2-clause

## Drake - Model-based design and verification for robotics

Drake is a C++ toolbox started by the Robot Locomotion Group at the MIT Computer Science and Artificial Intelligence Lab (CSAIL). The core development is currently led by the Toyota Research Institute. It is a collection of tools for analyzing the dynamics of our robots and building control systems for them, with a heavy emphasis on optimization-based design/analysis.

Webpage: https://drake.mit.edu

License: BSD 3-clause

## Robotran - Symbolic generator of multibody systems

Robotran is a symbolic software to model and analyze MultiBody Systems (MBS). It is a powerful tool to deal with both industrial and research applications, such as: robot manipulators, parallel actuators, human body, car suspensions, railway bogies, transmission mechanisms, machine tools etc.

Webpage: https://www.robotran.be/

## Control Toolbox 

The Control Toolbox ('CT'), is a C++ library for modeling, control, estimation, trajectory optimization and model predictive control. The CT is applicable to a broad class of dynamic systems, but features additional tools specially designed for robotics. This page outlines its general concept, its major building blocks and highlights selected application examples. The library contains several tools to design and evaluate controllers, model dynamical systems and numerically solve optimal control problems.

Webpage: https://ethz-adrl.github.io/ct/

License: BSD 2-clause

## Crocoddyl

Crocoddyl is an optimal control library for robot control under contact sequence. Its solver is based on an efficient Differential Dynamic Programming (DDP) algorithm. Crocoddyl computes optimal trajectories along to optimal feedback gains. It uses Pinocchio for fast computation of robot dynamics and its analytical derivatives.

Webpage: https://github.com/loco-3d/crocoddyl

License: BSD 3-clause
