from typing import Dict, Any, Optional
from com.fractalcommunication.interfaces import IMetricsLogger
from com.fractalcommunication.state import ConversationState

class SimpleMetricsLogger(IMetricsLogger):
    def __init__(self):
        self.metrics = {}
        self.errors = {}
        
    def log_reflection(self, state: ConversationState, reflection: str):
        module = "ReflectionEngine"
        metric = "reflectionLength"
        self.metrics.setdefault(f"{module}_{metric}", []).append(len(reflection))
        print(f"[Metrics] Reflection: {len(reflection)} characters")

    def log_anchor(self, anchor_name: str, success: bool, state: ConversationState):
        module = "AnchorModule"
        metric = "anchorApplicationSuccess"
        self.metrics.setdefault(f"{module}_{metric}", []).append(anchor_name if success else "FAILED")
        print(f"[Metrics] Anchor: {anchor_name}, Success: {success}")

    def log_outcome(self, state: ConversationState, outcome: str):
        module = "SynthesisModule"
        metric = "outputLength"
        self.metrics.setdefault(f"{module}_{metric}", []).append(len(outcome))
        print(f"[Metrics] Outcome: {len(outcome)} characters")
        
    def log_error(self, module_name: str, error_message: str, cause: Optional[Exception] = None):
        self.errors.setdefault(module_name, []).append(error_message + (f" Cause: {str(cause)}" if cause else ""))
        print(f"[ERROR] {module_name}: {error_message}" + (f" Cause: {str(cause)}" if cause else ""))
        
    def get_all_metrics(self) -> Dict[str, Any]:
        all_metrics = {}
        for key, values in self.metrics.items():
            all_metrics[f"{key}_count"] = len(values)
        for key, errs in self.errors.items():
            all_metrics[f"{key}_error_count"] = len(errs)
        return all_metrics