# KARIGAR AI - Base Agent & Sovereign Approval Gate Manager
# "AI Recommends. Artisans Decide."

from enum import Enum
import datetime

class ApprovalGate(Enum):
    GATE_1_CATALOGUE = "GATE_1_CATALOGUE" # Listing and craft story verification
    GATE_2_PRICING   = "GATE_2_PRICING"   # Cost floor and approved listing price
    GATE_3_DEAL      = "GATE_3_DEAL"      # Commercial negotiation and buyer agreements

class GateViolationException(Exception):
    """Raised whenever an autonomous process attempts to finalize a commercial commitment without explicit artisan approval."""
    pass

class BaseAgent:
    def __init__(self, name: str, gate: ApprovalGate):
        self.name = name
        self.gate = gate

    def log_gate_event(self, conn, artisan_id: int, entity_id: int, action: str, details: str):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO approval_logs (artisan_id, gate_name, entity_id, action, details)
            VALUES (?, ?, ?, ?, ?)
            """,
            (artisan_id, self.gate.value, entity_id, action, details)
        )
        conn.commit()
