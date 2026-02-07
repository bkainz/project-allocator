import random
from sqlmodel import Session, create_engine, select
from src.models import User, Project, ProjectDetail, ProjectDetailTemplate
from src.db import DATABASE_URL

engine = create_engine(DATABASE_URL)

def populate():
    with Session(engine) as session:
        # 1. Create Supervisors (Staff)
        supervisors = []
        for i in range(1, 4):
            email = f"prof{i}@example.com"
            user = session.exec(select(User).where(User.email == email)).one_or_none()
            if not user:
                user = User(email=email, name=f"Professor {i}", role="staff")
                session.add(user)
                print(f"Created supervisor: {user.name}")
            supervisors.append(user)
        
        # 2. Create Students
        students = []
        for i in range(1, 6):
            email = f"student{i}@example.com"
            user = session.exec(select(User).where(User.email == email)).one_or_none()
            if not user:
                user = User(email=email, name=f"Student {i}", role="student")
                session.add(user)
                print(f"Created student: {user.name}")
            students.append(user)

        session.commit() # Commit users to get IDs

        # 3. Create Project Templates
        template_defs = [
            {"title": "Prerequisites", "description": "Required skills", "message": "List skills", "type": "textfield", "required": False},
            {"title": "Category", "description": "Project Type", "message": "Select type", "type": "select", "options": ["Self-Driven", "Industry", "Supervised"], "required": True},
            {"title": "Project Plan", "description": "Upload your project plan PDF", "message": "Upload file", "type": "file", "required": False}
        ]
        
        templates = []
        for t_def in template_defs:
             # Check if exists by title
             t = session.exec(select(ProjectDetailTemplate).where(ProjectDetailTemplate.title == t_def["title"])).one_or_none()
             if not t:
                 t = ProjectDetailTemplate(**t_def)
                 session.add(t)
                 session.commit()
                 print(f"Created template: {t.title}")
             templates.append(t)

        # 4. Create Example Projects
        project_ideas = [
            ("AI for Medical Imaging", "Using deep learning to detect anomalies in X-rays using public datasets.", "Self-Driven"),
            ("Automated Form Filling Agent", "LLM agent that parses PDF forms and auto-populates them from user context.", "Supervised"),
            ("Distributed Compute Allocator", "Optimizing GPU usage across university clusters.", "Industry"),
            ("Federated Learning on Mobile", "Privacy-preserving ML on edge devices.", "Self-Driven"),
            ("Robotic Surgery Assistant", "Computer vision for surgical tool tracking.", "Supervised")
        ]

        for title, desc, cat in project_ideas:
            # Check if exists
            exists = session.exec(select(Project).where(Project.title == title)).one_or_none()
            if not exists:
                proj = Project(title=title, description=desc, approved=True)
                session.add(proj)
                session.commit() # to get ID
                
                # Add details
                # Find category template
                cat_template = next((t for t in templates if t.title == "Category"), None)
                if cat_template:
                    d = ProjectDetail(project_id=proj.id, template_id=cat_template.id, value=cat)
                    session.add(d)
                
                print(f"Created project: {title}")
        
        session.commit()
        print("Demo data population complete!")

if __name__ == "__main__":
    populate()
