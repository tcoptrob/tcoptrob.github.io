---
  hide:
    - navigation
---

# Optimization tools

If you would like to contribute to this list, you can use this form or send an email to tc.opt.rob@gmail.com.

## OPEN SOURCE LIBRARIES AND TOOLBOXES

### ACADO

ACADO Toolkit is an open-source software environment and algorithm collection for automatic control and dynamic optimization. It also uses the direct multiple shooting method. ACADO is written in C++ but comes with a user-friendly Matlab interface. Authors are Moritz Diehl,  Boris Houska, Hand Joachim Ferreau, Milan Vukov, Rien Quiynen, KU Leuven.

License: Gnu LGPL

Webpage: www.acadotoolkit.org

### CasADi

CasADi is an open-source tool for nonlinear optimization and algorithmic differentiation. It facilitates rapid — yet efficient — implementation of different methods for numerical optimal control, both in an offline context and for nonlinear model predictive control (NMPC).

License: GNU Lesser General Public License (LGPL), v3.0

Webpage: https://web.casadi.org/

### Control Toolbox

The Control Toolbox ('CT'), is a C++ library for modeling, control, estimation, trajectory optimization and model predictive control. The CT is applicable to a broad class of dynamic systems, but features additional tools specially designed for robotics. The library contains several tools to design and evaluate controllers, model dynamical systems and numerically solve optimal control problems.

License: BSD 2-clause

Webpage: https://ethz-adrl.github.io/ct/

### Crocoddyl

Crocoddyl is an optimal control library for robot control under contact sequence. Its solver is based on an efficient Differential Dynamic Programming (DDP) algorithm. Crocoddyl computes optimal trajectories along to optimal feedback gains. It uses Pinocchio for fast computation of robot dynamics and its analytical derivatives.

Weboage: https://github.com/loco-3d/crocoddyl

License: BSD 3-clause


### Ipopt

Ipopt is an open-source solver for large-scale nonlinear continuous optimization. It can be used from modeling environments, such as AIMMS, AMPL, GAMS, or Matlab, and it is also available as a callable library with interfaces to C++, C, Fortran, Java, and R. Ipopt uses an interior point method, together with a filter linear search procedure.

License: Eclipse Public License

Webpage: https://github.com/coin-or/Ipopt


### Manopt

Matlab, Python and Julia toolboxes for unconstrained optimization on manifolds and matrices, making it easy to deal with various types of constraints and symmetries which arise naturally in applications, such as orthonormality, low rank, positivity and invariance under group actions.

License: GNU General Public License (GPL) v3.0

Webpage: https://www.manopt.org/


### LexLS
A fast C++ solver for lexicographic least-squares problems based on the lexicographic QR (l-QR) presented in the paper Efficient resolution of potentially conflicting linear constraints in robotics, by D. Dimitrov, A. Sherikov and P.-B. Wieber.

License: BSD 3-clause

Webpage: https://github.com/jrl-umi3218/lexls


### NLOpt

NLopt is a free/open-source library for nonlinear optimization, providing a common interface for a number of different free optimization routines available online as well as original implementations of various other algorithms.

License: GNU Lesser General Public License

Webpage: https://nlopt.readthedocs.io


### Open Optimal Control Library (OpenOCL)

A toolbox that uses C++ implementations of CasADi, Ipopt, and acados in the backend. Derivatives are calculated automatically using CasADi. For trajectory optimization they use the direct collocation method and solve the non-linear program using CasADi and Ipopt. OpenOCL has a basic interface to acados which provides some fast SQP methods.

License: BSD 3-clause

Webpage: https://openocl.org/


### qpOASES

qpOASES is an open-source C++ implementation of the recently proposed online active set strategy, which was inspired by important observations from the field of parametric quadratic programming (QP). It has several theoretical features that make it particularly suited for model predictive control (MPC) applications. Further numerical modifications have made qpOASES a reliable QP solver, even when tackling semi-definite, ill-posed or degenerated QP problems. Moreover, several interfaces to third-party software like ​Matlab or ​Simulink are provided that make qpOASES easy-to-use even for users without knowledge of C/C++.

License: GNU Lesser General Public License (LGPL), v2.1

Webpage: https://projects.coin-or.org/qpOASES


### qpSWIFT

qpSWIFT is a sparse quadratic programming solver built for embedded applications like robotics. qpSWIFT employs a primal-dual interior-point method with Mehrotra predictor-corrector steps and Nesterov-Todd scaling. The core of the solver is written in ANSI-C with interfaces to popular programming languages like matlab, python, and simulink. To know more about the installation and usage of the solver, please refer to the pdf documentation available at (pdf) or the web documentation available at (github wiki). For details on the algorithm, please refer to the research article at (link)

License:  GNU General Public License (GPL) v3.0

Webpage:  https://qpswift.github.io/

Repository: https://github.com/qpSWIFT/qpSWIFT


### Roboptim

Roboptim is a modern open-source C++ library for numerical optimization applied to robotics by Thomas Moulard (LAAS-CNRS, Toulouse, France and AIST-JRL, Tsukuba, Japan).

License: LGPL

Webpage:  http://www.roboptim.net/


## OTHER LIBRARIES AND TOOLBOXES

### MUSCOD

MUSCOD is a powerful optimal control code for systems ordinary differential and differential-algebraic equations and can be used for robotics problems. It uses a direct multiple shooting method.  MUSCOD has been written by Hans Georg Bock, Daniel Leineweber and co-workers (University of Heidelberg, Germany).

Webpage: http://www.iwr.uni-heidelberg.de/~agbock/RESEARCH/muscod.php, https://neos-server.org/neos/solvers/miocp:MUSCOD-II/AMPL.html


### OCPID-DAE1

A page with general information about optimal control and the code OCPID.DAE1 by Matthias Gerdts (Universität der Bundeswehr, Munich, Germany):

Webpage: http://www.optimal-control.de

### SNOPT

SNOPT is a general-purpose system for constrained optimization. It minimizes a linear or nonlinear function subject to bounds on the variables and sparse linear or nonlinear constraints. It is suitable for large-scale linear and quadratic programming and for linearly constrained optimization, as well as for general nonlinear programs.

Webpage: https://web.stanford.edu/group/SOL/snopt.htm
