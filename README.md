🛸 Swarm Rescue: Collective Search and Rescue Simulation

This project is a collective search and rescue simulation operating entirely on local rules and Swarm Intelligence principles, without a centralized control unit. Developed as part of a university Robotics course, the simulation models autonomous agents navigating complex debris environments (mazes) to locate trapped targets and dynamically redirect the swarm to the discovery site via emergent behavior.

🚀 Key Features<br>
Decentralized Decision Making: Robots do not rely on a global network. They interact exclusively with neighbors within their local perception radius.<br>
Advanced Boids Algorithm: Beyond classic flocking, the agents are equipped with "Obstacle Avoidance" and "Goal Seeking" steering behaviors.<br>
Anti-Tunneling (Physics Protection): Implements an exponential repulsion force algorithm based on distance to prevent high-speed agents from phasing through solid walls (ghosting/tunneling).<br>
Dynamic HUD & Info Panel: Real-time projection of target status, swarm metrics, and specific coordinate data onto the simulation canvas.<br>
Data Analysis & Logging: Every simulation tick is recorded into a CSV format to analyze convergence rates and generate performance graphs.

🧠 Algorithm Details<br>
The simulation architecture is heavily inspired by Craig Reynolds' Boids artificial life program. In each frame, every agent calculates its steering velocity based on the weighted sum of 5 primary vectors:<br>

Separation: Short-range repulsion to avoid crowding and collisions with local flockmates.<br>
Alignment: Steering towards the average heading of local flockmates.<br>
Cohesion: Steering to move toward the average position (center of mass) of local flockmates.<br>
Obstacle Avoidance: Detecting environmental boundaries (debris) and applying aggressive counter-forces to navigate mazes.<br>
Goal Seeking: A strong attraction vector triggered across the swarm when any single agent detects the rescue target.<br>

https://github.com/user-attachments/assets/211e753d-bc60-4695-9135-19414f9954a9

🛠️ Tech Stack<br>
Core Language: Python 3.10+<br>
Vector Mathematics: NumPy<br>
Simulation Renderer: OpenCV (2D Matrix Canvas)<br>
Data Logging & Plotting: Pandas & Matplotlib

⚙️ Installation & Execution<br>
Clone the repository:
Bash
git clone https://github.com/eminyazar/swarm-rescue.git
cd swarm-rescue

Install dependencies:
Bash
pip install -r requirements.txt

Run the simulation:
Bash
python main.py
(Press 'q' while on the screen to terminate the simulation and save the data log)

Generate the analysis graph:
Bash
python plot_results.py

📊 Performance Analysis
System success is measured by the Convergence metric—the average distance of the swarm to the target over time. Tests indicate that applying emergent swarm intelligence significantly optimizes search duration and area coverage compared to isolated individual agents.
(As the target's position changes each time, the graph will also change.)

<img width="2558" height="1653" alt="convergence_graph" src="https://github.com/user-attachments/assets/907f2909-2123-41bc-adf3-9215e09a5c39" />

📝 License
This project was developed for academic and educational purposes. Distributed under the MIT License.

Developed by: M.Emin Yazar - Senior Computer Engineering Student
