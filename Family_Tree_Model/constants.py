

KING = "king"

class Gender:
    MALE = "male"
    FEMALE = "female"

class Relation:
    SON = "son"
    DAUGHTER = "daughter"
    HUSBAND = "husband"
    WIFE = "wife"
    SPOUSE = "spouse"

    FATHER = "father"
    MOTHER = "mother"
    BROTHER = "brother"
    SISTER = "sister"
    CHILDREN = "children"

    BROTHER_IN_LAW = "brother-in-law"
    SISTER_IN_LAW = "sister-in-law"
    COUSIN = "cousin"

    MATERNAL_UNCLE = "maternal-uncle"
    MATERNAL_AUNT = "maternal-aunt"
    PATERNAL_UNCLE = "paternal-uncle"
    PATERNAL_AUNT = "paternal-aunt"

    GRAND_SON = "grand-son"
    GRAND_DAUGHTER = "grand-daughter"

class Status:
    ADD_SUCCESS = "ADDITION_SUCCEEDED"
    ADD_FAILED = "ADDITION_FAILED"
    NOT_FOUND = "PERSON_NOT_FOUND"
    REL_NOT_FOUND = "RELATIONSHIP_NOT_FOUND"
    EXCEPTION = "EXCEPTION_OCCURED: "
    NOT_SUPPORTED = "NOT_SUPPORTED"

class Pattern:
    ADD = "ADD_TO_FAMILY "
    GET = "GET_RELATIONSHIP "
