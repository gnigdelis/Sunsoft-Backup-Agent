from pprint import pprint

from core.engine.guardian_engine import (
    GuardianEngine,
)


guardian = GuardianEngine()


result = guardian.start()


pprint(result)