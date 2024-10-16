
from utils import *
from gurobipy import *


class Vars_generator:
    # - Input
    @staticmethod
    def genVars_Input_of_Round(i, r):
        return [f'IP_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Blue_Input_of_Round(i, r):
        return [f'IP_SupP_Blue_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_Input_of_Round(i, r):
        return [f'IP_SupP_Red_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Input_of_isWhite(r):
        return [f'IP_isWhite_r{r}_{j}' for j in range(bs)]

    # - MixColumns
    @staticmethod
    def genVars_SupP_Blue_Output_of_MixColumns(i, r):
        return [f'OMC_SupP_Blue_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_Output_of_MixColumns(i, r):
        return [f'OMC_SupP_Red_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Blue_ColExistWhite(r):
        return [f'MC_SupP_Blue_ColExistWhite_r{r}_{i}' for i in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Red_ColExistWhite(r):
        return [f'MC_SupP_Red_ColExistWhite_r{r}_{i}' for i in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Blue_ColAllGray(r):
        return [f'MC_SupP_Blue_ColAllGray_r{r}_{i}' for i in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Red_ColAllGray(r):
        return [f'MC_SupP_Red_ColAllGray_r{r}_{i}' for i in range(bs)]

    @staticmethod
    def genVars_MC_ConsumedDeg_Blue(r):
        return [f'CD_MC_Blue_r{r}_{i}' for i in range(bs)]

    @staticmethod
    def genVars_MC_ConsumedDeg_Red(r):
        return [f'CD_MC_Red_r{r}_{i}' for i in range(bs)]

    # Initial Degree
    @staticmethod
    def genVars_degree_forward():
        return ['deg_f_' + str(j) for j in range(bs * b)]

    @staticmethod
    def genVars_degree_backward():
        return ['deg_b_' + str(j) for j in range(bs * b)]

    # Match
    @staticmethod
    def genVars_Match_IsWhite(r):
        return  [f'Match_IW_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Match_Exist(r):
        return [f'Match_Ex_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Match(r):
        return [f'Match_r{r}_{j}' for j in range(bs)]

class Constraints_generator:
    def __init__(self, total_round, initial_round, matching_round):
        self.ini_r = initial_round
        self.mat_r = matching_round
        self.TR = total_round

    def genConstraints_initial_degree(self):
        cons = []
        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()

        IP_1 = Vars_generator.genVars_Input_of_Round(1, self.ini_r)
        IP_2 = Vars_generator.genVars_Input_of_Round(2, self.ini_r)

        for bi in range(bs * b):
            cons = cons + [IP_1[bi] + ' + ' + IP_2[bi] + ' >= 1']
            cons = cons + [d1[bi] + ' + ' + IP_2[bi] + ' = 1']
            cons = cons + [d2[bi] + ' + ' + IP_1[bi] + ' = 1']

        return cons

    def genConstraints_forward_round(self, r):
        cons = []

        IP_1 = Vars_generator.genVars_Input_of_Round(1, r)
        IP_2 = Vars_generator.genVars_Input_of_Round(2, r)

        if r == self.TR - 1:
            OP_1 = Vars_generator.genVars_Input_of_Round(1, 0)
            OP_2 = Vars_generator.genVars_Input_of_Round(2, 0)
            cons = cons + MITMPreConstraints.equalConstraints(IP_1, OP_1)
            cons = cons + MITMPreConstraints.equalConstraints(IP_2, OP_2)
            return cons

        IP_SupP_Blue_1 = Vars_generator.genVars_SupP_Blue_Input_of_Round(1, r)
        IP_SupP_Blue_2 = Vars_generator.genVars_SupP_Blue_Input_of_Round(2, r)
        IP_SupP_Red_1 = Vars_generator.genVars_SupP_Red_Input_of_Round(1, r)
        IP_SupP_Red_2 = Vars_generator.genVars_SupP_Red_Input_of_Round(2, r)
        IP_isWhite = Vars_generator.genVars_Input_of_isWhite(r)

        OMC_SupP_Blue_1 = Vars_generator.genVars_SupP_Blue_Output_of_MixColumns(1, r)
        OMC_SupP_Blue_2 = Vars_generator.genVars_SupP_Blue_Output_of_MixColumns(2, r)
        OMC_SupP_Red_1 = Vars_generator.genVars_SupP_Red_Output_of_MixColumns(1, r)
        OMC_SupP_Red_2 = Vars_generator.genVars_SupP_Red_Output_of_MixColumns(2, r)

        OP_1 = Vars_generator.genVars_Input_of_Round(1, r + 1)
        OP_2 = Vars_generator.genVars_Input_of_Round(2, r + 1)

        for bi in range(bs):
            cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                IP_1[bi],
                IP_2[bi],
                IP_SupP_Blue_1[bi],
                IP_SupP_Blue_2[bi],
                IP_SupP_Red_1[bi],
                IP_SupP_Red_2[bi],
                IP_isWhite[bi]
            )

        IMC_SupP_Blue_ColExistWhite = Vars_generator.genVars_MC_SupP_Blue_ColExistWhite(r)
        IMC_SupP_Red_ColExistWhite = Vars_generator.genVars_MC_SupP_Red_ColExistWhite(r)
        IMC_SupP_Blue_ColAllGray = Vars_generator.genVars_MC_SupP_Blue_ColAllGray(r)
        IMC_SupP_Red_ColAllGray = Vars_generator.genVars_MC_SupP_Red_ColAllGray(r)
        CD_Blue = Vars_generator.genVars_MC_ConsumedDeg_Blue(r)
        CD_Red = Vars_generator.genVars_MC_ConsumedDeg_Red(r)

        cons = cons + MITMPreConstraints.genSubConstraints_7Xor_SupP_Blue(
            IP_SupP_Blue_1,
            IP_SupP_Blue_2,
            IMC_SupP_Blue_ColExistWhite,
            IMC_SupP_Blue_ColAllGray,
            OMC_SupP_Blue_1,
            OMC_SupP_Blue_2,
            CD_Blue
        )
        cons = cons + MITMPreConstraints.genSubConstraints_7Xor_SupP_Red(
            IP_SupP_Red_1,
            IP_SupP_Red_2,
            IMC_SupP_Red_ColExistWhite,
            IMC_SupP_Red_ColAllGray,
            OMC_SupP_Red_1,
            OMC_SupP_Red_2,
            CD_Red
        )

        cons = cons + [BasicTools.plusTerms(CD_Blue) + ' <= 15']
        cons = cons + [BasicTools.plusTerms(CD_Red) + ' <= 15']

        for bi in range(bs):
            cons = cons + MITMPreConstraints.Determine_Allone([OMC_SupP_Blue_1[bi],OMC_SupP_Red_1[bi]],OP_1[bi])
            cons = cons + MITMPreConstraints.Determine_Allone([OMC_SupP_Blue_2[bi], OMC_SupP_Red_2[bi]],
                                                              OP_2[bi])

        return cons

    def genConstraints_backward_round(self, r):
        cons = []

        OP_1 = Vars_generator.genVars_Input_of_Round(1, r)
        OP_2 = Vars_generator.genVars_Input_of_Round(2, r)

        if r == self.TR - 1:
            IP_1 = Vars_generator.genVars_Input_of_Round(1, 0)
            IP_2 = Vars_generator.genVars_Input_of_Round(2, 0)
            cons = cons + MITMPreConstraints.equalConstraints(IP_1, OP_1)
            cons = cons + MITMPreConstraints.equalConstraints(IP_2, OP_2)
            return cons

        IP_SupP_Blue_1 = Vars_generator.genVars_SupP_Blue_Input_of_Round(1, r)
        IP_SupP_Blue_2 = Vars_generator.genVars_SupP_Blue_Input_of_Round(2, r)
        IP_SupP_Red_1 = Vars_generator.genVars_SupP_Red_Input_of_Round(1, r)
        IP_SupP_Red_2 = Vars_generator.genVars_SupP_Red_Input_of_Round(2, r)
        IP_isWhite = Vars_generator.genVars_Input_of_isWhite(r)

        OMC_SupP_Blue_1 = Vars_generator.genVars_SupP_Blue_Output_of_MixColumns(1, r)
        OMC_SupP_Blue_2 = Vars_generator.genVars_SupP_Blue_Output_of_MixColumns(2, r)
        OMC_SupP_Red_1 = Vars_generator.genVars_SupP_Red_Output_of_MixColumns(1, r)
        OMC_SupP_Red_2 = Vars_generator.genVars_SupP_Red_Output_of_MixColumns(2, r)

        IP_1 = Vars_generator.genVars_Input_of_Round(1, r + 1)
        IP_2 = Vars_generator.genVars_Input_of_Round(2, r + 1)

        for bi in range(bs):
            cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                IP_1[bi],
                IP_2[bi],
                IP_SupP_Blue_1[bi],
                IP_SupP_Blue_2[bi],
                IP_SupP_Red_1[bi],
                IP_SupP_Red_2[bi],
                IP_isWhite[bi]
            )

        IMC_SupP_Blue_ColExistWhite = Vars_generator.genVars_MC_SupP_Blue_ColExistWhite(r)
        IMC_SupP_Red_ColExistWhite = Vars_generator.genVars_MC_SupP_Red_ColExistWhite(r)
        IMC_SupP_Blue_ColAllGray = Vars_generator.genVars_MC_SupP_Blue_ColAllGray(r)
        IMC_SupP_Red_ColAllGray = Vars_generator.genVars_MC_SupP_Red_ColAllGray(r)
        CD_Blue = Vars_generator.genVars_MC_ConsumedDeg_Blue(r)
        CD_Red = Vars_generator.genVars_MC_ConsumedDeg_Red(r)

        cons = cons + MITMPreConstraints.genSubConstraints_7Xor_SupP_Blue(
            IP_SupP_Blue_1,
            IP_SupP_Blue_2,
            IMC_SupP_Blue_ColExistWhite,
            IMC_SupP_Blue_ColAllGray,
            OMC_SupP_Blue_1,
            OMC_SupP_Blue_2,
            CD_Blue
        )
        cons = cons + MITMPreConstraints.genSubConstraints_7Xor_SupP_Red(
            IP_SupP_Red_1,
            IP_SupP_Red_2,
            IMC_SupP_Red_ColExistWhite,
            IMC_SupP_Red_ColAllGray,
            OMC_SupP_Red_1,
            OMC_SupP_Red_2,
            CD_Red
        )

        cons = cons + [BasicTools.plusTerms(CD_Blue) + ' <= 15']
        cons = cons + [BasicTools.plusTerms(CD_Red) + ' <= 15']

        for bi in range(bs):
            cons = cons + MITMPreConstraints.Determine_Allone([OMC_SupP_Blue_1[bi], OMC_SupP_Red_1[bi]], OP_1[bi])
            cons = cons + MITMPreConstraints.Determine_Allone([OMC_SupP_Blue_2[bi], OMC_SupP_Red_2[bi]],
                                                              OP_2[bi])

        return cons

    def genConstraints_Match(self):
        cons = []

        r = self.mat_r
        next_r = (self.mat_r + 1) % self.TR

        IP_r_1 = Vars_generator.genVars_Input_of_Round(1, r)
        IP_r_2 = Vars_generator.genVars_Input_of_Round(2, r)
        IP_next_r_1 = Vars_generator.genVars_Input_of_Round(1, next_r)
        IP_next_r_2 = Vars_generator.genVars_Input_of_Round(2, next_r)
        IW_r = Vars_generator.genVars_Match_IsWhite(r)
        IW_next_r = Vars_generator.genVars_Match_IsWhite(next_r)

        for bi in range(bs):
            cons = cons + MITMPreConstraints.Determine_Allzero([IP_r_1[bi], IP_r_2[bi]], IW_r[bi])
            cons = cons + MITMPreConstraints.Determine_Allzero([IP_next_r_1[bi], IP_next_r_2[bi]], IW_next_r[bi])

        Exist_r = Vars_generator.genVars_Match_Exist(r)
        Exist_next_r = Vars_generator.genVars_Match_Exist(next_r)
        Match_r = Vars_generator.genVars_Match(r)
        Match_next_r = Vars_generator.genVars_Match(next_r)
        for Ri in range(RowN):
            sum_IW_r = []
            sum_IW_next_r = []
            sum_r = []
            sum_next_r = []
            for i in P[Ri]:
                sum_IW_r = sum_IW_r + [IW_r[i]]
                sum_IW_next_r = sum_IW_next_r + [IW_next_r[i]]
                sum_r = sum_r + [Match_r[i]]
                sum_next_r = sum_next_r + [Match_next_r[i]]
            sum_IW_r = sum_IW_r + [IW_next_r[Ri]]
            sum_IW_next_r = sum_IW_next_r + [IW_r[Ri]]
            cons = cons + MITMPreConstraints.Determine_Allzero(sum_IW_r, Exist_r[Ri])
            cons = cons + MITMPreConstraints.Determine_Allzero(sum_IW_next_r, Exist_next_r[Ri])
            cons = cons + [BasicTools.plusTerms(sum_r) + ' - ' + Exist_r[Ri] + ' >= 0']
            cons = cons + [BasicTools.plusTerms(sum_next_r) + ' - ' + Exist_next_r[Ri] + ' >= 0']
        cons = cons + [BasicTools.plusTerms(Match_r) + ' - ' + BasicTools.minusTerms(Exist_r) + ' = 0']
        cons = cons + [BasicTools.plusTerms(Match_next_r) + ' - ' + BasicTools.plusTerms(Exist_next_r) + ' = 0']

        M = Vars_generator.genVars_Match('final')
        for bi in range(bs):
            cons = cons + MITMPreConstraints.Determine_ExistOne([Match_r[bi], Match_next_r[bi]], M[bi])

        GMat = 'GMat'
        cons = cons + [GMat + ' - ' + BasicTools.minusTerms(M) + ' = 0']
        cons = cons + ['GMat >= 1']

        return cons

    def genConstraints_additional(self):
        cons = []
        CD_Blue = []
        CD_Red = []

        for r in range(0, self.TR-1):
            if r != self.mat_r:
                CD_Blue = CD_Blue + Vars_generator.genVars_MC_ConsumedDeg_Blue(r)
                CD_Red = CD_Red + Vars_generator.genVars_MC_ConsumedDeg_Red(r)

        d1 = Vars_generator.genVars_degree_forward()
        d2 = Vars_generator.genVars_degree_backward()

        Deg1 = 'GDeg1'
        Deg2 = 'GDeg2'

        if len(CD_Blue) > 0:
            cons = cons + [
                Deg1 + ' - ' + BasicTools.minusTerms(d1) + ' + ' + BasicTools.plusTerms(CD_Blue) + ' = 0']
        else:
            cons = cons + [Deg1 + ' - ' + BasicTools.minusTerms(d1) + ' = 0']
        if len(CD_Red) > 0:
            cons = cons + [
                Deg2 + ' - ' + BasicTools.minusTerms(d2) + ' + ' + BasicTools.plusTerms(CD_Red) + ' = 0']
        else:
            cons = cons + [Deg2 + ' - ' + BasicTools.minusTerms(d2) + ' = 0']

        cons = cons + [Deg1 + ' >= -1']
        cons = cons + [Deg2 + ' >= -1']

        return cons

    def genConstraints_total(self):
        cons = []

        cons = cons + self.genConstraints_initial_degree()

        if self.ini_r <= self.mat_r:
            for r in range(self.ini_r, self.mat_r): # 1-2
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(self.mat_r + 1, self.TR): # 4
                cons = cons + self.genConstraints_backward_round(r)
            for r in range(0, self.ini_r): # 0
                cons = cons + self.genConstraints_backward_round(r)
        if self.ini_r > self.mat_r:
            for r in range(self.ini_r, self.TR): # 3-4
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(0, self.mat_r): # 无
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(self.mat_r + 1, self.ini_r): # 1-2
                cons = cons + self.genConstraints_backward_round(r)

        cons = cons + self.genConstraints_Match()

        cons = cons + self.genConstraints_additional()
        return cons

    def genModel(self, filename):
        V = set([])
        cons = []
        cons = cons + self.genConstraints_total()

        # cons = cons + ['GDeg1 + GDeg2 >= 32']
        cons = cons + ['GObj - GDeg1 <= 0']
        cons = cons + ['GObj - GDeg2 <= 0']
        cons = cons + ['GObj - GMat <= 0']
        cons = cons + ['GObj >= -1']

        V = BasicTools.getVariables_From_Constraints(cons)

        with open(filename + ".lp", "w") as fid:
            fid.write('Maximize' + '\n')
            fid.write('GObj' + '\n')
            fid.write('\n')
            fid.write('Subject To')
            fid.write('\n')
            for c in cons:
                fid.write(c)
                fid.write('\n')

            GV = []
            BV = []
            for v in V:
                if v[0] == 'G':
                    GV.append(v)
                else:
                    BV.append(v)

            fid.write('Bounds' + '\n')
            fid.write('GDeg1 >= -10' + '\n')
            fid.write('GDeg2 >= -10' + '\n')
            fid.write('GObj >= -10' + '\n')
            fid.write('Binary' + '\n')
            for bv in BV:
                fid.write(bv + '\n')

            fid.write('Generals' + '\n')
            for gv in GV:
                fid.write(gv + '\n')


if __name__ == '__main__':
    TR = 6

    root = f'./Model/TR{TR}'
    if not os.path.exists(root):
        os.mkdir(root)

    with open(f"./Model/Result_{TR}.txt", "w") as rd:
        rd.write('TR, ini_r, mat_r: d1, d2, m' + '\n')
        for ini_r in range(1, TR - 1):
            for mat_r in range(0, TR - 1):
                if mat_r != ini_r:
                    filename = f'./Model/TR{TR}/inir{ini_r}_matr{mat_r}'
                    A = Constraints_generator(TR, ini_r, mat_r)

                    A.genModel(filename)
                    Model = read(filename + '.lp')
                    # Model.setParam('TimeLimit', 180 * 60)
                    Model.optimize()

                    rd.write(str(TR) + ',' + str(ini_r) + ',' + str(mat_r) + ':')
                    if Model.SolCount == 0:
                        rd.write('none \n')
                    else:
                        Model.write(filename + '.sol')
                        solFile = open(filename + '.sol', 'r')
                        Sol = dict()

                        for line in solFile:
                            if line[0] != '#':
                                temp = line
                                # temp = temp.replace('-', ' ')
                                temp = temp.split()
                                Sol[temp[0]] = int(eval(temp[1]))
                        rd.write(str(Sol['GDeg1']) + ',' + str(Sol['GDeg2']) + ',' + str(Sol['GMat']) + '\n')
                        rd.flush()