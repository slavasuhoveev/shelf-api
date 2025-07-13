from pydantic import BaseModel, ConfigDict


class BaseShelfModel(BaseModel):
    """Base Pydantic model for the Shelf project with shared configuration.

    Configuration options:
    ---------------------
    validate_assignment: True
        Automatically validate and coerce values when assigning to fields after model initialization.

    strict: True
        Enforces strict type checking (e.g., int is not accepted where float is expected, and vice versa).
        Helps catch subtle bugs and ensures predictable validation.

    use_enum_values: True
        Automatically converts Enum members to their values when exporting or serializing the model.
        For example, Color.RED will be serialized as "red" instead of "Color.RED".

    extra: "forbid"
        Forbids any unexpected fields that are not explicitly declared in the model.
        Useful for catching typos or unexpected data.

    exclude_none: True
        Automatically excludes fields with `None` values from the serialized output (e.g., `.dict()` or `.json()`).
        Helps reduce payload size and omit unset optional fields.

    from_attributes: True
        Allows instantiating models from ORM objects (e.g., SQLAlchemy), enabling attribute-based parsing.
        Equivalent to `orm_mode = True` in Pydantic v1.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        strict=True,
        use_enum_values=True,
        extra="forbid",
        exclude_none=True,
        from_attributes=True
    )
