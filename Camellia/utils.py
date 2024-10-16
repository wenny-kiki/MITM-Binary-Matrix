

from Configration import *


class BasicTools:
    @staticmethod
    def plusTerms(in_vars):
        """
        >>> BasicTools.plusTerms(['x', 'y', 'z'])
        'x + y + z'
        >>> BasicTools.plusTerms(['x', 'y'])
        'x + y'
        >>> BasicTools.plusTerms(['x', 'y', 'z', 'a', 'b'])
        'x + y + z + a + b'
        >>>
        """
        t = ''
        for v in in_vars:
            t = t + v + ' + '
        return t[0:-3]

    @staticmethod
    def minusTerms(in_vars):
        """
        >>> BasicTools.minusTerms(['x', 'y', 'z'])
        'x - y - z'
        >>> BasicTools.minusTerms(['x', 'y'])
        'x - y'
        >>> BasicTools.minusTerms(['x', 'y', 'z', 'a', 'b'])
        'x - y - z - a - b'
        >>>
        """
        t = ''
        for v in in_vars:
            t = t + v + ' - '
        return t[0:-3]

    @staticmethod
    def getVariables_From_Constraints(C):
        V = set([])
        for s in C:
            temp = s.strip()
            temp = temp.replace(' + ', '   ')
            temp = temp.replace(' - ', '   ')
            temp = temp.replace(' >= ', '   ')
            temp = temp.replace(' <= ', '   ')
            temp = temp.replace(' = ', '   ')
            temp = temp.replace(' -> ', '   ')
            temp = temp.replace(' AND ', '     ')
            temp = temp.replace(' OR ', '    ')
            temp = temp.replace(' MAX ', '     ')
            temp = temp.replace(' MIN ', '     ')
            temp = temp.replace(' , ', '   ')
            temp = temp.replace(' ( ', '   ')
            temp = temp.replace(' ) ', '   ')
            temp = temp.split()
            for v in temp:
                if not v.lstrip('-').isdecimal():
                    V.add(v)
        return V

    @staticmethod
    def AND(V_in, V_out):
        # (0, 0) -> 0, (0, 1) -> 0, (1, 0) -> 0, (1, 1) -> 1
        m = len(V_in)
        constr = []
        constr = constr + [V_out + ' - ' + BasicTools.minusTerms(V_in) + ' >= ' + str(1 - m)]
        constr = constr + [BasicTools.plusTerms(V_in) + ' - ' + str(m) + ' ' + V_out + ' >= 0']
        return constr

    @staticmethod
    def OR_(V_in, V_out):
        # (0, 0) -> 0, (0, 1) -> 1, (1, 0) -> 1, (1, 1) -> 1
        m = len(V_in)
        constr = []
        constr = constr + [str(m) + ' ' + V_out + ' - ' + BasicTools.minusTerms(V_in) + ' >= 0']
        constr = constr + [V_out + ' - ' + BasicTools.minusTerms(V_in) + ' <= 0']
        return constr

    @staticmethod
    def N_AND(V_in, V_out):
        # (0, 0) -> 1, (0, 1) -> 1, (1, 0) -> 1, (1, 1) -> 0
        m = len(V_in)
        constr = []
        constr = constr + [V_out + ' + ' + BasicTools.plusTerms(V_in) + ' <= ' + str(m)]
        constr = constr + [BasicTools.plusTerms(V_in) + ' + ' + str(m) + ' ' + V_out + ' >= ' + str(m)]
        return constr

    @staticmethod
    def N_OR_(V_in, V_out):
        # (0, 0) -> 1, (0, 1) -> 0, (1, 0) -> 0, (1, 1) -> 0
        m = len(V_in)
        constr = []
        if m != 0:
            constr = constr + [V_out + ' + ' + BasicTools.plusTerms(V_in) + ' >= 1']
            for j in range(m):
                constr = constr + [V_in[j] + ' + ' + V_out + ' <= 1']
        elif m == 0:
            constr = constr + [V_out + ' >= 1']
        return constr


