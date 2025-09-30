# 🌿 VerdantProtocol

**VerdantProtocol** is a modular, scalable, and intelligent environmental monitoring and automation framework designed for grow tents, greenhouses, and beyond. It leverages a swarm of Wi-Fi-enabled sensor nodes to feed real-time data to a central master controller, which orchestrates actuator responses to optimize plant health and resource efficiency.

---

## 🧠 Project Overview

VerdantProtocol is built around the concept of distributed intelligence:

- **Sensor Nodes**: Autonomous Raspberry Pi Pico W modules measuring soil moisture, temperature, humidity, barometric pressure, light, and more.
- **Master Controller**: A Raspberry Pi 5 running an MQTT broker, automation logic, and optional dashboard.
- **Actuator Nodes**: Devices like sprinklers, fans, heaters, and humidifiers that respond to commands from the master controller.

---

## 🧬 Architecture
Sensor Nodes (Pico W) --> MQTT --> Raspberry Pi 5 (Master Controller) --> Actuators

Each node publishes data to MQTT topics. The master controller subscribes to these topics, logs the data, and triggers automation rules based on thresholds or conditions.

---

## 🎯 Goals

- 🌱 Optimize plant health through real-time environmental monitoring
- 🔧 Enable modular, battery-powered sensor nodes
- 📡 Use Wi-Fi and MQTT for lightweight communication
- 🧩 Support scalable deployments from tents to farms
- 📊 Provide optional dashboards and data logging

---

## 📁 Repositories

| Repo | Description |
|------|-------------|
| `verdantprotocol-core` | Master controller logic, MQTT broker setup, automation scripts |
| `verdantprotocol-nodes` | Firmware for Pico W sensor modules |
| `verdantprotocol-actuators` | Scripts and logic for actuator control |

---

## 🚀 Getting Started

1. Flash sensor node firmware to your Pico W devices
2. Set up the Raspberry Pi 5 with MQTT broker and automation logic
3. Connect actuators and define rules
4. Monitor and expand your network as needed

---

## 📜 License

MIT License — open source and ready to grow.

---

## 🤖 Join the Swarm

VerdantProtocol is designed to evolve. Add new sensors, expand your zones, and automate smarter. This is just the beginning.
