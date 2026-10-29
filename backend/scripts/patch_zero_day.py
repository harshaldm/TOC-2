import sys
from pathlib import Path

gen_file = Path("backend/app/data/synthetic_generator.py")
main_file = Path("backend/app/main.py")

# 1. Patch synthetic_generator.py
with open(gen_file, "r", encoding="utf-8") as f:
    gen_content = f.read()

zero_day_func = '''    def generate_zero_day_bypass(self, session_id: Optional[str] = None) -> List[NetworkPacketEvent]:
        """
        Attack 6: Zero-Day Handshake Skip to Teardown (SYN -> FIN).
        Strict FSM Violation: In SYN_SENT state, an unsolicited FIN packet arrives.
        """
        sid = session_id or f"atk_zd_{uuid.uuid4().hex[:6]}"
        attacker_ip = "10.0.99.99"
        curr_time = time.time()
        delta1 = random.uniform(0.01, 0.03)
        delta2 = random.uniform(0.01, 0.03)
        src_port = random.randint(35000, 60000)

        p1 = NetworkPacketEvent(
            session_id=sid,
            seq_index=0,
            timestamp=curr_time + delta1,
            delta_t=delta1,
            src_ip=attacker_ip,
            dst_ip=self.server_ip,
            src_port=src_port,
            dst_port=self.server_port,
            event_type=EventType.SYN.value,
            current_state=ProtocolState.CLOSED.value,
            next_state=ProtocolState.SYN_SENT.value,
            payload_size=0,
            flags=["SYN"],
            is_anomaly=0,
            attack_category="Normal",
            violation_type="NONE",
        )

        p2 = NetworkPacketEvent(
            session_id=sid,
            seq_index=1,
            timestamp=curr_time + delta1 + delta2,
            delta_t=delta2,
            src_ip=attacker_ip,
            dst_ip=self.server_ip,
            src_port=src_port,
            dst_port=self.server_port,
            event_type=EventType.FIN.value,
            current_state=ProtocolState.SYN_SENT.value,
            next_state=ProtocolState.ERROR_STATE.value,
            payload_size=0,
            flags=["FIN"],
            is_anomaly=1,
            attack_category="ZeroDay_Handshake_Bypass",
            violation_type="UNSEEN_TRANSITION_SEQUENCE",
        )

        return [p1, p2]

'''

if "def generate_zero_day_bypass" not in gen_content:
    target = "    def generate_dataset("
    idx = gen_content.find(target)
    if idx != -1:
        new_gen = gen_content[:idx] + zero_day_func + gen_content[idx:]
        with open(gen_file, "w", encoding="utf-8") as f:
            f.write(new_gen)
        print("[OK] Patched synthetic_generator.py")
    else:
        print("[ERR] Could not find target in synthetic_generator.py")
else:
    print("[SKIP] synthetic_generator.py already has generate_zero_day_bypass")

# 2. Patch backend/app/main.py
with open(main_file, "r", encoding="utf-8") as f:
    main_content = f.read()

# Update REST endpoint
old_rest = '''    elif scenario_id == "zero_day_bypass":
        # Handshake Skip to Teardown: SYN -> FIN
        packets = [
            generator.generate_normal_session()[0],  # SYN
            generator.generate_stealth_fin_scan()[0], # FIN
        ]
        packets[0].session_id = "zd_bypass_01"
        packets[1].session_id = "zd_bypass_01"
        packets[1].seq_index = 1'''

new_rest = '''    elif scenario_id == "zero_day_bypass":
        packets = generator.generate_zero_day_bypass()'''

if old_rest in main_content:
    main_content = main_content.replace(old_rest, new_rest)
    print("[OK] Patched REST endpoint in main.py")

# Update WebSocket handler
old_ws = '''                elif scenario_id == "slowloris":
                    pkts = generator.generate_slowloris_attack()
                else:
                    pkts = generator.generate_normal_session()'''

new_ws = '''                elif scenario_id == "slowloris":
                    pkts = generator.generate_slowloris_attack()
                elif scenario_id == "zero_day_bypass":
                    pkts = generator.generate_zero_day_bypass()
                else:
                    pkts = generator.generate_normal_session()'''

if old_ws in main_content:
    main_content = main_content.replace(old_ws, new_ws)
    print("[OK] Patched WebSocket handler in main.py")

with open(main_file, "w", encoding="utf-8") as f:
    f.write(main_content)

print("[SUCCESS] All patches applied.")

