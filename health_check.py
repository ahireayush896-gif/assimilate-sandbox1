"""Health check script."""


def ping():
    """Return health status."""
    return {"status": "ok"}


if __name__ == "__main__":
    print(ping())
