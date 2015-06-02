#
# Kalman filter for  awheel encoder
#
# A Kalman filter against a simulated system.
#

#
# System
#

# time step
dt = 1;
A = [1, dt; 0, 0];

#rev per power 
b = 1;
B = [0; b];
# process noise covarriance
Q = [1, 0.0; 0.0, 1];
# tick per rev
N = 25; 
n = N / (2 * pi());
C = [n, 0; 0, n];
# sensor noise covarriance
R = [1, 0; 0, 1];

# Initial Conditions
u = [1];
x = [0; b * u(1)];
t = 0;
t_end = 50;

# generate process and sensor noise samples
W = mvnrnd(0, [1, 0; 0, 1], (t_end / dt) + 1)';

#
# Kalman variables
#
x_hat = x;
P = [2, 2;, 2, 2];

#
# plot support, collect as we go
# 1 - time, 
# 2,3 - actual position and velocity, 
# 4,5 - sensor tics and tics velocity,
# 6,7 - Kalman position and velocity
State = [t; x(1); x(2); 0; 0; 0; 0];

do

  #
  # Update simulated system
  #
  state_i = zeros(7, 1);

  # next time step
  t = t + dt;
  state_i(1) = t;

  #
  # Walk system forward and make sensor observation 
  #

  # grab prior values for approximating sensor
  x_old = x;
  z_old = C * x_old;

  # walk
  x = A * x + B * u + W(t);
  z = C * x;

  # sensor error is all quantization error - tics are discrete
  tics_old = floor(z_old(1));
  tics_new = floor(z(1));
  v_tics = (tics_new - tics_old) / dt;
  z = [tics_new; v_tics];

  # record actual system state
  state_i(2) = x(1);
  state_i(3) = x(2);

  # record observed systems state
  state_i(4) = z(1);
  state_i(5) = z(2);

  #
  # Kalman
  #

  # predict
  x_hat = A * x_hat + B * u;
  P = A * P * (A') + Q;

  # update
  y_hat = z - C * x_hat;
  S = C * P * (C') + R;
  K = P * (C') * inverse(S);
  x_hat = x_hat + K * y_hat;
  P = (eye(2) - K * C) * P;

  # record estimated state
  state_i(6) = x_hat(1);
  state_i(7) = x_hat(2);
  State = cat(2, State, state_i);
  
until (t > t_end)
 

plot(State(1, :), State(3, :), "k", State(1, :), State(5, :) , "b", State(1, :), State(7, :), "r");

