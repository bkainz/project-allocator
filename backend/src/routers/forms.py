from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import Response
from sqlmodel import Session
from fpdf import FPDF
import io

from ..dependencies import check_student, get_session, get_user
from ..models import User

router = APIRouter(prefix="/forms", tags=["forms"])

@router.get(
    "/registration",
    dependencies=[Security(check_student)],
)
async def get_registration_form(
    user: Annotated[User, Depends(get_user)],
    session: Annotated[Session, Depends(get_session)],
):
    if not user.allocation:
        raise HTTPException(status_code=404, detail="User not allocated to a project")
    
    project = user.allocation.allocated_project
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "AIBE Thesis Registration Form", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    # Student Info
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, f"Student Name: {user.name}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Email: {user.email}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Project Info
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Project Details:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 10, f"Title: {project.title}")
    pdf.ln(5)
    
    # Agreement
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Agreement:", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    agreement_text = (
        "I hereby confirm that I meet all prerequisites for starting this thesis. "
        "I agree to the regulations of the examination office and the AIBE department. "
        "I will submit my thesis on time and according to the requirements."
    )
    pdf.multi_cell(0, 6, agreement_text)
    
    pdf.ln(20)
    
    # Signatures
    pdf.cell(90, 10, "______________________", new_x="RIGHT", new_y="TOP")
    pdf.cell(0, 10, "______________________", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(90, 10, "Student Signature", new_x="RIGHT", new_y="TOP")
    pdf.cell(0, 10, "Supervisor Signature", new_x="LMARGIN", new_y="NEXT")
    
    # Output
    pdf_bytes = pdf.output()
    
    return Response(
        content=bytes(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=registration_form.pdf"}
    )
