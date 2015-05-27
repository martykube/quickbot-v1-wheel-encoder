#
# System
#
% time step
dt = 1;
A = [1, dt; 0, 0];

%rev per power 
b = 6;
B = [0; b];
Q = [1, 0;, 1, 0];

C = [0, 1];
R = [1];

% Initial Conditions
x = [0; 0];
u = [0.5];
t = 0;
t_end = 5;

# generate process and sensor noise samples
W = mvnrnd(0, [1, 0; 0, 1], (t_end / dt) + 1)';
V = mvnrnd(0, [20], (t_end / dt) + 1)';


#
# Kalman variables
#
x_hat = x;
P = [2, 2;, 2, 2];

#
# plot support, collect as we go
# time, position, rotation velocity, observed velocity
State = [t; x(1); x(2); x(2)];

do
  u = t;
  #
  # Update system
  #
  state_i = zeros(4, 1);

  # next time step
t = t + dt;
state_i(1) = t;

  % Walk system forward and make sensor observation
  x = A * x + B * u + W(t);
z = C * x + V(t);
state_i(2) = x(2);
state_i(3) = z(1);

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

  state_i(4) = x_hat(2);
  State = cat(2, State, state_i);
  
until (t > t_end)
 

plot(State(1, :), State(2, :), "k", State(1, :), State(3, :) , "b", State(1, :), State(4, :), "r");

