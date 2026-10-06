import os


def vault_secret(key: str) -> str:
    """Obtiene un secreto técnico desde Vault.

    Para desarrollo/pruebas se puede habilitar explícitamente el fallback por
    variables de entorno con ALLOW_ENV_SECRET_FALLBACK=true. Los secretos nunca
    están escritos en el código.
    """
    addr = os.getenv("VAULT_ADDR")
    token = os.getenv("VAULT_TOKEN")

    if addr and token:
        try:
            import hvac

            client = hvac.Client(url=addr, token=token)
            if client.is_authenticated():
                data = client.secrets.kv.v2.read_secret_version(
                    path="gateway"
                )["data"]["data"]
                value = data.get(key)
                if value:
                    return value
        except Exception:
            pass

    if os.getenv("ALLOW_ENV_SECRET_FALLBACK", "false").lower() == "true":
        value = os.getenv(key.upper())
        if value:
            return value

    raise RuntimeError(
        f"No se pudo obtener el secreto '{key}' desde Vault. "
        "Configura VAULT_ADDR/VAULT_TOKEN o habilita explícitamente "
        "ALLOW_ENV_SECRET_FALLBACK para una ejecución local de desarrollo."
    )
