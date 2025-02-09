# 🧠 AI Assistant for Low-Resource Systems

### **A Lightweight AI Assistant for Raspberry Pi & Windows**

🚀 **Current Status**: Work in progress\
🎯 **Final Goal**: A fully operational AI assistant running efficiently on a **Raspberry Pi**, capable of executing **chat-based and voice commands** to control a **Windows** computer.

---

## 🔥 **Project Overview**

This project aims to build an **AI assistant optimized for low-resource environments**, specifically designed to run on a **Raspberry Pi** while interacting with a Windows machine. The assistant will support:

✅ **Voice Commands** – Execute system actions (adjust brightness, control volume, open applications, etc.).\
✅ **Chat-based Interaction** – Understand and process text-based queries (currently using CamemBERT Base for intent recognition).\
✅ **System Control** – Perform tasks such as file searches, microphone activation, and power management.\
✅ **Efficient Performance** – Utilize minimal computational resources to ensure smooth operation on lightweight hardware.

The **Raspberry Pi** acts as the brain, processing user inputs and sending commands to the Windows machine via a **USB connection**. This setup ensures a seamless **offline** experience without relying on cloud-based AI models. Security concerns will be thoroughly examined to protect user data.

---

## 📌 **Motivation**

As an AI enthusiast passionate about **efficiency and edge computing**, I wanted to challenge myself by designing an assistant that:

- **Runs on constrained hardware** (like a Raspberry Pi).
- **Operates without internet dependency**, ensuring privacy and security (I am currently working on updating the speech recognition to function offline).
- **Provides real-time control** over a Windows environment using voice or text.
- Bridges **embedded systems and AI**, demonstrating practical AI integration into everyday computing.
- Uses **Python** for its extensive library support, modularity, and ease of integration with AI and system control functionalities, making it a versatile choice over C.

---

## 📍 **Current Progress**

### ✅ **Implemented Features**

🔹 **Core system architecture** – Handling context management, user input recognition, and Windows control features.\
🔹 **Basic NLP processing** – Implemented an intent recognition model to understand user commands.\


### 🔄 **Work in Progress**

🛠 **Speech Recognition** – Implementing an efficient offline voice-to-text system.\
🛠 **USB Communication** – Enabling seamless command transmission between the Raspberry Pi and Windows.\
🛠 **AI-powered Context Management** – Enhancing the assistant’s ability to remember user preferences and maintain conversation history.\
🛠 **Module triggering** – Ensuring a smooth link between user input and the correct system functions.

---

## 🚀 **Next Steps**

🔜 **Voice Control Implementation** – Integrating an **on-device** voice recognition model for offline usage.\
🔜 **Better NLP Processing** – Improving the assistant’s ability to handle complex queries and extract more meaningful intents.\
🔜 **Optimization for Raspberry Pi** – Reducing computational overhead for smoother performance.\
🔜 **GUI for Windows** – Adding a simple **chat interface** to interact with the assistant.\
🔜 **Advanced Understanding** – Enhancing the model’s ability to better interpret user commands.\
🔜 **Machine Learning Integration** – Implementing feedback-based learning to improve responses over time.

---

## 🔧 **Tech Stack**

💻 **Languages**: Python\
🛠 **Libraries**: `torch` (for AI processing), `speechrecognition` (for voice input), `pyaudio` (for audio handling), `subprocess` (for system commands), and more.\
📡 **Communication**: USB serial connection between Raspberry Pi & Windows\
🔊 **Speech Processing**: Offline models (planned)\
💻 **Development Environment**: Currently developed on a Virtual Machine running Linux, with plans to implement the bridge with Windows in a later phase.

---

## 📜 **How to Run** (Planned)

1. Clone the repository:
   ```bash
   git clone https://github.com/WhassuppussahW/ai-assistant.git
   cd ai-assistant
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the assistant:
   ```bash
   python main.py
   ```

More detailed setup instructions will be provided as the project progresses.

