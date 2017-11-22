Introduction
============

The purpose of this project is to visualise the Clarke Transform and the Park Transform.

Three-Phase Inputs
----------------------------------------
.. math::
	\omega = 2 \pi f

.. math::
	\left[\begin{matrix} a \\ b \\ c \end{matrix}\right] = \left[\begin{matrix} \cos(n \cdot \omega t) \\ \cos[n \cdot (\omega t - \frac{2}{3} \pi)] \\ \cos[n \cdot (\omega t + \frac{2}{3} \pi)] \end{matrix}\right]

.. math::
	where, n >= 0


Clarke Transform (amplitude invariant)
----------------------------------------
.. math::
	\left[\begin{matrix} \alpha \\ \beta \\ Zero \end{matrix}\right] = \frac{2}{3} \left[\begin{matrix} 1 & -\frac{1}{2} & -\frac{1}{2} \\ 0 & \frac{\sqrt{3}}{2} & -\frac{\sqrt{3}}{2} \\ \frac{1}{2} & \frac{1}{2} & \frac{1}{2} \end{matrix}\right] \left[\begin{matrix} a \\ b \\ c \end{matrix}\right]

Park Transform
----------------------------------------
.. math::
	\left[\begin{matrix} d \\ q \\ Zero \end{matrix}\right] = \left[\begin{matrix} \cos\theta & \sin\theta & 0 \\ -\sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{matrix}\right] \left[\begin{matrix} \alpha \\ \beta \\ Zero \end{matrix}\right]
	
	
.. figure:: images/Visualisation_of_Clarke_and_Park_Transforms.svg
   :height: 450
   :width: 800
   
|  **UI apperance.**
|
|  **Input Harmonic Oder :**
|    The order of harmonic to be analysed. Should be a positive number (unsigned float)		
|
|  **Input PLL Oder :**
|    The order of the PLL. Positive number means anti-clockwise rotation. Negative number means clockwise rotation. The value of the number means how many times the base frequency the PLL frequency is. Should be a real number (signed float).
|
|  **Samples :** 
|	 The number of samples to be taken within one base period. Should be unsigned int.
|
|  **FPS :**
|	 Only applied when saving video. NOT applied in real time. Should be unsigned int.
|
|  **Base Freq :**
|	 Base frequency of the system, i.e., 50 or 60. This can be any non-zero positive number (unsigned float, non-zero).
|
|  **FFmpeg path :**
|	 Path of the FFmpeg binary (string).

.. note::
   Zero Sequences are not plotted since their :math:`\alpha, \beta, d` and :math:`q` components are zero. Also, they need 3D coordinates.