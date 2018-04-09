title: 'Math happens:  Stiffness matrix, residuals, and more'
author: N Ouyang
date: 2018-04-08 05:55:56
tags:
---
$$ $$

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
```bash
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
```bash
+ y (pitch)
^
|
----> + x (roll)

+ z (up out of page) (yaw)
```


Zeros defined as:
```bash
x: tip of proximal joint
y: center of proximal joint
z: neutral axis
```
Points 13 through 15 are at x=2.6 cm, and each x is spaced 5 mm apart.

```bash
xs = [4.6, 4.1, 3.5, 3.1, 2.6]
```
Because there is a mold line going down the center of the finger, thus our center points (positions 14 ... 2)  are at y = 0.1cm. Note also that the other two y positions are not equidistant from y=0.
```bash
ys = [0.4, 0.1, -0.2]
## ys = [0.4, 0, -0.2]   
```

In terms of applicability to real life, we are also assuming that we can zero the sensors right before grasping the object and then hold it still for a second in order to obtain our reading and thereby deduce our parameters.

## Experiment

The previous round of data collection was at small deflections. After discovering that the stop at the end of the triple beam balance, I was able to roughly double the amount of force I could apply to the finger before hitting the end of the triple beam balance.

Max forces at each x position before triple beam bottoms out (note that off-axis measurements reduce the max force I can apply)

```bash
140g
160 to 180g
200g
240g
300g
```

I collected data in intervals of 20 grams, three times at each position.

### Post-Process Data 

I took two data point for each force, one with no force applied as a "zero" calibration measurement to account for IMU instability over time, and one of the IMU sensor reading right after applying force (once the system stabilizes and the readings become constant).

Thus, to get the actual datapoints I subtracted the second reading from the first.

I did not use the x,y,z nor distance measurements from the IMU. I only used the rotation measurements for roll, pitch, and yaw.

## Math

### 1D Case 

In the one-axis case, the math is straightforward.

\begin{align}
\tau = k \times F
\end{align}

For example, one datapoint might be

\begin{align}
k &= F / \tau \\
k &= (20g \times 9.8 m/s^2)\,/\,0.1 \text{ degrees}
\end{align}

where `k` represents the stiffness of the finger. Let `c` represent the inverse of `k`.

Using least squares error, we may fit a line to find $\hat{c}$. 

\begin{align}
 \hat{c} &= \frac{1}{\hat{k}} \\
 \theta &= \tau \hat{c} + b
\end{align}

where `b` be a constant determined by the line of fit.

### Residuals

From the above, we may calculate the residuals of any of our estimated variables.
For instance, from our actual data we may obtain an estimate for `k`.

\begin{align}
 \tau_{data} &= \hat{k} \cdot \theta_{data} \\
\end{align}

Using this k we can go back and calculate estimates for the "true" torque, assuming our linear model was correct.

\begin{align}
 \hat{\tau} &= \hat{k} \cdot \theta_{data} 
\end{align}

We would then calculate our torque residuals as

\begin{align}
 \epsilon_{\tau} = \hat{\tau} - \tau 
\end{align}

If we plot a graph of (torque residuals) vs (estimate residuals) and find that our points are randomly scattered around a straight line, then our model well-approximates reality as sensed by a noisy sensor.

However, our residuals may instead follow a parabola, in which case we would want to amend our model to have higher order terms.

\begin{align}
 \hat{\tau} = \hat{k}\theta_{data} +c_1 \theta_{data} + c_2 \theta_{data}
\end{align}

and so forth. 

We may eventually use machine learning techniques such as logistic regression with basis functions in order to fit such higher order terms, if needed. Or perhaps we will not need to.


###  3D case

The 3d case is exactly the same, except now each of the variables are vectors / matrices. 

\begin{align}
\[ \vec{\tau} \ ]_{3xn}  = \[ k \]_{3x3} \cdot \[ \vec{\theta} \]_{3xn}
\end{align}

where

\begin{align}
\tau &= \[ \stackrel{3x1}{\tau_1} | \stackrel{3x1}{\tau_2} | ... |\stackrel{3x1}{\tau_n} \] \\
\\
\theta &= \[ \stackrel{3x1}{\theta_1} | \stackrel{3x1}{\theta_2} | ... |\stackrel{3x1}{\theta_n} \]
\end{align}


## First Round of Data 


### Graph
![torque vs deflection](/researchblog/images/temp-plot.png)

```bash
Coefficients: 
 [-0.00678065]
Intercept: 
 [0.7679924242424274]
