import enum
import strawberry

@strawberry.enum(description="Type of the project")
class ProjectType(enum.Enum):
    SCIENTIFIC = "scientific"
    CONSTRUCTION = "construction"
    MARKETING = "marketing"
