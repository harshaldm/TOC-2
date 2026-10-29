# ProtoGuard NIDS: Web Dashboards Quick Reference Guide

> A concise guide to the 4 interactive dashboards on the ProtoGuard NIDS platform.

---

## Navigation Overview

The web application features a top navigation bar with **4 core views**:

| Tab Name | Purpose | Primary Target Audience |
| :--- | :--- | :--- |
| **1. Live FSM & Simulation** | Interactive visual simulator for normal & attack traffic | Live demos, presentations, attack observation |
| **2. 3-Way Benchmarking** | Empirical performance comparisons (FSM vs. ML vs. Hybrid) | Academic evaluation, metrics, defense slides |
| **3. Custom Sequence Tester** | Interactive sequence builder & "what-if" testing playground | Manual packet testing, edge-case evaluation |
| **4. TOC Automata Specs** | Formal Theory of Computation definitions & proofs | Theory verification, viva/defense questions |

---

## 1. Live FSM & Simulation Dashboard

The **command center** of ProtoGuard. It simulates real-world network traffic packet-by-packet with real-time state visualization.

### Key Visual Components:
1. **Simulation Control Bar (Top)**:
   - **Scenario Dropdown**: Select between 7 pre-configured scenarios (Benign, Out-of-Order ACK, Premature Data, Stealth FIN, SYN Flood, Slowloris, Zero-Day).
   - **Playback Controls**: Start, Pause, Reset, and a **Speed Slider (0.5x to 4x)**.
2. **Interactive SVG State Machine (Left Upper)**:
   - Visualizes all **11 protocol states** as interconnected nodes.
   - The active state glows in cyan. As packets arrive, directed arrows pulse with green (legal) or red (illegal) animations.
   - On an attack, the machine transitions into a glowing red **`ERROR_STATE`**.
3. **3-Way Detector Scorecard (Left Lower)**:
   - Three side-by-side cards comparing:
     - **Rule-Based FSM**: Microsecond latency ($0.06\text{ ms}$), 100% confidence on syntax.
     - **Pure ML (RF + IF)**: High recall, catches statistical/temporal anomalies.
     - **Hybrid Engine**: Fused decision showing final verdict, confidence, and which stage triggered.
4. **Offending Alert Drawer (Right Upper)**:
   - Appears immediately upon detecting an intrusion.
   - Highlights the exact illegal transition (e.g., `CLOSED --(ACK)--> ERROR_STATE`), legal expected symbols, attack explanation, and mapped **CVE/CWE/MITRE** IDs.
5. **Live Packet Stream Table (Right Lower)**:
   - A real-time scrolling table showing incoming packet metadata: Packet #, Timestamp, Protocol Flags, Payload Size, Inter-arrival Time ($\Delta t$), and status badge.

---

## 2. 3-Way Benchmarking Dashboard

Displays **empirical scientific results** across 300 test sessions (2,184 packets) and novel zero-day attack sequences.

### Key Visual Components:
1. **Four Primary Comparison Cards**:
   - **Detection Rate (Recall)**: FSM ($36.1\%$) vs. Pure ML ($100\%$) vs. Hybrid ($100\%$).
   - **False Alarm Rate (FPR)**: FSM ($0.0\%$) vs. Pure ML ($3.5\%$) vs. Hybrid ($3.5\%$).
   - **Classification Accuracy**: FSM ($77.6\%$) vs. Pure ML ($97.7\%$) vs. Hybrid ($97.7\%$).
   - **Average Processing Latency**: FSM ($0.06\text{ ms}$) vs. Pure ML ($44.8\text{ ms}$) vs. Hybrid ($44.9\text{ ms}$).
2. **Zero-Day Generalization Panel**:
   - Evaluates performance on novel, unseen attack sequences (e.g., Handshake Skip to Teardown).
   - Shows how the **unsupervised Isolation Forest** achieves **100% recall** without prior labels.
3. **Top-6 Feature Importances Bar Chart**:
   - Ranks the most decisive features in the 27-D extractor (e.g., `fsm_violation_count`, `markov_log_likelihood`, `mean_delta_t`, `event_entropy`).

---

## 3. Custom Sequence Tester Dashboard

An interactive **sandbox playground** where users can build arbitrary packet sequences and test how the detection engines react.

### Key Visual Components:
1. **Interactive Token Builder**:
   - Clickable buttons for each alphabet symbol: `SYN`, `SYN_ACK`, `ACK`, `DATA`, `FIN`, `RST`, `TIMEOUT`.
   - Add or remove tokens to craft custom sequences (e.g., `[SYN, ACK, DATA]`).
2. **Traffic Parameter Controls**:
   - **Inter-Arrival Time ($\Delta t$) Slider**: Set timing from $0.0005\text{s}$ (burst flood) to $35.0\text{s}$ (Slowloris stall).
   - **Payload Size Input**: Test 0-byte header probes vs. large data transfers.
3. **One-Click Attack Presets**:
   - Instant buttons to load known patterns: Standard Flow, Blind ACK, Premature Payload, Stealth FIN, SYN Flood, and Slowloris.
4. **Live Verdict Output**:
   - Evaluates the sequence against the backend and shows the FSM step-by-step path, ML anomaly probability, and hybrid verdict breakdown.

---

## 4. TOC Automata Specs Dashboard

The **academic reference view** presenting the formal Theory of Computation foundations of the project.

### Key Visual Components:
1. **Formal 5-Tuple Cards**:
   - **$Q$ (States)**: The 11 formal states (`CLOSED` through `ERROR_STATE`).
   - **$\Sigma$ (Alphabet)**: The 8 discrete input event tokens.
   - **$q_0$ (Initial State)**: `CLOSED`.
   - **$F$ (Accepting States)**: `CLOSED` and `TIME_WAIT`.
2. **Right-Linear Regular Grammar ($G$)**:
   - Formulates the normal protocol as a Type-3 regular language $L(M)$.
   - Displays production rules ($S \to \text{SYN } A$, $A \to \text{SYN\_ACK } B$, etc.).
3. **Complement Anomaly Language Proof**:
   - Displays the set-theoretic definition: $L_{\text{anomaly}} = \Sigma^* \setminus L(M)$.
   - Explains how undefined transitions trap into `ERROR_STATE`.
4. **Transition Matrix**:
   - Complete tabular representation of the delta function $\delta(s, \sigma)$.

---

## Quick Summary for Project Defense

* **Tab 1 (Live FSM)** proves the **execution speed and visual interpretability** of automata.
* **Tab 2 (Benchmarks)** proves the **mathematical necessity of the hybrid model** (FSM eliminates false positives; ML eliminates blind spots).
* **Tab 3 (Custom Tester)** proves the system's **robustness on arbitrary edge cases**.
* **Tab 4 (TOC Specs)** grounds the implementation in **formal computer science theory**.

