#
# Kalman filter for  awheel encoder
#
# A Kalman filter against a simulated system.
#

#
# System
#


#rev per power
power = 35;
b = 0.37;
B = [0; b];

# process noise covarriance
Q = [1, 0.0; 0.0, 1];

# tick per rev
N = 16; 
n = N / (2 * pi());
C = [n, 0; 0, n];

# sensor noise covarriance
R = [5, 0; 0, 5];

# Initial Conditions
u = [power];
x = [0; b * u(1)];
t_end = 50;

#
# Kalman variables
#
x_hat = x;
P = [1, 1; 1, 1];

#
# plot support. At each new observation...
# 1 - time, 
# 2,3 - model prediction - tics and tics velocity
# 4,5 - sensor reading - tics and tics velocity
# 6,7 - kalman filter - tics and tics velocity
State = [0; 0; 0; 0; 0; 0; 0];

fileId = fopen('schmitt-left-actual-tics.txt','r');
ticsData = fscanf(fileId, '%f');

t_old = 0;
tics = 0;

# The timestamp of each leading edge detection/event
for t_new = ticsData'

  state_i(1) = t_new;

  # system dynamics for a variable time stamp
  dt = t_new - t_old;
  A = [1, dt; 0, 0];

  # observed systems state
  tics = tics + 1;
  v_tics = 1 / dt;
  z = [tics; v_tics];

  # translate to state variable for comparision
  state_i(4) = z(1) / n;
  state_i(5) = z(2) / n;

  #
  # Kalman
  #

  # predict
  x_hat = A * x_hat + B * u;
  P = A * P * (A') + Q;

  state_i(2) = x_hat(1);
  state_i(3) = x_hat(2);

  # update
  y_hat = z - C * x_hat;
  S = C * P * (C') + R;
  K = P * (C') * inverse(S);
  x_hat = x_hat + K * y_hat;
  P = (eye(2) - K * C) * P;

  # record estimated state
  state_i(6) = x_hat(1);
  state_i(7) = x_hat(2);
  State = cat(2, State, state_i');

  # updates
  t_old = t_new;
  
endfor
 

#plot(State(1, :), State(3, :), "k", State(1, :), State(5, :) , "b", State(1, :), State(7, :), "r");

model_v_color = "b";
sensor_v_color = "r";
kalman_v_color = 'k';

#plot(State(1, :), State(2, :), model_v_color, State(1, :), State(4, :), sensor_v_color, State(1, :), State(6, :), kalman_v_color);

plot(State(1, :), State(3, :), model_v_color, State(1, :), State(5, :), sensor_v_color, State(1, :), State(7, :), kalman_v_color);

axis([0, 20, 0, 30]);