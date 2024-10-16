from gurobipy import quicksum

RowN = 4
ColN = 4
bs = RowN * ColN
MC = [
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 0]
]


class MITMPreConstraints:
    @staticmethod
    def Separate_Without_Guess_i(
            IP_1,
            IP_2,
            SupP_Blue_1_i,
            SupP_Blue_2_i,
            SupP_Red__1_i,
            SupP_Red__2_i,
            In_isNotWhite_i,
            model
    ):
        model.addGenConstrOr(In_isNotWhite_i, [IP_1, IP_2])
        model.addConstr(SupP_Blue_1_i - In_isNotWhite_i == 0)
        model.addConstr(SupP_Blue_2_i - IP_2 == 0)
        model.addConstr(SupP_Red__2_i - SupP_Blue_1_i == 0)
        model.addConstr(SupP_Red__1_i - IP_1 == 0)

    @staticmethod
    def NXor_SupP_Blue_i(
            IP_SupP_Blue_1,
            IP_SupP_Blue_2,
            OP_SupP_Blue_1_i,
            OP_SupP_Blue_2_i,
            CD_XOR_Blue_i,
            SumGary_SupP_Blue,
            IP_hasNoWhite_i,
            IP_SupP_Blue_AND_2_i,
            model
    ):
        n = len(IP_SupP_Blue_1)
        model.addGenConstrAnd(IP_hasNoWhite_i, IP_SupP_Blue_1)
        model.addGenConstrAnd(IP_SupP_Blue_AND_2_i, IP_SupP_Blue_2)
        model.addConstr(OP_SupP_Blue_1_i - IP_hasNoWhite_i == 0)
        model.addConstr(OP_SupP_Blue_2_i - IP_hasNoWhite_i <= 0)
        model.addConstr(CD_XOR_Blue_i - OP_SupP_Blue_2_i + IP_SupP_Blue_AND_2_i == 0)
        model.addConstr(quicksum(IP_SupP_Blue_2) + OP_SupP_Blue_2_i - SumGary_SupP_Blue == 0)
        model.addConstr(SumGary_SupP_Blue - 2 * IP_SupP_Blue_AND_2_i <= n - 1)
        model.addConstr(SumGary_SupP_Blue - (n + 1) * IP_SupP_Blue_AND_2_i >= 0)

    @staticmethod
    def NXor_SupP_Red_i(
            IP_SupP_Red_1,
            IP_SupP_Red_2,
            OP_SupP_Red_1_i,
            OP_SupP_Red_2_i,
            CD_XOR_Red_i,
            SumGary_SupP_Red,
            IP_hasNoWhite_i,
            IP_SupP_Red__AND_1_i,
            model
    ):
        n = len(IP_SupP_Red_2)
        # model.addConsAnd(IP_SupP_Red_2, IP_hasNoWhite_i)
        model.addGenConstrAnd(IP_SupP_Red__AND_1_i, IP_SupP_Red_1)
        model.addConstr(OP_SupP_Red_2_i - IP_hasNoWhite_i == 0)
        model.addConstr(OP_SupP_Red_1_i - IP_hasNoWhite_i <= 0)
        model.addConstr(CD_XOR_Red_i - OP_SupP_Red_1_i + IP_SupP_Red__AND_1_i == 0)
        model.addConstr(quicksum(IP_SupP_Red_1) + OP_SupP_Red_1_i - SumGary_SupP_Red == 0)
        model.addConstr(SumGary_SupP_Red - 2 * IP_SupP_Red__AND_1_i <= n - 1)
        model.addConstr(SumGary_SupP_Red - (n + 1) * IP_SupP_Red__AND_1_i >= 0)

    @staticmethod
    def Xor2_SupP_Blue_i(
            IP_SupP_Blue_1,
            IP_SupP_Blue_2,
            Key_SupP_Blue_1,
            Key_SupP_Blue_2,
            OP_SupP_Blue_1_i,
            OP_SupP_Blue_2_i,
            CD_Key_Blue_i,
            CD_Xor_Blue_i,
            model
    ):
        model.addConstr(Key_SupP_Blue_1 == 1)
        model.addConstr(IP_SupP_Blue_1 >= IP_SupP_Blue_2)
        model.addConstr(IP_SupP_Blue_1 == OP_SupP_Blue_1_i)
        model.addConstr(IP_SupP_Blue_2 - OP_SupP_Blue_2_i + CD_Xor_Blue_i >= 0)
        model.addConstr(IP_SupP_Blue_1 - IP_SupP_Blue_2 - CD_Xor_Blue_i >= 0)
        model.addConstr(- IP_SupP_Blue_2 - Key_SupP_Blue_2 + OP_SupP_Blue_2_i - CD_Xor_Blue_i + 1 >= 0)
        model.addConstr(OP_SupP_Blue_2_i - CD_Xor_Blue_i >= 0)
        model.addConstr(- IP_SupP_Blue_2 - Key_SupP_Blue_2 + OP_SupP_Blue_2_i + CD_Key_Blue_i - 2 * CD_Xor_Blue_i + 1 >= 0)
        model.addConstr(Key_SupP_Blue_2 - CD_Key_Blue_i >= 0)
        model.addConstr(Key_SupP_Blue_2 - OP_SupP_Blue_2_i + CD_Xor_Blue_i >= 0)

    @staticmethod
    def Xor2_SupP_Red_i(
            IP_SupP_Red_1,
            IP_SupP_Red_2,
            Key_SupP_Red_1,
            Key_SupP_Red_2,
            OP_SupP_Red_1_i,
            OP_SupP_Red_2_i,
            CD_Key_Red_i,
            CD_Xor_Red_i,
            model
    ):
        model.addConstr(Key_SupP_Red_2 == 1)
        model.addConstr(IP_SupP_Red_2 >= IP_SupP_Red_1)
        model.addConstr(IP_SupP_Red_2 == OP_SupP_Red_2_i)
        model.addConstr(IP_SupP_Red_1 - OP_SupP_Red_1_i + CD_Xor_Red_i >= 0)
        model.addConstr(- IP_SupP_Red_1 + IP_SupP_Red_2 - CD_Xor_Red_i >= 0)
        model.addConstr(- IP_SupP_Red_1 - Key_SupP_Red_1 + OP_SupP_Red_1_i - CD_Xor_Red_i + 1 >= 0)
        model.addConstr(OP_SupP_Red_1_i - CD_Xor_Red_i >= 0)
        model.addConstr(- IP_SupP_Red_1 - Key_SupP_Red_1 + OP_SupP_Red_1_i + CD_Key_Red_i - 2 * CD_Xor_Red_i + 1 >= 0)
        model.addConstr(Key_SupP_Red_1 - CD_Key_Red_i >= 0)
        model.addConstr(Key_SupP_Red_1 - OP_SupP_Red_1_i + CD_Xor_Red_i >= 0)

    @staticmethod
    def compute_real_CD_MC(IP, CD, CD_Real, model):
        model.addConstr(CD[0] + CD[1] + CD[2] + CD[3] - CD_Real + 0 >= 0)
        model.addConstr(- 2 * IP[0] - 2 * IP[1] - 2 * IP[2] - 2 * IP[3] - 3 * CD[0] - 3 * CD[1] - 3 * CD[2] - 3 * CD[3] + 2 * CD_Real + 8 >= 0)
        model.addConstr(IP[0] + IP[1] + IP[2] + IP[3] - 3 * CD[0] - 3 * CD[1] - 3 * CD[2] - 3 * CD[3] + 4 * CD_Real + 0 >= 0)
        model.addConstr(- 3 * IP[0] - 3 * IP[2] - 3 * IP[3] - 2 * CD_Real + 9 >= 0)
        model.addConstr(- 2 * IP[0] - 5 * IP[1] - 2 * IP[2] - 2 * IP[3] + 3 * CD[1] - 3 * CD_Real + 11 >= 0)
        model.addConstr(- 4 * IP[1] - 3 * IP[2] - 4 * IP[3] - 6 * CD[0] - 2 * CD[1] - 2 * CD[3] + CD_Real + 11 >= 0)
        model.addConstr(- 4 * IP[0] - 4 * IP[1] - 3 * IP[3] - 2 * CD[0] - 2 * CD[1] - 6 * CD[2] + CD_Real + 11 >= 0)
        model.addConstr(- 3 * IP[0] - 4 * IP[1] - 4 * IP[2] - 2 * CD[1] - 2 * CD[2] - 6 * CD[3] + CD_Real + 11 >= 0)
        model.addConstr(- 2 * IP[0] + IP[1] - 2 * IP[2] - IP[3] - CD[0] - 4 * CD[1] - CD[2] + CD_Real + 5 >= 0)
        model.addConstr(IP[0] + 2 * IP[1] + IP[2] + IP[3] - 2 * CD[0] - CD[1] - 2 * CD[2] - 2 * CD[3] + 2 * CD_Real + 0 >= 0)
        model.addConstr(- 2 * IP[0] - 2 * IP[1] - 2 * IP[2] - 2 * IP[3] - 3 * CD[1] - CD_Real + 8 >= 0)
        model.addConstr(- 3 * IP[0] - 2 * IP[2] - CD[0] - 2 * CD[1] - 2 * CD[3] + CD_Real + 5 >= 0)
        model.addConstr(- 2 * IP[0] - 3 * IP[3] - 2 * CD[1] - 2 * CD[2] - CD[3] + CD_Real + 5 >= 0)
        model.addConstr(- IP[2] + CD[2] - CD_Real + 3 >= 0)
        model.addConstr(- IP[3] + CD[3] - CD_Real + 3 >= 0)
        model.addConstr(- IP[0] + CD[0] - CD_Real + 3 >= 0)

    @staticmethod
    def Match(InCol1, InCol2, DOM, model):
        model.addConstr(InCol1[0] + InCol1[1] + InCol1[2] + InCol1[3] + InCol2[0] + InCol2[1] + InCol2[2] + InCol2[3] - 4 * DOM + 0 >= 0)
        model.addConstr(- InCol1[0] - InCol1[1] - InCol1[2] - InCol1[3] - InCol2[0] - InCol2[1] - InCol2[2] - InCol2[3] + 4 * DOM + 4 >= 0)
        model.addConstr(2 * InCol1[0] + 2 * InCol1[1] + InCol1[2] + 2 * InCol1[3] + InCol2[0] + InCol2[1] + InCol2[3] - 4 * DOM + 0 >= 0)
        model.addConstr(InCol1[2] + InCol1[3] + 2 * InCol2[1] + InCol2[2] + InCol2[3] - 2 * DOM + 0 >= 0)
        model.addConstr(InCol1[0] + 2 * InCol2[0] + InCol2[1] + InCol2[2] + InCol2[3] - 2 * DOM + 0 >= 0)
        model.addConstr(InCol1[0] + InCol1[1] + 2 * InCol1[2] + InCol2[0] + InCol2[1] - 2 * DOM + 0 >= 0)
        model.addConstr(InCol1[1] + InCol1[2] + 2 * InCol1[3] + 2 * InCol2[0] + InCol2[1] + InCol2[2] + 2 * InCol2[3] - 4 * DOM + 0 >= 0)
        model.addConstr(InCol1[1] + 2 * InCol1[2] + InCol2[0] + InCol2[2] + InCol2[3] - 2 * DOM + 0 >= 0)
        model.addConstr(InCol1[0] + 2 * InCol1[1] + InCol2[1] + InCol2[2] + InCol2[3] - 2 * DOM + 0 >= 0)
        model.addConstr(2 * InCol1[0] + InCol1[2] + InCol1[3] + InCol2[2] + InCol2[3] - 2 * DOM + 0 >= 0)
        model.addConstr(2 * InCol1[1] + InCol1[3] + InCol2[0] + InCol2[1] + InCol2[2] - 2 * DOM + 0 >= 0)
        model.addConstr(2 * InCol1[0] + InCol1[1] + 2 * InCol1[3] + InCol2[0] + 2 * InCol2[1] + InCol2[2] + InCol2[3] - 4 * DOM + 0 >= 0)
        model.addConstr(InCol1[1] + 2 * InCol1[2] + InCol1[3] + InCol2[1] + InCol2[3] - 2 * DOM + 0 >= 0)
        model.addConstr(InCol1[0] + InCol1[2] + 2 * InCol1[3] + InCol2[0] + InCol2[2] - 2 * DOM + 0 >= 0)
        model.addConstr(2 * InCol1[0] + 2 * InCol1[1] + InCol1[2] + InCol1[3] + 2 * InCol2[0] + InCol2[2] + InCol2[3] - 4 * DOM + 0 >= 0)
        model.addConstr(InCol1[0] + InCol1[2] + InCol2[0] + 2 * InCol2[1] + InCol2[2] - 2 * DOM + 0 >= 0)
        model.addConstr(InCol1[0] + InCol1[1] + 2 * InCol1[2] + InCol1[3] + InCol2[2] - 2 * DOM + 0 >= 0)
        model.addConstr(2 * InCol1[0] + InCol1[2] + InCol2[0] + InCol2[1] + InCol2[3] - 2 * DOM + 0 >= 0)
        model.addConstr(- InCol1[1] - InCol1[2] - InCol1[3] - InCol2[0] + DOM + 3 >= 0)
        model.addConstr(- InCol1[0] - InCol1[2] - InCol1[3] - InCol2[1] + DOM + 3 >= 0)
        model.addConstr(- InCol1[0] - InCol1[1] - InCol2[0] - InCol2[1] + DOM + 3 >= 0)
        model.addConstr(- InCol1[0] - InCol1[1] - InCol1[3] - InCol2[2] + DOM + 3 >= 0)
        model.addConstr(- InCol1[1] - InCol1[2] - InCol2[1] - InCol2[2] + DOM + 3 >= 0)
        model.addConstr(- InCol1[0] - InCol1[2] - InCol2[0] - InCol2[2] + DOM + 3 >= 0)
        model.addConstr(- InCol1[3] - InCol2[0] - InCol2[1] - InCol2[2] + DOM + 3 >= 0)
        model.addConstr(- InCol1[2] - InCol2[0] - InCol2[1] - InCol2[3] + DOM + 3 >= 0)
        model.addConstr(- InCol1[1] - InCol2[0] - InCol2[2] - InCol2[3] + DOM + 3 >= 0)
        model.addConstr(- InCol1[0] - InCol1[3] - InCol2[0] - InCol2[3] + DOM + 3 >= 0)
        model.addConstr(- InCol1[0] - InCol1[1] - InCol1[2] - InCol2[3] + DOM + 3 >= 0)
        model.addConstr(- InCol1[2] - InCol1[3] - InCol2[2] - InCol2[3] + DOM + 3 >= 0)
        model.addConstr(- InCol1[1] - InCol1[3] - InCol2[1] - InCol2[3] + DOM + 3 >= 0)
        model.addConstr(- InCol1[0] - InCol2[1] - InCol2[2] - InCol2[3] + DOM + 3 >= 0)
        model.addConstr(2 * InCol1[1] + InCol1[2] + InCol1[3] + 2 * InCol2[0] + 2 * InCol2[1] + InCol2[2] + InCol2[3] - 4 * DOM + 0 >= 0)
        model.addConstr(InCol1[1] + InCol1[3] + InCol2[2] + InCol2[3] - DOM + 0 >= 0)
        model.addConstr(InCol1[1] + InCol1[2] + InCol1[3] + InCol2[0] + 2 * InCol2[1] - 2 * DOM + 0 >= 0)

    @staticmethod
    def WhiterKey_Xor(Key1_1, Key1_2, Key2_1, Key2_2, IP_1, IP_2, OP_1, OP_2, CD_Blue, CD_Red, CD_Key_Blue, CD_Key_Red, model):
        model.addConstr(- Key1_2 - Key2_2 - IP_1 - IP_2 + OP_1 + OP_2 - 2 * CD_Blue - 2 * CD_Red - 3 * CD_Key_Blue - CD_Key_Red + 3 >= 0)
        model.addConstr(Key1_2 + Key2_2 + IP_1 + 2 * IP_2 + OP_1 - 2 * OP_2 + 2 * CD_Blue - CD_Red + 2 * CD_Key_Blue - 2 * CD_Key_Red - 2 >= 0)
        model.addConstr(Key1_1 + 2 * Key2_1 + Key2_2 + IP_1 - IP_2 - OP_1 + OP_2 - 3 * CD_Blue + CD_Red - 2 * CD_Key_Blue - 1 >= 0)
        model.addConstr(Key1_1 + Key2_1 + 2 * IP_1 + IP_2 - 2 * OP_1 + OP_2 + 2 * CD_Red - 2 * CD_Key_Blue + 2 * CD_Key_Red - 2 >= 0)
        model.addConstr(- Key1_1 - Key2_1 - IP_1 + OP_1 - 2 * CD_Red - 2 * CD_Key_Red + 2 >= 0)
        model.addConstr(Key1_1 + Key1_2 - 1 >= 0)
        model.addConstr(Key1_1 + 2 * Key2_1 + Key2_2 - IP_2 - OP_1 + OP_2 - 2 * CD_Blue + CD_Red - CD_Key_Blue + CD_Key_Red - 1 >= 0)
        model.addConstr(- 2 * Key1_2 - Key2_2 - IP_2 + OP_2 - 2 * CD_Blue - 3 * CD_Key_Blue + 3 >= 0)
        model.addConstr(Key1_2 - Key2_2 + IP_1 - OP_1 - OP_2 + CD_Red + 1 >= 0)
        model.addConstr(Key2_2 - OP_2 + CD_Blue + CD_Key_Blue >= 0)
        model.addConstr(Key1_1 - Key2_2 + IP_2 - OP_1 - OP_2 + CD_Red - CD_Key_Blue + CD_Key_Red + 1 >= 0)
        model.addConstr(IP_1 + IP_2 - 1 >= 0)
        model.addConstr(Key2_1 - OP_1 + CD_Red + CD_Key_Red >= 0)
        model.addConstr(Key1_2 - OP_2 + CD_Blue + CD_Key_Blue >= 0)
        model.addConstr(- Key1_1 + Key2_2 + IP_2 + OP_1 - OP_2 + CD_Blue - CD_Red + CD_Key_Blue - 2 * CD_Key_Red >= 0)


def column(A, j):
    return [A[j], A[j + 4], A[j + 8], A[j + 12]]


def ShuffleCell(A):
    return [A[0], A[11], A[6], A[13], A[10], A[1], A[12], A[7], A[5], A[14], A[3], A[8], A[15], A[4], A[9], A[2]]


def ShuffleCell_Inv(A):
    return [A[0], A[5], A[15], A[10], A[13], A[8], A[2], A[7], A[11], A[14], A[4], A[1], A[6], A[3], A[9], A[12]]


# if __name__ == '__main__':
    # for Coli in range(ColN):
    #     for RoWi in range(RowN):
    #         res = [i for i in range(ColN) if MC[RoWi][i] == 1]
    #         print(res)
    # A = [i for i in range(bs)]
    # print(ShuffleCell_Inv(ShuffleCell(A)))
