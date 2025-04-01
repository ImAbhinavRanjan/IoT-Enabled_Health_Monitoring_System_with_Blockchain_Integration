# IoT-Enabled Health Monitoring System with Blockchain Integration

## 📌 Project Overview
This project is an **IoT-based health monitoring system** that collects real-time pulse rate and blood oxygen levels using an **ESP32 microcontroller** and **MAX30100 sensor**. The data is displayed on a **Django-powered web application** and stored securely on a **Ganache blockchain** for integrity and privacy. Patients can log in to view their health data in graphical format.

## 🔥 Features
- **Real-time Health Monitoring**: Captures pulse rate (BPM) and blood oxygen level (SpO2) using MAX30100.
- **Web-Based Dashboard**: Displays real-time data and historical trends.
- **Blockchain Integration**: Uses Ganache to store health data securely.
- **ESP32 as IoT Device**: Connects wirelessly and streams data via Wi-Fi.
- **Secure Authentication**: Patients can log in to access their data.
- **Data Visualization**: Interactive graphs for better analysis.

## 🛠️ Tech Stack
### **Hardware Components:**
- **ESP32** (Microcontroller for IoT communication)
- **MAX30100** (Pulse and SpO2 sensor)

### **Software & Tools:**
- **Arduino IDE** (For ESP32 programming)
- **Django** (Python framework for backend development)
- **HTML, CSS, JavaScript, Bootstrap** (Frontend UI)
- **WebSockets** (For real-time data updates)
- **Ganache** (Blockchain for secure data storage)
- **Remix IDE & MetaMask** (For smart contract deployment)

## ⚙️ System Architecture
1. **ESP32 reads sensor data** from MAX30100.
2. **Data is sent over Wi-Fi** to the Django backend.
3. **Django processes & displays the data** on the web dashboard.
4. **Data is stored on the blockchain** via Ganache for security.
5. **Users authenticate and access** their health records securely.

## 🛠️ Installation & Setup
### **1. Setting Up ESP32**
- Install **Arduino IDE** and ESP32 board support.
- Install necessary libraries (`WiFi`, `WebServer`, `MAX30100_PulseOximeter`).
- Flash the ESP32 with the provided **Arduino sketch**.

### **2. Blockchain Integration**
- Install **Ganache** and **MetaMask**.
- Deploy smart contracts using **Remix IDE**.
- Connect MetaMask to the local blockchain.

## 👨‍💻 Author
Developed by **Abhinav Ranjan** 🚀

