
from utils import *
from gurobipy import *


class Vars_generator:
    @staticmethod
    def genVars_input_of_round(i, r, pos):
        return [f'IP_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_IP_isWhite(r, pos):
        return [f'IP_isWhite_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Blue_input_of_round(i, r, pos):
        return [f'IP_SupP_Blue_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_input_of_round(i, r, pos):
        return [f'IP_SupP_Red_{i}_r{r}_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_input_of_MixColumns(i, r):
        return [f'IMC_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_input_of_MixColumns_isWhite(r):
        return [f'IMC_isWhite_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Blue_input_of_MixColumns(i, r):
        return [f'IMC_SupP_Blue_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_SupP_Red_input_of_MixColumns(i, r):
        return [f'IMC_SupP_Red_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Blue_isWhite(r):
        return [f'OXor_SupP_Blue_isWhite_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Red_isWhite(r):
        return [f'OXor_SupP_Red_isWhite_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Xor_ConsumedDeg_Blue(r):
        return [f'CD_Xor_Blue_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Xor_ConsumedDeg_Red(r):
        return [f'CD_Xor_Red__r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Blue_SumGray(r):
        return [f'G_SupP_Blue_SumGray_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_MC_SupP_Red_SumGray(r):
        return [f'G_SupP_Red_SumGray_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Blue_AND(i, r):
        return [f'OXor_SupP_Blue_AND_{i}_r{r}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_OXor_SupP_Red_AND(i, r):
        return [f'OXor_SupP_Red_AND_{i}_r{r}_{j}' for j in range(bs)]

    # Initial Degree
    @staticmethod
    def genVars_degree__forward():
        return ['deg_f_' + str(j) for j in range(bs * b)]

    @staticmethod
    def genVars_degree_backward():
        return ['deg_b_' + str(j) for j in range(bs * b)]

    # Match
    @staticmethod
    def genVars_Match_Counter(pos):
        return [f'Match_Counter_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Match_SupP_Blue_isWhite(pos):
        return [f'Match_SupP_Blue_isWhite_{pos}_{j}' for j in range(bs)]

    @staticmethod
    def genVars_Match_SupP_Red_isWhite(pos):
        return [f'Match_SupP_Red_isWhite_{pos}_{j}' for j in range(bs)]


class Constraints_generator:
    def __init__(self, total_round, initial_round, matching_round):
        self.ini_r = initial_round
        self.mat_r = matching_round
        self.TR = total_round
        self.pos2 = ['L', 'R']
        self.isOdd = self.TR % 2

    def genConstraints_initial_degree(self):
        cons = []
        d1 = Vars_generator.genVars_degree__forward()
        d2 = Vars_generator.genVars_degree_backward()
        IP_1 = []
        IP_2 = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_isWhite = []
        for pos in self.pos2:
            IP_1 = IP_1 + Vars_generator.genVars_input_of_round(1, self.ini_r, pos)
            IP_2 = IP_2 + Vars_generator.genVars_input_of_round(2, self.ini_r, pos)
            IP_SupP_Blue_1 = IP_SupP_Blue_1 + Vars_generator.genVars_SupP_Blue_input_of_round(1, self.ini_r, pos)
            IP_SupP_Blue_2 = IP_SupP_Blue_2 + Vars_generator.genVars_SupP_Blue_input_of_round(2, self.ini_r, pos)
            IP_SupP_Red_1 = IP_SupP_Red_1 + Vars_generator.genVars_SupP_Red_input_of_round(1, self.ini_r, pos)
            IP_SupP_Red_2 = IP_SupP_Red_2 + Vars_generator.genVars_SupP_Red_input_of_round(2, self.ini_r, pos)
            IP_isWhite = IP_isWhite + Vars_generator.genVars_IP_isWhite(self.ini_r, pos)
        for bi in range(bs * b):
            cons = cons + [IP_1[bi] + ' + ' + IP_2[bi] + ' >= 1']
            cons = cons + [d1[bi] + ' + ' + IP_2[bi] + ' = 1']
            cons = cons + [d2[bi] + ' + ' + IP_1[bi] + ' = 1']
        for bi in range(bs * b):
            cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                IP_1[bi],
                IP_2[bi],
                IP_SupP_Blue_1[bi],
                IP_SupP_Blue_2[bi],
                IP_SupP_Red_1[bi],
                IP_SupP_Red_2[bi],
                IP_isWhite[bi]
            )
        return cons

    def genConstraints_forward_round(self, r):
        cons = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_nextr_SupP_Blue_1 = []
        IP_nextr_SupP_Blue_2 = []
        IP_nextr_SupP_Red_1 = []
        IP_nextr_SupP_Red_2 = []
        for pos in self.pos2:
            IP_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, r, pos))
            IP_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, r, pos))
            IP_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, r, pos))
            IP_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, r, pos))
            IP_nextr_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, r + 1, pos))
            IP_nextr_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, r + 1, pos))
            IP_nextr_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, r + 1, pos))
            IP_nextr_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, r + 1, pos))

        IMC_1 = Vars_generator.genVars_input_of_MixColumns(1, r)
        IMC_2 = Vars_generator.genVars_input_of_MixColumns(2, r)
        for bi in range(bs):
            cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_1[0][bi], IP_SupP_Red_1[0][bi]], IMC_1[bi])
            cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_2[0][bi], IP_SupP_Red_2[0][bi]], IMC_2[bi])

        # Separate
        IMC_SupP_Blue_1 = Vars_generator.genVars_SupP_Blue_input_of_MixColumns(1, r)
        IMC_SupP_Blue_2 = Vars_generator.genVars_SupP_Blue_input_of_MixColumns(2, r)
        IMC_SupP_Red_1 = Vars_generator.genVars_SupP_Red_input_of_MixColumns(1, r)
        IMC_SupP_Red_2 = Vars_generator.genVars_SupP_Red_input_of_MixColumns(2, r)
        IMC_isWhite = Vars_generator.genVars_input_of_MixColumns_isWhite(r)
        for bi in range(bs):
            cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                IMC_1[bi],
                IMC_2[bi],
                IMC_SupP_Blue_1[bi],
                IMC_SupP_Blue_2[bi],
                IMC_SupP_Red_1[bi],
                IMC_SupP_Red_2[bi],
                IMC_isWhite[bi]
            )
        if r != self.mat_r:
            # nXor
            CD_Xor_Blue = Vars_generator.genVars_Xor_ConsumedDeg_Blue(r)
            SumGray_SupP_Blue = Vars_generator.genVars_MC_SupP_Blue_SumGray(r)
            OXor_SupP_Blue_isWhite = Vars_generator.genVars_OXor_SupP_Blue_isWhite(r)
            OXor_SupP_Blue_AND_2 = Vars_generator.genVars_OXor_SupP_Blue_AND(2, r)
            CD_Xor_Red = Vars_generator.genVars_Xor_ConsumedDeg_Red(r)
            SumGray_SupP_Red = Vars_generator.genVars_MC_SupP_Red_SumGray(r)
            OXor_SupP_Red_isWhite = Vars_generator.genVars_OXor_SupP_Red_isWhite(r)
            OXor_SupP_Red_AND_1 = Vars_generator.genVars_OXor_SupP_Red_AND(1, r)
            for bi in range(bs):
                cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Blue_i(
                    Perm_Camellia(bi, IMC_SupP_Blue_1) + [IP_SupP_Blue_1[1][bi]],
                    Perm_Camellia(bi, IMC_SupP_Blue_2) + [IP_SupP_Blue_2[1][bi]],
                    IP_nextr_SupP_Blue_1[0][bi],
                    IP_nextr_SupP_Blue_2[0][bi],
                    CD_Xor_Blue[bi],
                    SumGray_SupP_Blue[bi],
                    OXor_SupP_Blue_isWhite[bi],
                    OXor_SupP_Blue_AND_2[bi]
                )
                cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Red_i(
                    Perm_Camellia(bi, IMC_SupP_Red_1) + [IP_SupP_Red_1[1][bi]],
                    Perm_Camellia(bi, IMC_SupP_Red_2) + [IP_SupP_Red_2[1][bi]],
                    IP_nextr_SupP_Red_1[0][bi],
                    IP_nextr_SupP_Red_2[0][bi],
                    CD_Xor_Red[bi],
                    SumGray_SupP_Red[bi],
                    OXor_SupP_Red_isWhite[bi],
                    OXor_SupP_Red_AND_1[bi]
                )

            # Link
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[0], IP_nextr_SupP_Blue_1[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[0], IP_nextr_SupP_Blue_2[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[0], IP_nextr_SupP_Red_1[1])
            cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[0], IP_nextr_SupP_Red_2[1])
        return cons

    def genConstraints_backward_round(self, r):
        cons = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_nextr_SupP_Blue_1 = []
        IP_nextr_SupP_Blue_2 = []
        IP_nextr_SupP_Red_1 = []
        IP_nextr_SupP_Red_2 = []
        for pos in self.pos2:
            IP_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, r, pos))
            IP_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, r, pos))
            IP_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, r, pos))
            IP_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, r, pos))
            IP_nextr_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, r + 1, pos))
            IP_nextr_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, r + 1, pos))
            IP_nextr_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, r + 1, pos))
            IP_nextr_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, r + 1, pos))

        IMC_1 = Vars_generator.genVars_input_of_MixColumns(1, r)
        IMC_2 = Vars_generator.genVars_input_of_MixColumns(2, r)
        for bi in range(bs):
            cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_1[0][bi], IP_SupP_Red_1[0][bi]], IMC_1[bi])
            cons = cons + MITMPreConstraints.Determine_Allone([IP_SupP_Blue_2[0][bi], IP_SupP_Red_2[0][bi]], IMC_2[bi])

        # Separate
        IMC_SupP_Blue_1 = Vars_generator.genVars_SupP_Blue_input_of_MixColumns(1, r)
        IMC_SupP_Blue_2 = Vars_generator.genVars_SupP_Blue_input_of_MixColumns(2, r)
        IMC_SupP_Red_1 = Vars_generator.genVars_SupP_Red_input_of_MixColumns(1, r)
        IMC_SupP_Red_2 = Vars_generator.genVars_SupP_Red_input_of_MixColumns(2, r)
        IMC_isWhite = Vars_generator.genVars_input_of_MixColumns_isWhite(r)
        for bi in range(bs):
            cons = cons + MITMPreConstraints.Separate_Without_Guess_i(
                IMC_1[bi],
                IMC_2[bi],
                IMC_SupP_Blue_1[bi],
                IMC_SupP_Blue_2[bi],
                IMC_SupP_Red_1[bi],
                IMC_SupP_Red_2[bi],
                IMC_isWhite[bi]
            )
        # nXor
        CD_Xor_Blue = Vars_generator.genVars_Xor_ConsumedDeg_Blue(r)
        SumGray_SupP_Blue = Vars_generator.genVars_MC_SupP_Blue_SumGray(r)
        OXor_SupP_Blue_isWhite = Vars_generator.genVars_OXor_SupP_Blue_isWhite(r)
        OXor_SupP_Blue_AND_2 = Vars_generator.genVars_OXor_SupP_Blue_AND(2, r)
        CD_Xor_Red = Vars_generator.genVars_Xor_ConsumedDeg_Red(r)
        SumGray_SupP_Red = Vars_generator.genVars_MC_SupP_Red_SumGray(r)
        OXor_SupP_Red_isWhite = Vars_generator.genVars_OXor_SupP_Red_isWhite(r)
        OXor_SupP_Red_AND_1 = Vars_generator.genVars_OXor_SupP_Red_AND(1, r)
        for bi in range(bs):
            cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Blue_i(
                Perm_Camellia(bi, IMC_SupP_Blue_1) + [IP_nextr_SupP_Blue_1[0][bi]],
                Perm_Camellia(bi, IMC_SupP_Blue_2) + [IP_nextr_SupP_Blue_2[0][bi]],
                IP_SupP_Blue_1[1][bi],
                IP_SupP_Blue_2[1][bi],
                CD_Xor_Blue[bi],
                SumGray_SupP_Blue[bi],
                OXor_SupP_Blue_isWhite[bi],
                OXor_SupP_Blue_AND_2[bi]
            )
            cons = cons + MITMPreConstraints.genConstraints_of_nXor_SupP_Red_i(
                Perm_Camellia(bi, IMC_SupP_Red_1) + [IP_nextr_SupP_Red_1[0][bi]],
                Perm_Camellia(bi, IMC_SupP_Red_2) + [IP_nextr_SupP_Red_2[0][bi]],
                IP_SupP_Red_1[1][bi],
                IP_SupP_Red_2[1][bi],
                CD_Xor_Red[bi],
                SumGray_SupP_Red[bi],
                OXor_SupP_Red_isWhite[bi],
                OXor_SupP_Red_AND_1[bi]
            )

        # Link
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[0], IP_nextr_SupP_Blue_1[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[0], IP_nextr_SupP_Blue_2[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[0], IP_nextr_SupP_Red_1[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[0], IP_nextr_SupP_Red_2[1])
        return cons

    def genConstraints_splice(self):
        cons = []
        IP_SupP_Blue_1 = []
        IP_SupP_Blue_2 = []
        IP_SupP_Red_1 = []
        IP_SupP_Red_2 = []
        IP_nextr_SupP_Blue_1 = []
        IP_nextr_SupP_Blue_2 = []
        IP_nextr_SupP_Red_1 = []
        IP_nextr_SupP_Red_2 = []
        for pos in self.pos2:
            IP_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, self.TR - 2, pos))
            IP_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, self.TR - 2, pos))
            IP_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, self.TR - 2, pos))
            IP_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, self.TR - 2, pos))
            IP_nextr_SupP_Blue_1.append(Vars_generator.genVars_SupP_Blue_input_of_round(1, 2, pos))
            IP_nextr_SupP_Blue_2.append(Vars_generator.genVars_SupP_Blue_input_of_round(2, 2, pos))
            IP_nextr_SupP_Red_1.append(Vars_generator.genVars_SupP_Red_input_of_round(1, 2, pos))
            IP_nextr_SupP_Red_2.append(Vars_generator.genVars_SupP_Red_input_of_round(2, 2, pos))
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[0], IP_nextr_SupP_Blue_1[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[0], IP_nextr_SupP_Blue_2[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[0], IP_nextr_SupP_Red_1[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[0], IP_nextr_SupP_Red_2[1])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_1[1], IP_nextr_SupP_Blue_1[0])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Blue_2[1], IP_nextr_SupP_Blue_2[0])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_1[1], IP_nextr_SupP_Red_1[0])
        cons = cons + MITMPreConstraints.equalConstraints(IP_SupP_Red_2[1], IP_nextr_SupP_Red_2[0])
        return cons

    def genConstraints_Match(self):
        cons = []
        Match_Counter = []
        for pos in self.pos2:
            Match_Counter.append(Vars_generator.genVars_Match_Counter(pos))
        Match_rounds = match_rounds(self.TR, self.ini_r, self.mat_r)
        Match_SupP_Blue_1_points = [[[] for bi in range(bs)] for i in range(b)]
        Match_SupP_Red_2_points = [[[] for bi in range(bs)] for i in range(b)]
        for i in range(b):
            for r in Match_rounds[i]:
                IMC_SupP_Blue_1 = Vars_generator.genVars_SupP_Blue_input_of_MixColumns(1, r)
                IMC_SupP_Red_2 = Vars_generator.genVars_SupP_Red_input_of_MixColumns(2, r)
                for bi in range(bs):
                    Match_SupP_Blue_1_points[i][bi].append(IMC_SupP_Blue_1[bi])
                    Match_SupP_Red_2_points[i][bi].append(IMC_SupP_Red_2[bi])
        for i in range(b):
            for bi in range(bs):
                cons = cons + MITMPreConstraints.Determine_Allone(
                    Match_SupP_Blue_1_points[i][bi] + Match_SupP_Red_2_points[i][bi],
                    Match_Counter[i][bi])
        return cons

    def genConstraints_additional(self):
        cons = []
        CD_Blue = []
        CD_Red = []
        for r in range(self.TR):
            if r not in [self.TR - 2, self.TR - 1, 0, 1]:
                CD_Blue = CD_Blue + Vars_generator.genVars_Xor_ConsumedDeg_Blue(r)
                CD_Red = CD_Red + Vars_generator.genVars_Xor_ConsumedDeg_Red(r)

        d1 = Vars_generator.genVars_degree__forward()
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

        cons = cons + [Deg1 + ' >= 1']
        cons = cons + [Deg2 + ' >= 1']

        Match_counter = []
        for pos in self.pos2:
            Match_counter = Match_counter + Vars_generator.genVars_Match_Counter(pos)
        GM = 'GMat'
        cons = cons + [GM + ' - ' + BasicTools.minusTerms(Match_counter) + ' = 0']
        cons = cons + [GM + ' >= 1']

        return cons

    def genConstraints_total(self):
        cons = []
        cons = cons + self.genConstraints_initial_degree()
        if self.ini_r <= self.mat_r:
            for r in range(self.ini_r, self.mat_r + 1):
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(2, self.ini_r):
                cons = cons + self.genConstraints_backward_round(r)
            for r in range(self.mat_r + 1, self.TR - 2):
                cons = cons + self.genConstraints_backward_round(r)
        if self.ini_r > self.mat_r:
            for r in range(self.ini_r, self.TR - 2):
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(2, self.mat_r + 1):
                cons = cons + self.genConstraints_forward_round(r)
            for r in range(self.mat_r + 1, self.ini_r):
                cons = cons + self.genConstraints_backward_round(r)
        cons = cons + self.genConstraints_splice()
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
        cons = cons + ['GObj >= 1']

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

            fid.write('Binary' + '\n')
            for bv in BV:
                fid.write(bv + '\n')

            fid.write('Generals' + '\n')
            for gv in GV:
                fid.write(gv + '\n')


if __name__ == '__main__':
    TR = 14
    root = f'./Model/TR{TR}'
    if not os.path.exists(root):
        os.mkdir(root)
    with open(f"./Model/Result_{TR}.txt", "w") as rd:
        rd.write('TR, ini_r, mat_r: d1, d2, m' + '\n')
        for ini_r in range(2, TR - 2):
            # for mat_r in range(11, 12):
            for mat_r in range(2, TR - 2):
        # for ini_r in range(9, 10):
        #     for mat_r in range(4, 5):
                if ini_r != mat_r:
                    filename = f'./Model/TR{TR}/inir{ini_r}_matr{mat_r}'
                    A = Constraints_generator(TR, ini_r, mat_r)
                    A.genModel(filename)
                    Model = read(filename + '.lp')
                    # Model.setParam('TimeLimit', 180 * 60)
                    Model.optimize()

                    if Model.SolCount == 0:
                        pass
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
                        rd.write(str(TR) + ',' + str(ini_r) + ',' + str(mat_r) + ':')
                        rd.write(str(Sol['GDeg1']) + ',' + str(Sol['GDeg2']) + ',' + str(Sol['GMat']) + '\n')
                        rd.flush()
