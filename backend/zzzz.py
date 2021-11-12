import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

ramp = lambda u: np.maximum( u, 0 )
step = lambda u: ( u > 0 ).astype(float)


# =============================================================================
# # x from 0 to 30
# x = 30 * np.random.random((20, 1))
#
# # y = a*x + b with noise
# y = 0.5 * x + 1.0 + np.random.normal(size=x.shape)
# =============================================================================


x = np.linspace( 0, 10, 27 )
#Y = 0.2*X  - 0.3* ramp(X-2) + 0.3*ramp(X-6) + 0.05*np.random.randn(len(X))
y =  0.3* ramp(x-2)+ 0.5*np.random.randn(len(x))
# =============================================================================

x1=x[-6:]
y1=y[-6:]
print(x)
print("---------------------------------------")
print(x1)
print("---------------------------------------")
print(y)
print("---------------------------------------")
print(y1)

#plt.plot( x, y, 'ok' );
x1 = x1.reshape((-1, 1))
# create a linear regression model
model = LinearRegression()
model.fit(x1, y1)

# predict y from the data
x_new = np.linspace(0, 15, 30)
y_new = model.predict(x[:, np.newaxis])

# plot the results
plt.figure(figsize=(4, 3))
ax = plt.axes()
ax.scatter(x, y)
ax.plot(x, y_new)

ax.set_xlabel('x')
ax.set_ylabel('y')

ax.axis('tight')


plt.show()