# Fourier series approximation of a binary signal (square wave)
This is an extra-credit assignment done as part of my Computer Networks course. This code uses numpy and matplotlib. To run, simply run  
```pip install numpy matplotlib```  
and then run the code with ```python main.py```. This was tested on and definitely works with python 3.10.10.

This code converts a binary string (like ```"101011110"```) into a function (with time period 1, amplitude 1 by default) ```f(x)``` that returns a square wave with ```x``` being the time parameter.  

It then calculates the Riemann integral of the function, and then uses it to calculate the coefficients a<sub>0</sub>, a<sub>1</sub>, a<sub>2</sub>, a<sub>3</sub>... a<sub>n</sub> and b<sub>1</sub>, b<sub>2</sub>, b<sub>3</sub>... b<sub>n</sub> for the 'offset', and sin(n\*x/L) and cos(n\*x/L) upto a specifiable n.

The focus here wasn't to write good code, but to understand some of the math that goes into understanding the Fourier series coefficients to represent an aperiodic square wave signal as a sum of sine and cosine waves.  

The comments in the code have additional information on how this approximation can be much improved using techniques other than using the Fourier series coefficients alone.