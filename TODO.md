# Project Allocator - Backlog & TODO

## 🚀 Active Development
- [x] **Categories**: Dynamic project tagging (backend/frontend)
- [x] **Thesis Upload**: Supervisor attachments & Student final submission
- [x] **Forms**: PDF Registration Form generation
- [x] **Student Workflow**: Student-proposed projects & Supervisor acceptance flow

## 🐛 Known Issues / Fixes
- [x] Fix 500 error on projects without proposals (Demo Data)
- [x] Fix "Failed to create project" validation error on optional fields
- [x] Graceful handling of "System" projects in frontend table

## 📋 Backlog (Future Work)
### Student Workflow Refinements
- [ ] **Email Notifications**: Notify supervisors when a student proposes a project.
- [ ] **Approval Dashboard**: Dedicated view for Supervisors to manage pending student requests.
- [ ] **Status Tracking**: Clearer UI for students to see if their proposal is "Pending Review" or "Accepted".

### Security & Robustness
- [ ] **File Validation**: Enforce PDF-only uploads and size limits.
- [ ] **Auth Integration**: Switch from Dummy Auth to Real Azure AD in production.
- [ ] **Database Migrations**: Automate migration application on container startup.

### Features
- [ ] **Archive**: Ability to archive past terms/years.
- [ ] **Batch Import**: Upload CSV of projects for bulk creation.
- [ ] **Ranking Algorithm**: Refine allocation algorithm weights based on category preferences.

## 🛠 Tech Debt
- [ ] Clean up populate_demo.py and seed.py scripts.
- [ ] Normalize inconsistent API response models (ProjectReadWithProposal vs Optional).
