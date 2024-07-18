# RL Traffic Lights Control

**Bachelor's Thesis by Sergio Vittorio Zambelli - ID: 861172**

---

## Introduction

Traffic control is a critical issue in modern cities, where heavy congestion is a common occurrence and difficult to manage. The main challenge lies in regulating traffic at networked intersections using traffic lights to facilitate a smoother flow of vehicles.

---

## Project Overview

This thesis addresses the problem of traffic control using traffic light agents with Deep Reinforcement Learning (DRL) techniques. By combining the power of neural networks with the efficacy of Reinforcement Learning (RL), this approach is compared with the classical cyclic agent approach, where agents are programmed to alternate traffic flows in each direction at fixed and regular time intervals, making them less responsive to traffic variations.

### Key Challenges

- **Creating Intelligent Agents**: Developing smart agents capable of converging to optimal behaviors in the shortest possible time.
- **Simulation and Implementation**: Using the SUMO library for environment simulation and Stable Baselines 3 for implementing RL algorithms.
- **Training Techniques**: Structuring two types of agent training:
  - **Classical Training**
  - **Curriculum Learning**: A technique aimed at reducing training time.

### Training Outcomes

- Agents trained with a curriculum-based process converge to optimal behavior significantly faster than those trained using classical methods.
- Both models, despite different training techniques, demonstrated the same capability to minimize traffic flow, validating Curriculum Learning as an effective method for reducing resource usage during training.

### Performance Comparison

A comparison between the intelligent agent and the fixed-cycle agent revealed significant performance differences based on traffic conditions:
- **High Traffic**: The fixed-cycle agent performed better, effectively managing large volumes of vehicles and maintaining smoother traffic flow.
- **Low to Moderate Traffic**: The fixed-cycle agent showed inferior performance compared to the intelligent agent, highlighting the different strengths of the two approaches.

---

## Conclusion

The study confirms the potential of DRL techniques in optimizing traffic light control, offering a promising alternative to traditional fixed-cycle approaches, especially in varying traffic conditions. Curriculum Learning emerged as a valuable method to expedite the training process, ensuring efficient use of resources.

---

## Tools and Libraries

- **SUMO**: Simulation of Urban MObility library for environment simulation.
- **Stable Baselines 3**: Library for implementing RL algorithms.

---

Thank you for reading! 🚦🚗