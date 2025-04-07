from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="Employee API Project", version="1.0.0")

@app.get(path="/")
def root():
    return {"message": "Server is running"}

# ==============================
# Employee Login Endpoint
# ==============================

class EmployeeLoginRequest(BaseModel):
    email: EmailStr
    password: str


class EmployeeLoginResponse(BaseModel):
    userId: int
    firstName: str
    lastName: str
    email: EmailStr
    token: str


@app.post("/api/auth/signin", response_model=EmployeeLoginResponse)
def employee_signin(login: EmployeeLoginRequest):
    # Dummy implementation: in a real app, verify the credentials.
    if login.email == "john.doe@example.com" and login.password == "securePassword123":
        return EmployeeLoginResponse(
            userId=101,
            firstName="John",
            lastName="Doe",
            email=login.email,
            token="eyJhbGciOiJIUzI1NiIsInR..."
        )
    raise HTTPException(status_code=401, detail="Invalid email or password")


# ==============================
# User Organization Endpoints
# ==============================

# GET: Retrieve user organization details
class Organization(BaseModel):
    name: str
    organisationId: int
    image: str
    roleId: int
    enableScreenshot: int
    description: str
    role: str
    otherRoleIds: List[int]


class UserOrganizationResponseData(BaseModel):
    organisationList: List[Organization]


class UserOrganizationResponse(BaseModel):
    status: str
    data: UserOrganizationResponseData
    message: str


@app.get("/api/organisation/getUserOrganization", response_model=UserOrganizationResponse)
def get_user_organization():
    # Dummy organization list
    org_list = [
        Organization(
            name="ExampleOrg",
            organisationId=123,
            image="https://example.com/images/org123.png",
            roleId=2,
            enableScreenshot=0,
            description="Example organization description",
            role="Admin",
            otherRoleIds=[3, 4]
        ),
        Organization(
            name="TestOrg",
            organisationId=456,
            image="https://example.com/images/org456.png",
            roleId=3,
            enableScreenshot=1,
            description="Test organization for demo purposes",
            role="User",
            otherRoleIds=[]
        )
    ]
    return UserOrganizationResponse(
        status="success",
        data=UserOrganizationResponseData(organisationList=org_list),
        message="User organisation list"
    )


# POST: Retrieve projects for a given organization
class OrganizationProjectsRequest(BaseModel):
    organisationId: int


class ProjectUser(BaseModel):
    userId: int
    fullName: str
    profileImage: Optional[str] = None


class Project(BaseModel):
    projectId: int
    name: str
    status: int
    startDate: datetime
    users: List[ProjectUser]


class OrganizationProjectsData(BaseModel):
    projectLists: List[Project]


class OrganizationProjectsResponse(BaseModel):
    status: str
    data: OrganizationProjectsData
    message: str


@app.post("/api/organisation/getUserOrganization", response_model=OrganizationProjectsResponse)
def get_organization_projects(org_request: OrganizationProjectsRequest, authorization: str = Header(...)):
    # Basic token check; in production, validate the JWT properly.
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    # Dummy project data based on the provided organisationId.
    projects = [
        Project(
            projectId=101,
            name="Project Alpha",
            status=0,
            startDate=datetime(2023, 1, 1, 10, 0, 0),
            users=[
                ProjectUser(userId=201, fullName="John Doe"),
                ProjectUser(userId=202, fullName="Jane Smith")
            ]
        ),
        Project(
            projectId=102,
            name="Project Beta",
            status=0,
            startDate=datetime(2024, 2, 15, 9, 30, 0),
            users=[
                ProjectUser(userId=301, fullName="Alice Brown", profileImage="https://example.com/profiles/301.jpg"),
                ProjectUser(userId=302, fullName="Bob White", profileImage="https://example.com/profiles/302.jpg")
            ]
        )
    ]
    return OrganizationProjectsResponse(
        status="success",
        data=OrganizationProjectsData(projectLists=projects),
        message="User organization project list retrieved successfully."
    )


# ==============================
# Task Details Endpoint
# ==============================

class TaskDetailsRequest(BaseModel):
    projectId: int
    organisationId: int


class TaskDetail(BaseModel):
    taskId: int
    name: str
    projectId: int
    projectName: str
    organisationId: int
    time: Optional[datetime] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    screenshots: str = ""
    notes: str = ""
    unTrackedTime: Optional[int] = None
    lastScreenShotTime: str
    totalTime: int


class TaskDetailsData(BaseModel):
    taskDetails: List[TaskDetail]


class TaskDetailsResponse(BaseModel):
    status: str
    data: TaskDetailsData
    message: str


@app.post("/api/task/getTaskByProjectId", response_model=TaskDetailsResponse)
def get_task_by_project_id(task_request: TaskDetailsRequest, authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    tasks = [
        TaskDetail(
            taskId=1663,
            name="Introduction",
            projectId=803,
            projectName="AI-ML",
            organisationId=698,
            lastScreenShotTime="00:00:00",
            totalTime=0
        ),
        TaskDetail(
            taskId=1670,
            name="Interview",
            projectId=803,
            projectName="AI-ML",
            organisationId=698,
            lastScreenShotTime="00:00:00",
            totalTime=0
        ),
        TaskDetail(
            taskId=1684,
            name="AI Database Query Generator",
            projectId=803,
            projectName="AI-ML",
            organisationId=698,
            lastScreenShotTime="00:00:00",
            totalTime=0
        )
    ]
    return TaskDetailsResponse(
        status="success",
        data=TaskDetailsData(taskDetails=tasks),
        message="Success"
    )


# ==============================
# Add Activity List Endpoint
# ==============================

class Activity(BaseModel):
    taskId: int
    projectId: int
    startTime: datetime
    endTime: datetime
    mouseActivity: int
    keyboardActivity: int
    totalActivity: int
    notes: str
    organisationId: int
    uri: str
    unTrackedTime: int


class AddActivityRequest(BaseModel):
    activityData: List[Activity]


class ActivityInsertMetadata(BaseModel):
    fieldCount: int
    affectedRows: int
    insertId: int
    serverStatus: int
    warningCount: int
    message: str
    protocol41: bool
    changedRows: int


class AddActivityResponseData(BaseModel):
    success: bool
    activities: ActivityInsertMetadata


class AddActivityResponse(BaseModel):
    status: str
    data: AddActivityResponseData
    message: str


@app.post("/api/activity/addActivityList", response_model=AddActivityResponse)
def add_activity_list(activity_request: AddActivityRequest, authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    # Simulated database insert metadata.
    metadata = ActivityInsertMetadata(
        fieldCount=0,
        affectedRows=1,
        insertId=2283680,
        serverStatus=2,
        warningCount=0,
        message="",
        protocol41=True,
        changedRows=0
    )
    return AddActivityResponse(
        status="success",
        data=AddActivityResponseData(success=True, activities=metadata),
        message="Success"
    )


# ==============================
# Run the API using Uvicorn
# ==============================

if __name__ == "__main__":

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
