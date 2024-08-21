from notebook.auth.security import passwd # type: ignore
password_hash = passwd()
print(password_hash)
