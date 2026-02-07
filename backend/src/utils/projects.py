import json

from fastapi import HTTPException

from ..models import (
    Project,
    ProjectDetailCreate,
    ProjectDetailRead,
    ProjectDetailTemplate,
    ProjectDetailUpdate,
    ProjectReadWithDetails,
)


def parse_project(project: Project) -> ProjectReadWithDetails:
    # Need to convert to read model to allow any types during parsing.
    project = ProjectReadWithDetails.model_validate(project)
    project_details = []
    for detail in project.details:
        detail = parse_project_detail(detail.template, detail)
        project_details.append(detail)
    project.details = project_details
    return project


def parse_project_detail(template: ProjectDetailTemplate, detail: ProjectDetailRead) -> ProjectDetailRead:
    detail = detail.model_copy(deep=True)
    match template.type:
        case "number" | "slider":
            if detail.value and detail.value != "":
                try:
                    detail.value = int(detail.value)
                except ValueError:
                    detail.value = 0
            else:
                detail.value = 0
        case "switch":
            detail.value = detail.value == "true"
        case "checkbox" | "categories":
            try:
                detail.value = json.loads(detail.value)
            except (TypeError, json.JSONDecodeError):
                detail.value = []
    return detail


def serialize_project_detail(
    template: ProjectDetailTemplate, detail: ProjectDetailCreate | ProjectDetailUpdate
) -> ProjectDetailCreate | ProjectDetailUpdate:
    check_project_detail(template, detail)
    detail = detail.model_copy(deep=True)
    
    # Handle None/Empty values
    if detail.value is None or detail.value == "":
        if template.type in ["checkbox", "categories"]:
            detail.value = "[]"
        elif template.type == "switch":
            detail.value = "false"
        else:
            detail.value = ""
        return detail

    match template.type:
        case "number" | "slider":
            detail.value = str(detail.value)
        case "switch":
            detail.value = "true" if detail.value else "false"
        case "checkbox" | "categories":
            detail.value = json.dumps(detail.value)
    
    # Ensure result is always a string for the database
    if not isinstance(detail.value, str):
        detail.value = str(detail.value)
        
    return detail


def check_project_detail(template: ProjectDetailTemplate, detail: ProjectDetailCreate | ProjectDetailUpdate):
    # Skip validation if optional and empty
    if not template.required and (detail.value is None or detail.value == "" or detail.value == []):
        return

    match template.type:
        case "slider":
            if detail.value is not None:
                try:
                    val = int(detail.value)
                    if not (0 <= val <= 100):
                        raise HTTPException(status_code=400, detail="Invalid project detail value")
                except ValueError:
                     raise HTTPException(status_code=400, detail="Invalid project detail value")
        case "select" | "radio":
            if detail.value not in template.options:
                raise HTTPException(status_code=400, detail="Invalid project detail value")
        case "checkbox":
            if not isinstance(detail.value, list) or not all(option in template.options for option in detail.value):
                raise HTTPException(status_code=400, detail="Invalid project detail value")
