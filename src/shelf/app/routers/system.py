"""System and infrastructure endpoints.

Includes health and readiness probes.
"""

from fastapi import (
    APIRouter,
)

system_group_router = APIRouter(prefix='/system', tags=['system'])


@system_group_router.get('/healthz')
def healthz():
    """Liveness probe endpoint."""
    return {'status': 'ok'}


@system_group_router.get('/readyz')
def readyz():
    """Readiness probe endpoint (DB connectivity etc. can be added later)."""
    return {'status': 'ready'}
