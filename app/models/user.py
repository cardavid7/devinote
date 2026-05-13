from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email : str = Field(index=True, unique=True, nullable=False)
    full_name : str = Field(default="")
    hashed_password: str = Field(nullable=False)
    active: bool = Field(default=True)

class UserCreate(SQLModel):
    email : str
    full_name : str = ""
    password: str

class UserRead(SQLModel):
    id: int
    email : str
    full_name : str
    
    model_config = {"from_attributes":True}


