

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

    BROTHER_IN_LAW = "brother_in_law"
    SISTER_IN_LAW = "sister_in_law"
    COUSIN = "cousin"

    MATERNAL_UNCLE = "maternal_uncle"
    MATERNAL_AUNT = "maternal_aunt"
    PATERNAL_UNCLE = "paternal_uncle"
    PATERNAL_AUNT = "paternal_aunt"

    GRAND_SON = "grand_son"
    GRAND_DAUGHTER = "grand_daughter"

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
