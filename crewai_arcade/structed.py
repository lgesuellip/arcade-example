from abc import ABC
from typing import Any, Callable, Optional, Type, Union
from pydantic import BaseModel, ConfigDict, Field
from crewai_tools.tools.base_tool import BaseTool

class StructuredTool(BaseTool):
    """Tool that can operate on any number of inputs."""

    func: Optional[Callable[..., Any]] = None
    """The function to run when the tool is called."""

    def __init__(self, *args: Any, func, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.func = func

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Use the tool."""
        if self.func:
            return self.func(*args, **kwargs)
        msg = "StructuredTool does not support invocation without a function."
        raise NotImplementedError(msg)

    @classmethod
    def from_function(
        cls,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        args_schema: Optional[Type[BaseModel]] = None,
        **kwargs: Any,
    ) -> "StructuredTool":
        """Create tool from a function.

        Args:
            func: The function to create a tool from
            name: The name of the tool. Defaults to the function name
            description: The description of the tool. Defaults to the function docstring
            args_schema: The schema for the function arguments
            **kwargs: Additional arguments to pass to the tool

        Returns:
            The tool

        Raises:
            ValueError: If the function has no docstring and no description was provided
        """
        return cls(
            name=name,
            func=func,
            args_schema=args_schema,  # type: ignore[arg-type]
            description=description,
            **kwargs,
        )