Mean squared error: 0.29
```
From this graph we get that 
\begin{align}
 \hat{c} &= -0.00678065
\end{align}

We see that the IMU appears to create a very accurate linear line, as the average squared deviation is on the order of a tenth of a degree. 

### 2D Sanity Check

We can run "forward" and "backward" calculations as a sanity check. We have $\hat {k} = \frac{1}{0.00678065} =  147.5$ from our above least squares line. We can also plug in an individual datapoint, for instance (100 gram cm, 2.85 deg, at position 2 i.e. with no off-axis torque terms), and see that 4.6cm * 100g = 460 g cm. Dividing by 2.85 deg, we get approximately 150 g cm / deg, which matches $\hat{k}.

( Note: I have no idea if this is a reasonable stiffness (well, 1/stiffness) estimate in terms of absolute real-life estimates. )


### 3D Sanity Check: Simplify to 2D case 

We know that $\tau = r \times F$
\begin{align}
\begin{bmatrix}
    \tau_{x}       \\
    \tau_{y}       \\
    \tau_{z}       \\
\end{bmatrix} =
\Bigg[ \; K \; \Bigg]_{3x3}  \;
\begin{bmatrix}
    \theta_{x}       \\
    \theta_{y}       \\
    \theta_{z}       \\
\end{bmatrix} \\
\end{align}

Further, we can use some of the simplifying assumptions we made about to model our system, in order to have an idea of what values our math should result in for $k$.

We may also see that we will only ever have x and y components for $r$; z components for $F$; and thereforce (by how cross products work) only ever have x and y components for $\tau$.

**Off-axis**
\begin{align}
r \approx
\begin{bmatrix}
    r_x       \\
    r_y       \\
    0       \\
\end{bmatrix} \; \times \;
f \approx
\begin{bmatrix}
    0       \\
    0       \\
    f_z      \\
\end{bmatrix} \; =  \; \tau \; = 
\begin{bmatrix}
    \tau_x       \\
    \tau_y       \\
    0      \\
\end{bmatrix}\\
\end{align}


**On-Axis**
In the even more simplified case, if we do not apply the force off-axis and there is only a pitch
deflection

\begin{align}
r \approx
\begin{bmatrix}
    r_x       \\
    0       \\
    0       \\
\end{bmatrix} \; \times \;
f \approx
\begin{bmatrix}
    0       \\
    0       \\
    f_z      \\
\end{bmatrix} \; =  \; \tau \; = 
\begin{bmatrix}
    0 \\
    \tau_y       \\
    0      \\
\end{bmatrix}\\
\end{align}

We **will** have enough nonzero values for the xyz components of $\theta$ that we will be able to calculate a nondegenerate estimate for $k$. This is thanks to applying the force off-axis, causing the finger to roll and create non-zero elements for $\theta_y$ ( our roll) and $\theta_z$ (our yaw).

### 3D Sanity Case: Pick datapoints with $\approx 0$ values

We can selectively pick datapoints which have tiny values in some components and check that the
resulting $\hat{K}$ matrix is as we expect.

###  Further Sanity Checks
 
We can also make sure that for off-axis forces on either side of the finger, one should be positive and one negative, and they should be roughly the same order magnitude. 

Note that, because pos 1 is +4mm but  pos 3 is only -2mm, thus $ | \theta_{pos3} |$ should be less than $ | \theta_{pos1} | $.





## Notes

* I somewhat tried to stick to the convention of "uppercase" letters for matrices, lowercase for constants and vectors, hats for estimates, and vector signs for well, vectors.  
But not really, because I got lazy.

* There was a brief explanation of how, if the residuals are plotted against the actual data, then we would expect a slight upward linear trend in the resulting datapoints. TODO: look into the statistics behind this. What we actually want is the residuals plotted against our estimates. That is, if we are looking at the torque residuals,  
\begin{align}
    \vec{\epsilon}_\tau = \vec{\tau}_{\text{calculated}} - \hat{\vec{\tau}}_{\text{estimated from } k\theta}
\end{align}
We want to plot 
  * $\epsilon_\tau$ vs. $\tau_{\text{estimated from }k\theta}$ and NOT 
  * $\epsilon_\tau$ vs. $\tau_{\text{calculated}}$

  * Note: $\tau_{\text{calculated}}$ is taken directly from the xyz position and the force we applied to get our datapoint.
\begin{align}
    \vec{\tau}_{\text{calculated}} = \vec{r}_{data} \times \vec{F}_{data}
\end{align}
  * Note: Then from fitting a line vs the deflections (that we also physically measured) we then
  derived a $\hat{K}$.  We then take this $\hat{K}$ and multiply against the deflections
  $\theta_{data}$ to work out our $\hat{\tau}_{\text{estimated from }k\theta}$.

## end
