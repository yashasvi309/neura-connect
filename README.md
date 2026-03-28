🧠 Neura Connect

Neurological Event Detection & Intelligent Audio-Feedback Engine

Neura Connect is a logic-heavy, end-to-end pipeline designed for patients with neurological conditions (such as epilepsy or severe tremors). It transforms raw hardware sensor telemetry from a smartwatch or phone into structured, actionable insights and real-time audio feedback. By fusing live mobile sensor data, real-time web context, and a multi-step AI reasoning loop, it eliminates the noise of everyday movements and outputs definitive, life-saving decisions.

🛑 No generic chat outputs. No static hardcoded rules. Just dynamic patient data driving intelligent, multi-step reasoning and immediate audio intervention.

🎯 1. The Problem & Our Solution (Clarity)

The Problem: Patients with neurological issues (e.g., prone to seizures) experience sudden events that require immediate, context-aware intervention. Traditional wearables either rely on rigid, hardcoded movement thresholds (triggering false alarms when a user is simply running) or lack the intelligence to provide immediate, actionable guidance to the patient or bystanders.

The Solution:
Neura Connect bridges local wearable hardware (via the Phyphox app on a phone or smartwatch) with an advanced AI reasoning engine. We ingest live sensor streams, enrich them with real-time web data via Bright Data, process them through a Tiny Recursive Model (TRM) and Featherless AI, and finally output instant audio feedback (e.g., calming instructions, medical alerts, or bystander guidance).

Why it matters: We convert meaningless accelerometer/gyroscope graphs into context-aware interventions (e.g., differentiating a bumpy car ride from a grand mal seizure, and automatically playing an audio prompt to guide bystanders).

🧩 2. Multi-Step Intelligence & Reasoning (How It Thinks)

This is not a simple UI wrapper or a one-shot chatbot. Our longitudinal_agent.py executes a structured, multi-step processing loop:

Ingestion: phyphox_bridge.py captures raw, high-frequency telemetry (accelerometer, gyroscope) from the patient's smartwatch or phone.

Contextualization: Triggered by anomalous movement patterns, cloud_logic.py uses Bright Data to scrape real-time external context (e.g., local weather/heat stressors, nearby hospital availability, or medical baseline data).

Recursive Analysis: The TRM (Tiny Recursive Model) performs iterative reasoning over the data. Instead of guessing immediately, it loops its thought process to identify hidden longitudinal trends (e.g., "Is this rhythmic shaking consistent with a seizure, or is the user just jogging?").

Final Transformation & Audio Generation: We route the synthesized context to highly specialized open-source models via Featherless AI's serverless endpoints. The AI generates a structured decision matrix and dynamically synthesizes an emergency audio script that is immediately played through the device speaker.

📊 3. Dynamic Inputs & Meaningful Data (What Feeds It)

The output is 100% determined by live, dynamic variables. We utilize two main data streams:

Hardware Inputs (Internal): Live accelerometer and gyroscope data streamed directly from the patient's smartwatch or phone.

Web Inputs (External): Dynamic environmental and contextual data pulled via Bright Data proxies to assess risk factors (e.g., high heat index increasing seizure probability).

If the input changes, the reasoning adapts. A sudden rhythmic shaking means something very different if Bright Data reports a local earthquake versus a clear day with a patient who has a history of epilepsy.

🛠️ 4. Quality of Output (Actionable Results)

We explicitly avoid "paragraph dumps." The system is designed to produce life-saving transformations and direct audio interventions.

When a data cycle detects an anomaly, the system outputs actionable JSON payloads containing:

State Assessment: (e.g., Normal, Elevated Tremor Risk, Active Seizure Detected)

Reasoning Trace: A brief, logical explanation of why the decision was made based on TRM's recursive loops.

Actionable Audio Directive: The generation of a real-time audio payload (e.g., "Seizure detected. Please clear the area around the patient and do not hold them down. Emergency contacts have been notified.")

🚀 5. Execution & Demo Guide (End-to-End Flow)

Our demo is designed to be understood in under a minute, proving full end-to-end functionality for neurological care.

Demo Flow:

We start the simulator.py (or connect live via a phone/watch app) to stream physical movement data.

The UI displays the raw, stable data stream (The "Before").

We introduce a physical anomaly simulating a seizure (e.g., rapid, rhythmic XYZ-axis shaking).

You will see the backend instantly query Bright Data for context, pass the data to Featherless AI and the TRM agent.

The Climax: The system outputs a structured alert on-screen and immediately plays the generated audio feedback through the speakers to assist the patient.

⚙️ Quick Start Installation

# 1. Clone the repo
git clone [https://github.com/yashasvi309/neura-connect.git](https://github.com/yashasvi309/neura-connect.git)
cd neura-connect

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Environment Variables (.env)
FEATHERLESS_API_KEY=your_key
BRIGHT_DATA_CREDENTIALS=your_proxy_url

# 4. Launch the Engine
python launch.py


📂 Repository Structure

longitudinal_agent.py - Core TRM reasoning logic and multi-step pipeline for seizure/tremor detection.

cloud_logic.py - Bright Data web scraping and Featherless AI routing.

phyphox_bridge.py - Live hardware sensor ingestion from smartwatch/phone.

simulator.py - Local data generation for seamless demo execution.

app.py / launch.py - System entry points and audio-feedback triggers.

/frontend - Clean, logic-focused UI for visualizing the reasoning process and audio status.
