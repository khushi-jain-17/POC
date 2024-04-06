from marshmallow import Schema, fields, validate, ValidationError 
import re


class UsernameValidator:
    @staticmethod
    def validate_name(uname):
        if uname[0].islower():
            raise ValidationError("Username must start with a capital letter")

class EmailValidator:
    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError('Invalid email address')

class PasswordValidator:
    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter')

        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter')

        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one digit')

        if not re.search(r'[\W]', password):
            raise ValidationError('Password must contain at least one special character')


class UserSchema(Schema):
    uid = fields.Integer(required = True)
    uname = fields.String(required=True, validate=[UsernameValidator.validate_name, validate.Length(min=1, max=100)])
    email = fields.Email(required=True, validate=EmailValidator.validate_email)
    password = fields.String(required=True, validate=PasswordValidator.validate_password)


class RoleSchema(Schema):
    role_id = fields.Integer(dump_only=True)
    rname = fields.String(required=True, validate=validate.Length(min=1, max=100))


