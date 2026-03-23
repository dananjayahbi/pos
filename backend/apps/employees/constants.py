"""Constants for the Employees application."""

# ════════════════════════════════════════════════════════════════════════
# Employment Type Choices
# ════════════════════════════════════════════════════════════════════════

EMPLOYMENT_TYPE_FULL_TIME = "full_time"
EMPLOYMENT_TYPE_PART_TIME = "part_time"
EMPLOYMENT_TYPE_CONTRACT = "contract"
EMPLOYMENT_TYPE_INTERN = "intern"
EMPLOYMENT_TYPE_PROBATION = "probation"

EMPLOYMENT_TYPE_CHOICES = [
    (EMPLOYMENT_TYPE_FULL_TIME, "Full Time"),
    (EMPLOYMENT_TYPE_PART_TIME, "Part Time"),
    (EMPLOYMENT_TYPE_CONTRACT, "Contract"),
    (EMPLOYMENT_TYPE_INTERN, "Intern"),
    (EMPLOYMENT_TYPE_PROBATION, "Probation"),
]

DEFAULT_EMPLOYMENT_TYPE = EMPLOYMENT_TYPE_FULL_TIME

# ════════════════════════════════════════════════════════════════════════
# Employee Status Choices
# ════════════════════════════════════════════════════════════════════════

EMPLOYEE_STATUS_ACTIVE = "active"
EMPLOYEE_STATUS_INACTIVE = "inactive"
EMPLOYEE_STATUS_ON_LEAVE = "on_leave"
EMPLOYEE_STATUS_TERMINATED = "terminated"
EMPLOYEE_STATUS_RESIGNED = "resigned"

EMPLOYEE_STATUS_CHOICES = [
    (EMPLOYEE_STATUS_ACTIVE, "Active"),
    (EMPLOYEE_STATUS_INACTIVE, "Inactive"),
    (EMPLOYEE_STATUS_ON_LEAVE, "On Leave"),
    (EMPLOYEE_STATUS_TERMINATED, "Terminated"),
    (EMPLOYEE_STATUS_RESIGNED, "Resigned"),
]

DEFAULT_EMPLOYEE_STATUS = EMPLOYEE_STATUS_ACTIVE

# ════════════════════════════════════════════════════════════════════════
# Gender Choices
# ════════════════════════════════════════════════════════════════════════

GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_OTHER = "other"
GENDER_PREFER_NOT_TO_SAY = "prefer_not_to_say"

GENDER_CHOICES = [
    (GENDER_MALE, "Male"),
    (GENDER_FEMALE, "Female"),
    (GENDER_OTHER, "Other"),
    (GENDER_PREFER_NOT_TO_SAY, "Prefer Not to Say"),
]

# ════════════════════════════════════════════════════════════════════════
# Marital Status Choices
# ════════════════════════════════════════════════════════════════════════

MARITAL_STATUS_SINGLE = "single"
MARITAL_STATUS_MARRIED = "married"
MARITAL_STATUS_DIVORCED = "divorced"
MARITAL_STATUS_WIDOWED = "widowed"

MARITAL_STATUS_CHOICES = [
    (MARITAL_STATUS_SINGLE, "Single"),
    (MARITAL_STATUS_MARRIED, "Married"),
    (MARITAL_STATUS_DIVORCED, "Divorced"),
    (MARITAL_STATUS_WIDOWED, "Widowed"),
]

# ════════════════════════════════════════════════════════════════════════
# Address Type Choices
# ════════════════════════════════════════════════════════════════════════

ADDRESS_TYPE_PERMANENT = "permanent"
ADDRESS_TYPE_TEMPORARY = "temporary"
ADDRESS_TYPE_WORK = "work"

ADDRESS_TYPE_CHOICES = [
    (ADDRESS_TYPE_PERMANENT, "Permanent"),
    (ADDRESS_TYPE_TEMPORARY, "Temporary"),
    (ADDRESS_TYPE_WORK, "Work"),
]

# ════════════════════════════════════════════════════════════════════════
# Document Type Choices
# ════════════════════════════════════════════════════════════════════════

DOCUMENT_TYPE_CONTRACT = "contract"
DOCUMENT_TYPE_RESUME = "resume"
DOCUMENT_TYPE_NIC_COPY = "nic_copy"
DOCUMENT_TYPE_CERTIFICATE = "certificate"
DOCUMENT_TYPE_OTHER = "other"

DOCUMENT_TYPE_CHOICES = [
    (DOCUMENT_TYPE_CONTRACT, "Contract"),
    (DOCUMENT_TYPE_RESUME, "Resume"),
    (DOCUMENT_TYPE_NIC_COPY, "NIC Copy"),
    (DOCUMENT_TYPE_CERTIFICATE, "Certificate"),
    (DOCUMENT_TYPE_OTHER, "Other"),
]

# ════════════════════════════════════════════════════════════════════════
# Bank Account Type Choices
# ════════════════════════════════════════════════════════════════════════

ACCOUNT_TYPE_SAVINGS = "savings"
ACCOUNT_TYPE_CURRENT = "current"

ACCOUNT_TYPE_CHOICES = [
    (ACCOUNT_TYPE_SAVINGS, "Savings"),
    (ACCOUNT_TYPE_CURRENT, "Current"),
]

# ════════════════════════════════════════════════════════════════════════
# Employment History Change Type Choices
# ════════════════════════════════════════════════════════════════════════

CHANGE_TYPE_PROMOTION = "promotion"
CHANGE_TYPE_TRANSFER = "transfer"
CHANGE_TYPE_DEMOTION = "demotion"
CHANGE_TYPE_SALARY_CHANGE = "salary_change"
CHANGE_TYPE_ROLE_CHANGE = "role_change"

CHANGE_TYPE_CHOICES = [
    (CHANGE_TYPE_PROMOTION, "Promotion"),
    (CHANGE_TYPE_TRANSFER, "Transfer"),
    (CHANGE_TYPE_DEMOTION, "Demotion"),
    (CHANGE_TYPE_SALARY_CHANGE, "Salary Change"),
    (CHANGE_TYPE_ROLE_CHANGE, "Role Change"),
]

# ════════════════════════════════════════════════════════════════════════
# Relationship Choices (for emergency contacts & family)
# ════════════════════════════════════════════════════════════════════════

RELATIONSHIP_SPOUSE = "spouse"
RELATIONSHIP_PARENT = "parent"
RELATIONSHIP_CHILD = "child"
RELATIONSHIP_SIBLING = "sibling"
RELATIONSHIP_OTHER = "other"

RELATIONSHIP_CHOICES = [
    (RELATIONSHIP_SPOUSE, "Spouse"),
    (RELATIONSHIP_PARENT, "Parent"),
    (RELATIONSHIP_CHILD, "Child"),
    (RELATIONSHIP_SIBLING, "Sibling"),
    (RELATIONSHIP_OTHER, "Other"),
]

# ════════════════════════════════════════════════════════════════════════
# Sri Lanka Provinces
# ════════════════════════════════════════════════════════════════════════

PROVINCE_CHOICES = [
    ("western", "Western"),
    ("central", "Central"),
    ("southern", "Southern"),
    ("northern", "Northern"),
    ("eastern", "Eastern"),
    ("north_western", "North Western"),
    ("north_central", "North Central"),
    ("uva", "Uva"),
    ("sabaragamuwa", "Sabaragamuwa"),
]

# ════════════════════════════════════════════════════════════════════════
# Employee ID Prefix
# ════════════════════════════════════════════════════════════════════════

EMPLOYEE_ID_PREFIX = "EMP"
EMPLOYEE_ID_PADDING = 4  # EMP-0001
