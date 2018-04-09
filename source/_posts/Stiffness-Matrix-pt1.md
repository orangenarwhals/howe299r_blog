title: 'Math happens:  Stiffness matrix, residuals, and more'
author: N Ouyang
date: 2018-04-08 05:55:56
tags:
---
<script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=TeX-MML-AM_CHTML' async></script>

## Motivation

In grasp stability, we often use a friction cone model where if our forces are outside the friction cone, slip occurs and our grasp is consider unstable. In order to determine the friction cone, we need nine variables: the xyz of the contact force, contact location, and force normals (how much force is applied tangentially vs perpendicularly). 

We have determined that the three pressure sensors on the finger by themselves are not sufficient in and of themselves to give us all nine datapoints -- using data from them alone, we are not able to distinguish marginal cases, where given the same starting position of the grasper relative to the object, sometimes the object is grasped without slip and sometimes the object falls. 

Therefore we would like to add more sensors in order to resolve these unknowns. We would like a force contact location sensor. Although there is a 6 axis force torque sensor, it costs multiple thousands of dollars and is finicky and fragile. Thus, we would like to see if we can estimate force and torque from an IMU instead.

## Assumptions

Based on the results from the previous analysis, we can say that the IMU seems fairly reasonably precise, with very small mean errors from the least-squares fit line.

(The error could come from both sensor noise and from a mismatch between our simplifed model and reality in terms of the bending of the finger).

Here we are making a few simplifying assumptions:

1. There is a linear relationship between force and deflection, or alternatively torque and angle of deflection
2. The center of the axis of rotation was at the tip of the proximal joint
(in reality, likely it is two or three mm shifted outward, and changes as the flex increases)
3. We consider the z axis to be defined respect to the surface of the finger, so that z=0 is always at the tip of the finger

## Setup (coordinates)
```
=======      ====================.
 {CL}  || --- || 15  12  9  6  3 ||
 {A} [xy=0]-- || 14  11  8  5  2 ||
 {MP}  || --- || 13  10  7  4  1 ||
=======      ====================.


  [[---]]
||  WEB  ||
||  CAM  ||
  ||--- ||
  
```

Coordinates
```
+ y (pitch)
^
|
----> + x (roll)

+ z (up out of page) (yaw)
```


Zeros defined as:
```
x: tip of proximal joint
y: center of proximal joint
z: neutral axis
```
Points 13 through 15 are at x=2.6 cm, and each x is spaced 5 mm apart.

```
xs = [4.6, 4.1, 3.5, 3.1, 2.6]
```
Because there is a mold line going down the center of the finger, thus our center points (positions 14 ... 2)  are at y = 0.1cm. Note also that the other two y positions are not equidistant from y=0.
```
ys = [0.4, 0.1, -0.2]
## ys = [0.4, 0, -0.2]   
```

In terms of applicability to real life, we are also assuming that we can zero the sensors right before grasping the object and then hold it still for a second in order to obtain our reading and thereby deduce our parameters.

## Experiment

The previous round of data collection was at small deflections. After discovering that the stop at the end of the triple beam balance, I was able to roughly double the amount of force I could apply to the finger before hitting the end of the triple beam balance.

Max forces at each x position before triple beam bottoms out (note that off-axis measurements reduce the max force I can apply)

```
140g
160 to 180g
200g
240g
300g
```

I collected data in intervals of 20 grams, three times at each position.

### Post processing data

I took two data point for each force, one with no force applied as a "zero" calibration measurement to account for IMU instability over time, and one of the IMU sensor reading right after applying force (once the system stabilizes and the readings become constant).

Thus, to get the actual datapoints I subtracted the second reading from the first.

I did not use the x,y,z nor distance measurements from the IMU. I only used the rotation measurements for roll, pitch, and yaw.

## Math

In the one-axis case, the math is straightforward.

\begin{align}
\tau = k \times F
\end{align}


## First round of data

### Sanity Check

### Results


### Graphs


<!--
$$

\begin{eqnarray}
\nabla\cdot\vec{E} &=& \frac{\rho}{\epsilon_0} \\
\nabla\cdot\vec{B} &=& 0 \\
\nabla\times\vec{E} &=& -\frac{\partial B}{\partial t} \\
\nabla\times\vec{B} &=& \mu_0\left(\vec{J}+\epsilon_0\frac{\partial E}{\partial t} \right)
\end{eqnarray}



\begin{align}
a+b_2^2 &= 2 \\
a &= 2-b \\
\alpha \\
\frac{q}{b} &= \partial a \\
\end{align}


\begin{bmatrix}
    x_{11}       & x_{12} & x_{13} & \dots & x_{1n} \\\\
    x_{21}       & x_{22} & x_{23} & \dots & x_{2n} \\\\
     \\\\
    x_{d1}       & x_{d2} & x_{d3} & \dots & x_{dn}
\end{bmatrix}


\alpha

$${23} & \dots & x_{2n} \\\\
     \\\\
    x_{d1}       & x_{d2} & x_{d3} & \dots & x_{dn}
\end{bmatrix}


\alpha

-->