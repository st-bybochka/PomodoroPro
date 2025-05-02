class PasswordValidator:

    @staticmethod
    def validate_password(password: str) -> str:
        errors = []
        if len(password) < 8:
            errors.append("Длина пароля должна быть не менее 8 символов")
        if not any(char.isupper() for char in password):
            errors.append("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(char.isdigit() for char in password):
            errors.append("Пароль должен содержать хотя бы одну цифру")

        if errors:
            raise ValueError("; ".join(errors))

        return password
