#
# Kalman filter for  awheel encoder
#
# A Kalman filter against a simulated system.
#

#
# System
#


#rev per power
power = 35 
b = 0.68;
B = [0; b];

# process noise covarriance
Q = [1, 0.0; 0.0, 1];

# tick per rev
N = 16; 
n = N / (2 * pi());
C = [n, 0; 0, n];

# sensor noise covarriance
R = [1, 0; 0, 1];

# Initial Conditions
u = [power];
x = [0; b * u(1)];
t = 0;
t_end = 50;

#
# Kalman variables
#
x_hat = x;
P = [2, 2;, 2, 2];

#
# plot support, collect as we go
# 1 - time, 
# 2,3 - sensor tics and tics velocity,
# 4,5 - Kalman position and velocity
State = [t; 0; 0; 0; 0];

fileId = fopen('left-35-tics.txt','r');
ticsData = fscanf(fileId, '%f');

t_old = 0;
tics = 0;

for t_new = ticsData'

  # next time step
  dt = t_new - t_old;
  state_i(1) = t;
  disp(dt);
  A = [1, dt; 0, 0];


  # observed systems state
  tics = tics + 1;
  v_tics = 1 / dt;
  z = [tics; v_tics];
  
  state_i(2) = z(1);
  state_i(3) = z(2);

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
  state_i(4) = x_hat(1);
  state_i(5) = x_hat(2);
  State = cat(2, State, state_i');

  # updates
  t_old = t_new;
  
endfor
 

#plot(State(1, :), State(3, :), "k", State(1, :), State(5, :) , "b", State(1, :), State(7, :), "r");

