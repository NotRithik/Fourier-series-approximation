import matplotlib.pyplot as plt
import numpy as np

'''
This code calculates the Fourier constants for a function f(x) and then reconstructs it.
It graphs the original function, the reconstructed function with sine waves,
and also graphs what the receiver would interpret the signal as.

This is meant to be used for a binary, square wave signal that will be reconstructed
at the other end also as a binary square wave, with the threshold being 0. If signal > 0, then 1. If signal <= 0, then 0.

The function binary_to_wave() takes in a binary string and returns a function f that constructs the square wave
of the signal at the given point in time. The time period (and thus frequency) can be modified
in the binary_to_wave() function. The amplitude can also be modified.

The function fourier_constants() takes in n, the number of constants to calculate,
the function f(x) and the range L to calculate the fourier constants over.

It uses the formula for calculating the fourier constants:
a_0 = 1/2L * integral of f(x)dx over -L to L.
a_i = 1/L * integral of f(x)*cos(ix*Pi/L)dx over -L to L.
b_i = 1/L * integral of f(x)*sin(ix*Pi/L)dx over -L to L.

This code uses Riemann integration in all places to find the integral of the function.

This is best used for approximating a periodic function (as shown in class for a periodic square wave),
but can also be used for an aperiodic function.

Since we are using this for an aperiodic function, we pad the end of the signal with zeroes.
This allows for some buffer area at the end of the signal, for the approximation to be 'smeared' over and ignored.
If the protocol is such that the receiver only looks at the first few x of the signal, or the transmitter
ends transmission of the sine waves after a certain number of x before the padding, then this can be used for
effective transmission of the signal.

With a smaller padding, or longer binary string being approximated, the approximation gets more and more obfuscated
towards the end of the signal.

The fourier series is best used for approximating a periodic signal, and would have a fundamental frequency
and harmonics of the fundamental frequency being used to approximate the signal using constants, for
representing the signal as a sum of sine waves and cosine waves.

For a better approximation of the signal, the fourier transform would be a better choice as this 
is more general and good for periodic as well as aperiodic signals to be represented in the frequency domain
instead of the time domain. It also would not require messing around with padding the signal with zeroes.
The fourier transform would lose information in the time domain, though.

A wavelet transform would also be a good choice as it would preserve information in the frequency domain
and information in the time domain as well. It would be calculated by sliding the wavelet over the signal
in different time windows, and convolving the signal with the wavelet to see how similar the signals are
at each point in time, kind of like a dot product.

'''


def binary_to_wave(binary_str, period=1, amplitude=1):
    values = [amplitude if bit == '1' else -amplitude for bit in binary_str]
    
    def square_wave(x):
        x = x % (len(values) * period)
        idx = int(x // period)
        return values[idx]
    
    return square_wave


def fourier_constants(n, f, L):
    a_consts = []
    b_consts = []

    # To find a_0, integrate f(x)dx from -L to L
    sum = 0
    prev_x = 0
    for x in np.linspace(-L, L, L*100):
        dx = x - prev_x
        sum += f(x) * dx
        prev_x = x

    # a_0 = 1/2L * integral of f(x)dx from start to end
    a_0 = 1/(2*L) * sum

    for i in range (1, n+1):
        # Integrate the function f(x)*cos(ix*Pi/L)dx from start to end
        sum = 0
        prev_x = 0
        for x in np.linspace(-L, L, L*100):
            dx = x - prev_x
            sum += f(x) * np.cos(i * np.pi * x / L) * dx
            prev_x = x

        integral_cos = sum
        a_i = (1/L) * integral_cos
        a_consts.append(a_i)

        # Integrate the function f(x)*sin(ix*Pi/L)dx from start to end
        sum = 0
        prev_x = 0
        for x in np.linspace(-L, L, L*100):
            dx = x - prev_x
            sum += f(x) * np.sin(i * np.pi * x / L) * dx
            prev_x = x

        integral_sin = sum
        b_i = (1/L) * integral_sin
        b_consts.append(b_i)

    return (a_0, a_consts, b_consts)


# The binary string to be approximated
binary_str = "100101000111011100011110"
padding = 100
# Since we are approximating an aperiodic function, and the Fourier series 
# is best for periodic functions, the edges of the aperiodic function might not be very crisply approximated.
# Thus when we pad the end of the signal with zeroes, it adds a buffer towards the end of the signal which can get 'smeared'
# over and we can ignore it.
# The start of the approximated function thus remains accurate at the cost of the part towards the end of the approximation.
str_padding = str("0" * padding)
binary_str = binary_str + str_padding
f = binary_to_wave(binary_str, period=1, amplitude=10)

# Plotting the square wave function
x = np.linspace(0, len(binary_str)-padding, 10000)
y = [f(xi) for xi in x]

(a0, a, b) = fourier_constants(200, f, len(binary_str))
print("a_0 =", a0)
print("a =", a)
print("b =", b)

def g(x):
    # This is the reconstruction of a signal from the fourier constants
    sum = a0
    for (i, a_i) in enumerate(a):
        sum += a_i * np.cos(i*x*np.pi/(len(binary_str)))
    for (i, b_i) in enumerate(b):
        sum += b_i * np.sin(i*x*np.pi/(len(binary_str)))
    return sum

z = [g(xi) for xi in x]

reconstruction = [20 if zi > 0 else -20 for zi in z]

plt.plot(x, y, label='f(x) (original binary square wave signal to be transmitted)', color='blue')
plt.plot(x, z, label='g(x) (sine wave approximation of original signal)', color='yellow')
plt.plot(x, reconstruction, label='reconstructed(x) (shown with higher amplitude for ease of viewing)', color='red', linestyle='dashed')
plt.xlabel('x')
plt.ylabel('y, z, r')
plt.title('Square Wave Function and Fourier Estimation')
plt.grid(True)
plt.legend()
plt.show()