from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from com.fractalcommunication.state import ConversationState

class IAnchor(ABC):
    @abstractmethod
    def name(self) -> str:
        """Unique anchor identifier."""
        pass

    @abstractmethod
    def apply(self, reflection: str, state: Any) -> str:
        """Modulate the reflection according to this anchor."""
        pass

    @abstractmethod
    def microtest(self) -> bool:
        """Provable micro-test for safety/efficacy."""
        pass


class IReflectionEngine(ABC):
    @abstractmethod
    def reflect(self, state: 'ConversationState') -> str:
        pass


class IAnchorModule(ABC):
    @abstractmethod
    def select_anchor(self, state: 'ConversationState') -> Optional[IAnchor]:
        pass

    @abstractmethod
    def register_anchor(self, anchor: IAnchor):
        pass


class ISynthesisModule(ABC):
    @abstractmethod
    def synthesize(self, reflection: str, anchored_response: str, state: 'ConversationState') -> str:
        pass


class IMemory(ABC):
    @abstractmethod
    def get_short_term(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_long_term(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, key: str, value: Any, scope: str = "short_term"):
        pass


class IMetricsLogger(ABC):
    @abstractmethod
    def log_reflection(self, state: 'ConversationState', reflection: str):
        pass

    @abstractmethod
    def log_anchor(self, anchor_name: str, success: bool, state: 'ConversationState'):
        pass

    @abstractmethod
    def log_outcome(self, state: 'ConversationState', outcome: str):
        pass


class IOrchestrator(ABC):
    @abstractmethod
    def run_conversation(self, user_input: str, user_id: str, session_id: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def handle_error(self, error: Exception, state: 'ConversationState') -> str:
        pass

    @abstractmethod
    def branch(self, state: 'ConversationState', options: List[str]) -> str:
        pass

    @abstractmethod
    def interrupt(self, state: 'ConversationState', reason: str) -> str:
        pass