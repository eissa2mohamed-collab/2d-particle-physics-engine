# 2D Particle Physics Engine

A lightweight, 2D impulse-based particle physics simulation built in Python using Pygame. This project demonstrates real-time vector integration, boundary restitution, positional separation, and sub-stepping collision resolution for multi-body interactions.

## Key Features

- **Impulse-Based Collision Resolution:** Uses vector math and 2D dot-product projections to calculate accurate momentum transfer during elastic and inelastic particle impacts.
- **Sub-Stepping Physics Solver:** Multi-pass solver (8 passes per frame) prevents particle overlap, tunneling, and pile instability.
- **Positional Separation:** Pushes intersecting geometry apart prior to velocity resolution, eliminating infinite sticking loops.
- **Air Drag & Ground Friction:** Simulates drag and surface friction to dampen kinetic energy over time for realistic motion decay.
- **Micro-Jitter Mitigation:** Low-velocity threshold clamping prevents numerical instability and shaking when particles settle on flat surfaces.
- **Boundary Clamping:** Edge-collision handling against configurable screen constraints (`SCREEN_WIDTH`, `SCREEN_HEIGHT`) with energy coefficient loss.

## Math & Physics Overview

The engine resolves 2D collisions using the following sequence per frame:

1. **Integration:** Position is updated via velocity vectors ($\vec{p}_{\text{new}} = \vec{p} + \vec{v}$), and vertical velocity is adjusted for gravity ($\vec{v}_y \mathrel{+}= g$).
2. **Overlap Resolution:** Distance between particle centers $d = \|\vec{p}_2 - \vec{p}_1\|$ is checked against combined radii $r_1 + r_2$. Overlapping pairs are separated along the collision normal $\hat{n}$:
   $$\vec{p}_{\text{separation}} = \hat{n} \cdot \frac{(r_1 + r_2) - d}{2}$$
3. **Impulse Calculation:** Scalar impulse $j$ along collision normal $\hat{n}$:
   $$j = \frac{-(1 + e) \cdot (\vec{v}_{\text{rel}} \cdot \hat{n})}{2}$$
   where $e$ is the coefficient of restitution (bounciness) and $\vec{v}_{\text{rel}}$ is relative velocity ($\vec{v}_2 - \vec{v}_1$).

## Prerequisites

- **Python 3.8+**
- **Pygame**

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/eissa2mohamed-collab/2d-particle-physics-engine.git](https://github.com/eissa2mohamed-collab/2d-particle-physics-engine.git)
   cd 2d-particle-physics-engine
2. Install dependencies:
   ```bash
   pip install pygame
3. Run the simulation:
   ```bash
   python main.py
4. Controls:
   - Left Mouse Click: Spawn a particle at cursor position.
5. License:
   Distributed under the MIT License.