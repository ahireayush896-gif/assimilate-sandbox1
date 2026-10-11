def ping():
    """Check health status and return ok status."""
    return {"status": "ok"}


if __name__ == "__main__":
    print(ping())
