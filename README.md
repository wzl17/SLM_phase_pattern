# SLM Phase Pattern generator

Implementation of Gerchberg-Saxton algorithm for generating a SLM phase pattern from a target intensity image.
The code is meant for a Hamamatsu LCOS-SLM model X13138-5

The various files have the following purposes:
* GS.py : Gerchberg–Saxton algorithm. Generates a phase hologram in a range [0,255] corresponding to a [0,2pi] phase. In the SLM plane the assumption is that a the incident amplitude has the shape of a Gaussian beam.

<p align="center">
  <img width="460" height="300" src="https://github.com/mmazzanti/SLM_phase_pattern/blob/master/Presentation_files/SLM_evol_show.gif">
</p>

![Algo_conv](https://github.com/mmazzanti/SLM_phase_pattern/blob/master/Presentation_files/SLM_evol_show.gif )

* GSW.py : Weighted Gerchberg–Saxton algorithm. Improvement of the GS algorithm to obtain better hologram uniformity. Based on [1]

* Fresnel_gen.py : Generates a Fresnel lens pattern for the specified focus.

![Frestnel lens](https://github.com/mmazzanti/SLM_phase_pattern/blob/master/Presentation_files/Lens_show.png )


* Blazed_grating_gen.py : Generates a blazed grating pattern for shifting the hologram from the zero order spot.

![blazed_grating](https://github.com/mmazzanti/SLM_phase_pattern/blob/master/Presentation_files/Grating_show.png )


[1]Roberto Di Leonardo, Francesca Ianni, and Giancarlo Ruocco, *"Computer generation of optimal holograms for optical trap arrays,"* Opt. Express 15, 1913-1922 (2007)
