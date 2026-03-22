# app/core/events.py

import logging
import asyncio
from typing import Callable, Dict, List

logger = logging.getLogger("events")

# -----------------------------------------
# Event Registry
# -----------------------------------------

listeners: Dict[str, List[Callable]] = {}


def on(event_name: str):
    """
    Decorator to register event listeners.
    """

    def decorator(func: Callable):
        listeners.setdefault(event_name, []).append(func)
        logger.info(f"Listener registered for event: {event_name}")
        return func

    return decorator


# -----------------------------------------
# Safe Event Emitter (NON-BLOCKING)
# -----------------------------------------

def emit(event_name: str, payload: dict):
    """
    Emit event safely without blocking main request.
    Supports both sync and async handlers.
    """

    handlers = listeners.get(event_name, [])
    logger.info(f"Event emitted: {event_name} -> {len(handlers)} handlers")

    for func in handlers:
        try:
            # If async function → run in background
            if asyncio.iscoroutinefunction(func):
                asyncio.create_task(_run_async_handler(func, payload))
            else:
                # Run sync function in thread (non-blocking)
                asyncio.get_event_loop().run_in_executor(
                    None, _run_sync_handler, func, payload
                )
        except Exception as e:
            logger.exception(f"Failed to dispatch handler: {e}")


async def _run_async_handler(func: Callable, payload: dict):
    try:
        await func(payload)
    except Exception as e:
        logger.exception(f"Async handler failed: {e}")


def _run_sync_handler(func: Callable, payload: dict):
    try:
        func(payload)
    except Exception as e:
        logger.exception(f"Sync handler failed: {e}")


# -----------------------------------------
# Event Names (Centralized)
# -----------------------------------------

TENANT_CREATED = "tenant_created"
RENT_DUE = "rent_due"
PAYMENT_RECEIVED = "payment_received"
INVOICE_CREATED = "invoice_created"
SUBSCRIPTION_ACTIVATED = "subscription_activated"