class MITMPreConstraints:
    @staticmethod
    def equalConstraints(x, y):
        assert len(x) == len(y)
        cons = []
        for i in range(len(x)):
            cons = cons + [x[i] + ' - ' + y[i] + ' = 0']
        return cons

    @staticmethod
    def Determine_Allone(V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [V_out + ' - ' + BasicTools.minusTerms(V_in) + ' >= ' + str(1 - m)]
        constr = constr + [BasicTools.plusTerms(V_in) + ' - ' + str(m) + ' ' + V_out + ' >= 0']
        return constr

    @staticmethod
    def Determine_Allzero(V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [V_out + ' + ' + BasicTools.plusTerms(V_in) + ' >= 1']
        for j in range(m):
            constr = constr + [V_in[j] + ' + ' + V_out + ' <= 1']
        return constr

    @staticmethod
    def Determine_ExistOne(V_in, V_out):
        m = len(V_in)
        constr = []
        constr = constr + [str(m) + ' ' + V_out + ' - ' + BasicTools.minusTerms(V_in) + ' >= 0']
        constr = constr + [V_out + ' - ' + BasicTools.minusTerms(V_in) + ' <= 0']
        return constr

    @staticmethod
    def Determine_Merge_isWhite(InBlue_1, InBlue_2, InRed_1, InRed_2, isWhite):
        cons = []
        cons = cons + [InBlue_2 + ' + ' + InRed_1 + ' + ' + isWhite + ' <= 2']
        cons = cons + [InBlue_1 + ' + ' + InRed_1 + ' + ' + isWhite + ' <= 2']
        cons = cons + [InBlue_2 + ' + ' + InRed_2 + ' + ' + isWhite + ' <= 2']
        cons = cons + [InBlue_1 + ' + ' + InRed_2 + ' + ' + isWhite + ' <= 2']
        cons = cons + [InBlue_1 + ' + ' + InBlue_2 + ' + ' + isWhite + ' >= 1']
        cons = cons + [InRed_1 + ' + ' + InRed_2 + ' + ' + isWhite + ' >= 1']
        return cons

    @staticmethod
    def Xor_no_Comsume(in1, in2, out):
        cons = []
        cons = cons + [in1[0] + ' - ' + out[0] + ' >= 0']
        cons = cons + [in1[1] + ' - ' + out[1] + ' >= 0']
        cons = cons + [in2[0] + ' - ' + out[0] + ' >= 0']
        cons = cons + [in2[1] + ' - ' + out[1] + ' >= 0']
        cons = cons + [in1[0] + ' + ' + in2[0] + ' - ' + out[0] + ' <= 1']
        cons = cons + [in1[1] + ' + ' + in2[1] + ' - ' + out[1] + ' <= 1']
        return cons

    @staticmethod
    def Separate_Without_Guess_i(
            In_1_i,
            In_2_i,
            SupP_Blue_1_i,
            SupP_Blue_2_i,
            SupP_Red__1_i,
            SupP_Red__2_i,
            In_isWhite_i
    ):
        cons = []
        cons = cons + BasicTools.N_OR_([In_1_i, In_2_i], In_isWhite_i)
        cons = cons + [SupP_Blue_1_i + ' + ' + In_isWhite_i + ' = 1']
        cons = cons + [SupP_Blue_2_i + ' - ' + In_2_i + ' = 0']
        cons = cons + [SupP_Red__2_i + ' - ' + SupP_Blue_1_i + ' = 0']
        cons = cons + [SupP_Red__1_i + ' - ' + In_1_i + ' = 0']
        return cons

    @staticmethod
    def Separate_With_Guess_i(
            In_1_i,
            In_2_i,
            SupP_Blue_1_i,
            SupP_Blue_2_i,
            SupP_Red__1_i,
            SupP_Red__2_i,
            In_isWhite_i,
            GuessBlue_i,
            GuessRed__i,
            GuessBoth_i
    ):
        cons = []
        cons = cons + BasicTools.N_OR_([In_1_i, In_2_i], In_isWhite_i)
        cons = cons + [GuessBlue_i + ' + ' + GuessRed__i + ' + ' + GuessBoth_i + ' - ' + In_isWhite_i + ' <= 0']
        cons = cons + [
            SupP_Blue_1_i + ' - ' + GuessBlue_i + ' - ' + GuessRed__i + ' - ' + GuessBoth_i + ' + ' + In_isWhite_i + ' = 1']
        cons = cons + [SupP_Blue_2_i + ' - ' + In_2_i + ' - ' + GuessRed__i + ' = 0']
        cons = cons + [SupP_Red__2_i + ' - ' + SupP_Blue_1_i + ' = 0']
        cons = cons + [SupP_Red__1_i + ' - ' + In_1_i + ' - ' + GuessBlue_i + ' = 0']
        return cons

    @staticmethod
    def genSubConstraints_MC_SupP__Blue(
            I_MC_SupP_Blue_1_coli,
            I_MC_SupP_Blue_2_coli,
            I_MC_SupP_Blue_ColExistWhite_coli,
            I_MC_SupP_Blue_ColAllGray_coli,
            O_MC_SupP_Blue_1_coli,
            O_MC_SupP_Blue_2_coli,
            G_SupP_Blue_SumGray_coli,
            G_CD_MC_Blue_coli
    ):
        cons = []
        cons = cons + BasicTools.N_AND(I_MC_SupP_Blue_1_coli, I_MC_SupP_Blue_ColExistWhite_coli)
        cons = cons + BasicTools.AND(I_MC_SupP_Blue_2_coli, I_MC_SupP_Blue_ColAllGray_coli)
        cons = cons + [BasicTools.plusTerms(O_MC_SupP_Blue_1_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Blue_ColExistWhite_coli + ' = ' + str(RowN)]
        cons = cons + [BasicTools.plusTerms(O_MC_SupP_Blue_2_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Blue_ColExistWhite_coli + ' <= ' + str(RowN)]
        cons = cons + [G_SupP_Blue_SumGray_coli + ' - ' + BasicTools.minusTerms(I_MC_SupP_Blue_2_coli) + ' - ' + BasicTools.minusTerms(O_MC_SupP_Blue_2_coli) + ' = 0']
        cons = cons + [G_SupP_Blue_SumGray_coli + ' - ' + str(BranchN) + ' ' + I_MC_SupP_Blue_ColAllGray_coli + ' <= ' + str(SumIOMC - BranchN)]
        cons = cons + [G_SupP_Blue_SumGray_coli + ' - ' + str(SumIOMC) + ' ' + I_MC_SupP_Blue_ColAllGray_coli + ' >= 0']
        cons = cons + [G_CD_MC_Blue_coli + ' - ' + BasicTools.minusTerms(O_MC_SupP_Blue_2_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Blue_ColAllGray_coli + ' = 0']
        return cons

    @staticmethod
    def genSubConstraints_MC_SupP__Red(
            I_MC_SupP_Red__1_coli,
            I_MC_SupP_Red__2_coli,
            I_MC_SupP_Red__ColExistWhite_coli,
            I_MC_SupP_Red__ColAllGray_coli,
            O_MC_SupP_Red__1_coli,
            O_MC_SupP_Red__2_coli,
            G_SupP_Red__SumGray_coli,
            G_CD_MC_Red__coli
    ):
        cons = []
        cons = cons + BasicTools.N_AND(I_MC_SupP_Red__2_coli, I_MC_SupP_Red__ColExistWhite_coli)
        cons = cons + BasicTools.AND(I_MC_SupP_Red__1_coli, I_MC_SupP_Red__ColAllGray_coli)
        cons = cons + [BasicTools.plusTerms(O_MC_SupP_Red__2_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Red__ColExistWhite_coli + ' = ' + str(RowN)]
        cons = cons + [BasicTools.plusTerms(O_MC_SupP_Red__1_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Red__ColExistWhite_coli + ' <= ' + str(RowN)]
        cons = cons + [G_SupP_Red__SumGray_coli + ' - ' + BasicTools.minusTerms(I_MC_SupP_Red__1_coli) + ' - ' + BasicTools.minusTerms(O_MC_SupP_Red__1_coli) + ' = 0']
        cons = cons + [G_SupP_Red__SumGray_coli + ' - ' + str(BranchN) + ' ' + I_MC_SupP_Red__ColAllGray_coli + ' <= ' + str(SumIOMC - BranchN)]
        cons = cons + [G_SupP_Red__SumGray_coli + ' - ' + str(SumIOMC) + ' ' + I_MC_SupP_Red__ColAllGray_coli + ' >= 0']
        cons = cons + [G_CD_MC_Red__coli + ' - ' + BasicTools.minusTerms(O_MC_SupP_Red__1_coli) + ' + ' + str(RowN) + ' ' + I_MC_SupP_Red__ColAllGray_coli + ' = 0']
        return cons

    @staticmethod
    def genConstraints_of_nXor_SupP_Blue_i(
            IP_SupP_Blue_1,
            IP_SupP_Blue_2,
            OP_SupP_Blue_1_i,
            OP_SupP_Blue_2_i,
            CD_XOR_Blue_i,
            SumGary_SupP_Blue,
            OP_isWhite_i,
            OP_SupP_Blue_AND_2_i,
    ):
        cons = []
        n = len(IP_SupP_Blue_1) + 1
        cons = cons + BasicTools.N_AND(IP_SupP_Blue_1, OP_isWhite_i)

        cons = cons + BasicTools.AND(IP_SupP_Blue_2, OP_SupP_Blue_AND_2_i)
        cons = cons + [OP_SupP_Blue_1_i + ' + ' + OP_isWhite_i + ' = 1']
        cons = cons + [OP_SupP_Blue_2_i + ' + ' + OP_isWhite_i + ' <= 1']
        cons = cons + [CD_XOR_Blue_i + ' - ' + OP_SupP_Blue_2_i + ' + ' + OP_SupP_Blue_AND_2_i + ' = 0']
        cons = cons + [SumGary_SupP_Blue + ' - ' + BasicTools.minusTerms(IP_SupP_Blue_2) + ' - ' + OP_SupP_Blue_2_i + ' = 0']
        cons = cons + [SumGary_SupP_Blue + ' - 2 ' + OP_SupP_Blue_AND_2_i + ' <= ' + str(n - 2)]
        cons = cons + [SumGary_SupP_Blue + ' - ' + str(n) + ' ' + OP_SupP_Blue_AND_2_i + ' >= 0']
        return cons

    @staticmethod
    def genConstraints_of_nXor_SupP_Red_i(
            IP_SupP_Red_1,
            IP_SupP_Red_2,
            OP_SupP_Red_1_i,
            OP_SupP_Red_2_i,
            CD_XOR_Red_i,
            SumGary_SupP_Red,
            OP_isWhite_i,
            OP_SupP_Red__AND_1_i
    ):
        cons = []
        n = len(IP_SupP_Red_1) + 1
        cons = cons + BasicTools.N_AND(IP_SupP_Red_2, OP_isWhite_i)
        cons = cons + BasicTools.AND(IP_SupP_Red_1, OP_SupP_Red__AND_1_i)
        cons = cons + [OP_SupP_Red_2_i + ' + ' + OP_isWhite_i + ' = 1']
        cons = cons + [OP_SupP_Red_1_i + ' + ' + OP_isWhite_i + ' <= 1']
        cons = cons + [CD_XOR_Red_i + ' - ' + OP_SupP_Red_1_i + ' + ' + OP_SupP_Red__AND_1_i + ' = 0']
        cons = cons + [SumGary_SupP_Red + ' - ' + BasicTools.minusTerms(IP_SupP_Red_1) + ' - ' + OP_SupP_Red_1_i + ' = 0']
        cons = cons + [SumGary_SupP_Red + ' - 2 ' + OP_SupP_Red__AND_1_i + ' <= ' + str(n - 2)]
        cons = cons + [SumGary_SupP_Red + ' - ' + str(n) + ' ' + OP_SupP_Red__AND_1_i + ' >= 0']
        return cons

    @staticmethod
    def genConstrains_of_Xor_i(
            IP1_SupP_Blue_1_i,
            IP1_SupP_Blue_2_i,
            IP1_SupP_Red_1_i,
            IP1_SupP_Red_2_i,
            IP2_SupP_Blue_1_i,
            IP2_SupP_Blue_2_i,
            IP2_SupP_Red_1_i,
            IP2_SupP_Red_2_i,
            OP_SupP_Blue_1_i,
            OP_SupP_Blue_2_i,
            OP_SupP_Red_1_i,
            OP_SupP_Red_2_i,
            CD_XOR_Blue_i,
            CD_XOR_Red_i,
            OP_isWhite_i,
            OP_SupP_Blue_AND_1_i,
            OP_SupP_Blue_AND_2_i,
            OP_SupP_Blue_OR__1_i,
            OP_SupP_Blue_OR__2_i,
            OP_SupP_Red__AND_1_i,
            OP_SupP_Red__AND_2_i,
            OP_SupP_Red__OR__1_i,
            OP_SupP_Red__OR__2_i
    ):
        cons = []
        cons = cons + BasicTools.N_AND([IP1_SupP_Blue_1_i, IP2_SupP_Blue_1_i], OP_isWhite_i)

        cons = cons + BasicTools.AND([IP1_SupP_Blue_2_i, IP2_SupP_Blue_2_i], OP_SupP_Blue_AND_2_i)
        cons = cons + BasicTools.OR_([IP1_SupP_Blue_2_i, IP2_SupP_Blue_2_i], OP_SupP_Blue_OR__2_i)
        cons = cons + [CD_XOR_Blue_i + ' + ' + OP_SupP_Blue_OR__2_i + ' <= 1']
        cons = cons + [CD_XOR_Blue_i + ' + ' + OP_isWhite_i + ' <= 1']
        cons = cons + [OP_SupP_Blue_1_i + ' + ' + OP_isWhite_i + ' = 1']
        cons = cons + [OP_SupP_Blue_2_i + ' - ' + OP_SupP_Blue_AND_2_i + ' - ' + CD_XOR_Blue_i + ' = 0']

        cons = cons + BasicTools.AND([IP1_SupP_Red_1_i, IP2_SupP_Red_1_i], OP_SupP_Red__AND_1_i)
        cons = cons + BasicTools.OR_([IP1_SupP_Red_1_i, IP2_SupP_Red_1_i], OP_SupP_Red__OR__1_i)
        cons = cons + [CD_XOR_Red_i + ' + ' + OP_SupP_Red__OR__1_i + ' <= 1']
        cons = cons + [CD_XOR_Red_i + ' + ' + OP_isWhite_i + ' <= 1']
        cons = cons + [OP_SupP_Red_2_i + ' + ' + OP_isWhite_i + ' = 1']
        cons = cons + [OP_SupP_Red_1_i + ' - ' + OP_SupP_Red__AND_1_i + ' - ' + CD_XOR_Red_i + ' = 0']
        return cons

    @staticmethod
    def Match_direct_double_color(x, y, m):
        c = []
        c = c + [x[0] + ' + ' + x[1] + ' + ' + m + ' <= 2']
        c = c + [y[0] + ' + ' + y[1] + ' + ' + m + ' <= 2']
        c = c + [x[0] + ' + ' + x[1] + ' - ' + m + ' >= 0']
        c = c + [x[0] + ' + ' + y[0] + ' - ' + m + ' >= 0']
        c = c + [x[1] + ' + ' + y[1] + ' - ' + m + ' >= 0']
        c = c + [x[0] + ' - ' + x[1] + ' - ' + y[0] + ' + ' + y[1] + ' - ' + m + ' <= 1']
        c = c + [x[1] + ' - ' + x[0] + ' + ' + y[0] + ' - ' + y[1] + ' - ' + m + ' <= 1']
        return c

    # @staticmethod
    # def Match_indirect():


def ShiftRow(A):
    return [A[0], A[1], A[2], A[3],
            A[5], A[6], A[7], A[4],
            A[10], A[11], A[8], A[9],
            A[15], A[12], A[13], A[14]]


def ShiftRow_Inv(A):
    return [A[0], A[1], A[2], A[3],
            A[7], A[4], A[5], A[6],
            A[10], A[11], A[8], A[9],
            A[13], A[14], A[15], A[12]]


def column(A, j):
    return [A[j + ColN * i] for i in range(RowN)]


def Perm_Camellia(Rowi, A):
    Martix = [
        [1, 0, 1, 1, 0, 1, 1, 1],
        [1, 1, 0, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 1, 0, 1, 0, 1, 1],
        [0, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 1, 1, 1, 0]
    ]
    return [A[i] for i in range(bs) if Martix[Rowi][i] == 1]


def match_rounds(TR, ini_r, mat_r):
    match_rounds = [[], []]
    if TR % 2 == 0:
        if ini_r <= mat_r:
            for r in range(ini_r, mat_r + 1):
                if (mat_r - r) % 2 == 0:
                    match_rounds[0].append(r)
                else:
                    match_rounds[1].append(r)
            for r in range(mat_r + 1, TR - 2):
                if (r - mat_r - 1) % 2 == 0:
                    match_rounds[1].append(r)
                else:
                    match_rounds[0].append(r)
            if mat_r % 2 == 0:
                for r in range(2, ini_r):
                    if (ini_r - r) % 2 == 0:
                        match_rounds[1].append(r)
                    else:
                        match_rounds[0].append(r)
            else:
                for r in range(2, ini_r):
                    if (ini_r - r) % 2 == 0:
                        match_rounds[0].append(r)
                    else:
                        match_rounds[1].append(r)
        else:
            for r in range(mat_r + 1, ini_r):
                if (r - mat_r - 1) % 2 == 0:
                    match_rounds[1].append(r)
                else:
                    match_rounds[0].append(r)
            for r in range(2, mat_r + 1):
                if (mat_r - r) % 2 == 0:
                    match_rounds[0].append(r)
                else:
                    match_rounds[1].append(r)
            if mat_r % 2 == 0:
                for r in range(ini_r, TR - 2):
                    if (TR - 2 - r) % 2 == 0:
                        match_rounds[1].append(r)
                    else:
                        match_rounds[0].append(r)
            else:
                for r in range(ini_r, TR - 2):
                    if (TR - r) % 2 == 0:
                        match_rounds[0].append(r)
                    else:
                        match_rounds[1].append(r)
    else:
        if mat_r % 2 == 0:
            for r in range(2, TR - 2):
                if r % 2 == 0:
                    match_rounds[0].append(r)
                else:
                    match_rounds[1].append(r)
        else:
            for r in range(2, TR - 2):
                if r % 2 == 0:
                    match_rounds[1].append(r)
                else:
                    match_rounds[0].append(r)
    return match_rounds



















