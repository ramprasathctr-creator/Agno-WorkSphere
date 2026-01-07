
import asyncio
import uuid
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.core.database import SessionLocal, AsyncSession
from app.models.project import Project
from app.models.user import User
from app.models.organization import OrganizationMember

async def check_project_members(project_id_str, org_id_str):
    project_id = uuid.UUID(project_id_str)
    org_id = uuid.UUID(org_id_str)
    
    async with SessionLocal() as db:
        # 1. Check Project
        result = await db.execute(select(Project).where(Project.id == project_id))
        project = result.scalar_one_or_none()
        if not project:
            print(f"Project {project_id_str} not found")
            return
            
        print(f"Project: {project.name}")
        print(f"Created By: {project.created_by}")
        print(f"Org ID: {project.organization_id}")
        print(f"Explicit Team Members: {project.team_members}")
        
        # 2. Check Creator as Org Member
        creator_org_member = await db.execute(
            select(OrganizationMember)
            .where(
                and_(
                    OrganizationMember.user_id == project.created_by,
                    OrganizationMember.organization_id == org_id
                )
            )
        )
        comm = creator_org_member.scalar_one_or_none()
        if comm:
            print(f"Creator {project.created_by} is an Org Member with role {comm.role}")
        else:
            print(f"Creator {project.created_by} IS NOT AN ORG MEMBER of {org_id_str}")

        # 3. Check get_project_team_members logic equivalent
        # Creator logic
        project_creator_result = await db.execute(
            select(User, OrganizationMember)
            .join(OrganizationMember, OrganizationMember.user_id == User.id)
            .where(
                and_(
                    User.id == project.created_by,
                    OrganizationMember.organization_id == org_id
                )
            )
        )
        creator_data = project_creator_result.first()
        if creator_data:
            print("Successfully found creator in org members join")
        else:
            print("FAILED to find creator in org members join")

if __name__ == "__main__":
    # From screenshot: 
    # ProjectID: 76d0b0ca-8c5d-4a2e-bcd2-3f4577f11257
    # OrgID: c4240d6f-e792-42ac-816e-caf29162246c
    asyncio.run(check_project_members(
        "76d0b0ca-8c5d-4a2e-bcd2-3f4577f11257", 
        "c4240d6f-e792-42ac-816e-caf29162246c"
    ))
