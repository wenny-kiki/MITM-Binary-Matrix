from utils import *
from gurobipy import *
import os


class constraints_generator:
    def __init__(self, TR, ini_r, mat_r):
        self.TR = TR
        self.ini_r = ini_r
        self.mat_r = mat_r
        self.m = Model("Midori64")
        # Variables
        self.Key1_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_1_{bi}") for bi in range(bs)]
        self.Key1_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_2_{bi}") for bi in range(bs)]
        self.Key2_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_1_{bi}") for bi in range(bs)]
        self.Key2_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_2_{bi}") for bi in range(bs)]
        self.Key1_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_SupP_Blue_1_{bi}") for bi in range(bs)]
        self.Key1_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_SupP_Blue_2_{bi}") for bi in range(bs)]
        self.Key1_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_SupP_Red_1_{bi}") for bi in range(bs)]
        self.Key1_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_SupP_Red_2_{bi}") for bi in range(bs)]
        self.Key2_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_SupP_Blue_1_{bi}") for bi in range(bs)]
        self.Key2_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_SupP_Blue_2_{bi}") for bi in range(bs)]
        self.Key2_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_SupP_Red_1_{bi}") for bi in range(bs)]
        self.Key2_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_SupP_Red_2_{bi}") for bi in range(bs)]
        self.Key1_MC_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_MC_SupP_Blue_1_{bi}") for bi in range(bs)]
        self.Key1_MC_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_MC_SupP_Blue_2_{bi}") for bi in range(bs)]
        self.Key1_MC_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_MC_SupP_Red_1_{bi}") for bi in range(bs)]
        self.Key1_MC_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key1_MC_SupP_Red_2_{bi}") for bi in range(bs)]
        self.Key2_MC_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_MC_SupP_Blue_1_{bi}") for bi in range(bs)]
        self.Key2_MC_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_MC_SupP_Blue_2_{bi}") for bi in range(bs)]
        self.Key2_MC_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_MC_SupP_Red_1_{bi}") for bi in range(bs)]
        self.Key2_MC_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key2_MC_SupP_Red_2_{bi}") for bi in range(bs)]
        self.IP_1 = [[self.m.addVar(vtype = GRB.BINARY, name = f"IP_1_r{r}_{bi}") for bi in range(bs)] for r in range(self.TR + 1)]
        self.IP_2 = [[self.m.addVar(vtype = GRB.BINARY, name = f"IP_2_r{r}_{bi}") for bi in range(bs)] for r in range(self.TR + 1)]
        # Initial Degree
        self.d1 = [self.m.addVar(vtype = GRB.BINARY, name = f"d1_{bi}") for bi in range(bs)]
        self.d2 = [self.m.addVar(vtype = GRB.BINARY, name = f"d2_{bi}") for bi in range(bs)]
        self.d1_Key1 = [self.m.addVar(vtype = GRB.BINARY, name = f"d1_Key1_{bi}") for bi in range(bs)]
        self.d2_Key1 = [self.m.addVar(vtype = GRB.BINARY, name = f"d2_Key1_{bi}") for bi in range(bs)]
        self.d1_Key2 = [self.m.addVar(vtype = GRB.BINARY, name = f"d1_Key2_{bi}") for bi in range(bs)]
        self.d2_Key2 = [self.m.addVar(vtype = GRB.BINARY, name = f"d2_Key2_{bi}") for bi in range(bs)]
        # Consume Degree
        self.CD_MC_Blue = []
        self.CD_MC_Red = []
        self.CD_MC_Blue_Real = []
        self.CD_MC_Red_Real = []
        self.CD_ARK_Blue = []
        self.CD_ARK_Red = []
        self.CD_Xor_Blue = []
        self.CD_Xor_Red = []
        self.CD_Key_MC_Blue = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_Key_MC_Blue_{bi}") for bi in range(2 * bs)]
        self.CD_Key_MC_Red = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_Key_MC_Red_{bi}") for bi in range(2 * bs)]
        self.CD_Key_MC_Blue_Real = [self.m.addVar(vtype = GRB.INTEGER, name = f"CD_Key_MC_Blue_Real_{Coli}") for Coli in range(2 * ColN)]
        self.CD_Key_MC_Red_Real = [self.m.addVar(vtype = GRB.INTEGER, name = f"CD_Key_MC_Red_Real_{Coli}") for Coli in range(2 * ColN)]
        self.CD_WhitenKey_Blue = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_WhitenKey_Blue_{bi}") for bi in range(2 * bs)]
        self.CD_WhitenKey_Red = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_WhitenKey_Red_{bi}") for bi in range(2 * bs)]
        self.CD_WhitenKey_Blue_Key = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_WhitenKey_Blue_Key_{bi}") for bi in range(2 * bs)]
        self.CD_WhitenKey_Red_Key = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_WhitenKey_Red_Key_{bi}") for bi in range(2 * bs)]
        self.CD_WhitenKey_Blue_Key_Real = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_WhitenKey_Blue_Key_Real_{bi}") for bi in range(bs)]
        self.CD_WhitenKey_Red_Key_Real = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_WhitenKey_Red_Key_Real_{bi}") for bi in range(bs)]
        # Match
        self.Match_counter = [self.m.addVar(vtype = GRB.INTEGER, name = f"Match_counter_{Coli}") for Coli in range(ColN)]
        self.Match_isNotWhite_forward = [self.m.addVar(vtype = GRB.BINARY, name = f"Match_isNotWhite_forward_{bi}") for bi in range(bs)]
        self.Match_isNotWhite_backward = [self.m.addVar(vtype = GRB.BINARY, name = f"Match_isNotWhite_backward_{bi}") for bi in range(bs)]
        # Objective
        self.GMat = self.m.addVar(vtype = GRB.INTEGER, name = "GMat")
        self.GDeg1 = self.m.addVar(vtype = GRB.INTEGER, name = "GDeg1")
        self.GDeg2 = self.m.addVar(vtype = GRB.INTEGER, name = "GDeg2")
        self.Obj = self.m.addVar(vtype = GRB.INTEGER, name = "Obj")
        self.ExistGray = [self.m.addVar(vtype = GRB.BINARY, name = f"ExistGray_{bi}") for bi in range(bs)]

    def genConstraints_initial_degree(self):
        for bi in range(bs):
            self.m.addConstr(self.IP_1[self.ini_r][bi] + self.IP_2[self.ini_r][bi] >= 1)
            self.m.addConstr(self.d1[bi] + self.IP_2[self.ini_r][bi] == 1)
            self.m.addConstr(self.d2[bi] + self.IP_1[self.ini_r][bi] == 1)
        for bi in range(bs):
            self.m.addConstr(self.Key1_1[bi] + self.Key1_2[bi] >= 1)
            self.m.addConstr(self.d1_Key1[bi] + self.Key1_2[bi] == 1)
            self.m.addConstr(self.d2_Key1[bi] + self.Key1_1[bi] == 1)
            self.m.addConstr(self.Key2_1[bi] + self.Key2_2[bi] >= 1)
            self.m.addConstr(self.d1_Key2[bi] + self.Key2_2[bi] == 1)
            self.m.addConstr(self.d2_Key2[bi] + self.Key2_1[bi] == 1)

            self.m.addConstr(self.Key1_SupP_Blue_1[bi] == 1)
            self.m.addConstr(self.Key1_SupP_Red_2[bi] == 1)
            self.m.addConstr(self.Key1_SupP_Blue_2[bi] == self.Key1_2[bi])
            self.m.addConstr(self.Key1_SupP_Red_1[bi] == self.Key1_1[bi])

            self.m.addConstr(self.Key2_SupP_Blue_1[bi] == 1)
            self.m.addConstr(self.Key2_SupP_Red_2[bi] == 1)
            self.m.addConstr(self.Key2_SupP_Blue_2[bi] == self.Key2_2[bi])
            self.m.addConstr(self.Key2_SupP_Red_1[bi] == self.Key2_1[bi])
        self.m.addConstr(quicksum(self.d1_Key1) + quicksum(self.d1_Key2) >= 1)
        self.m.addConstr(quicksum(self.d2_Key1) + quicksum(self.d2_Key2) >= 1)

    def genConstraints_Key_MC_Inv(self):
        # Key MC_Inv
        Key_MC_SumGary_SupP_Blue = [self.m.addVar(vtype = GRB.INTEGER, name = f"Key_MC_SumGary_SupP_Blue_{bi}") for bi in range(2 * bs)]
        Key_MC_IP_hasNoWhite = [self.m.addVar(vtype = GRB.BINARY, name = f"Key_MC_IP_hasNoWhite_{bi}") for bi in range(2 * bs)]
        Key_MC_IP_SupP_Blue_AND_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key_MC_IP_SupP_Blue_AND_2_{bi}") for bi in range(2 * bs)]
        Key_MC_SumGary_SupP_Red = [self.m.addVar(vtype = GRB.INTEGER, name = f"Key_MC_SumGary_SupP_Red_{bi}") for bi in range(2 * bs)]
        Key_MC_IP_SupP_Red_AND_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"Key_MC_IP_SupP_Red_AND_1_{bi}") for bi in range(2 * bs)]
        for Coli in range(ColN):
            for RoWi in range(RowN):
                MITMPreConstraints.NXor_SupP_Blue_i(
                    [column(self.Key1_SupP_Blue_1, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    [column(self.Key1_SupP_Blue_2, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    self.Key1_MC_SupP_Blue_1[RoWi * ColN + Coli],
                    self.Key1_MC_SupP_Blue_2[RoWi * ColN + Coli],
                    self.CD_Key_MC_Blue[RoWi * ColN + Coli],
                    Key_MC_SumGary_SupP_Blue[RoWi * ColN + Coli],
                    Key_MC_IP_hasNoWhite[RoWi * ColN + Coli],
                    Key_MC_IP_SupP_Blue_AND_2[RoWi * ColN + Coli],
                    self.m
                )
                MITMPreConstraints.NXor_SupP_Red_i(
                    [column(self.Key1_SupP_Red_1, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    [column(self.Key1_SupP_Red_2, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    self.Key1_MC_SupP_Red_1[RoWi * ColN + Coli],
                    self.Key1_MC_SupP_Red_2[RoWi * ColN + Coli],
                    self.CD_Key_MC_Red[RoWi * ColN + Coli],
                    Key_MC_SumGary_SupP_Red[RoWi * ColN + Coli],
                    Key_MC_IP_hasNoWhite[RoWi * ColN + Coli],
                    Key_MC_IP_SupP_Red_AND_1[RoWi * ColN + Coli],
                    self.m
                )
                MITMPreConstraints.NXor_SupP_Blue_i(
                    [column(self.Key2_SupP_Blue_1, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    [column(self.Key2_SupP_Blue_2, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    self.Key2_MC_SupP_Blue_1[RoWi * ColN + Coli],
                    self.Key2_MC_SupP_Blue_2[RoWi * ColN + Coli],
                    self.CD_Key_MC_Blue[RoWi * ColN + Coli + bs],
                    Key_MC_SumGary_SupP_Blue[RoWi * ColN + Coli + bs],
                    Key_MC_IP_hasNoWhite[RoWi * ColN + Coli + bs],
                    Key_MC_IP_SupP_Blue_AND_2[RoWi * ColN + Coli + bs],
                    self.m
                )
                MITMPreConstraints.NXor_SupP_Red_i(
                    [column(self.Key2_SupP_Red_1, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    [column(self.Key2_SupP_Red_2, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    self.Key2_MC_SupP_Red_1[RoWi * ColN + Coli],
                    self.Key2_MC_SupP_Red_2[RoWi * ColN + Coli],
                    self.CD_Key_MC_Red[RoWi * ColN + Coli + bs],
                    Key_MC_SumGary_SupP_Red[RoWi * ColN + Coli + bs],
                    Key_MC_IP_hasNoWhite[RoWi * ColN + Coli + bs],
                    Key_MC_IP_SupP_Red_AND_1[RoWi * ColN + Coli + bs],
                    self.m
                )
        for Coli in range(ColN):
            MITMPreConstraints.compute_real_CD_MC(
                column(self.Key1_SupP_Blue_2, Coli),
                column(self.CD_Key_MC_Blue, Coli),
                self.CD_Key_MC_Blue_Real[Coli],
                self.m
            )
            MITMPreConstraints.compute_real_CD_MC(
                column(self.Key1_SupP_Red_1, Coli),
                column(self.CD_Key_MC_Red, Coli),
                self.CD_Key_MC_Red_Real[Coli],
                self.m
            )
            MITMPreConstraints.compute_real_CD_MC(
                column(self.Key2_SupP_Blue_2, Coli),
                column(self.CD_Key_MC_Blue[bs:], Coli),
                self.CD_Key_MC_Blue_Real[Coli + ColN],
                self.m
            )
            MITMPreConstraints.compute_real_CD_MC(
                column(self.Key2_SupP_Red_1, Coli),
                column(self.CD_Key_MC_Red[bs:], Coli),
                self.CD_Key_MC_Red_Real[Coli + ColN],
                self.m
            )

    def genConstraints_forward(self, r):
        IMC_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"IMC_SupP_Blue_1_r{r}_{bi}") for bi in range(bs)]
        IMC_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"IMC_SupP_Blue_2_r{r}_{bi}") for bi in range(bs)]
        IMC_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"IMC_SupP_Red_1_r{r}_{bi}") for bi in range(bs)]
        IMC_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"IMC_SupP_Red_2_r{r}_{bi}") for bi in range(bs)]
        In_isNotWhite = [self.m.addVar(vtype = GRB.BINARY, name = f"In_isNotWhite_r{r}_{bi}") for bi in range(bs)]
        # Separate - ShuffleCell
        for bi in range(bs):
            MITMPreConstraints.Separate_Without_Guess_i(
                self.IP_1[r][bi],
                self.IP_2[r][bi],
                ShuffleCell_Inv(IMC_SupP_Blue_1)[bi],
                ShuffleCell_Inv(IMC_SupP_Blue_2)[bi],
                ShuffleCell_Inv(IMC_SupP_Red_1)[bi],
                ShuffleCell_Inv(IMC_SupP_Red_2)[bi],
                In_isNotWhite[bi],
                self.m
            )
        # MC
        OMC_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"OMC_SupP_Blue_1_r{r}_{bi}") for bi in range(bs)]
        OMC_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"OMC_SupP_Blue_2_r{r}_{bi}") for bi in range(bs)]
        OMC_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"OMC_SupP_Red_1_r{r}_{bi}") for bi in range(bs)]
        OMC_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"OMC_SupP_Red_2_r{r}_{bi}") for bi in range(bs)]
        CD_MC_Blue = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_MC_Blue_r{r}_{bi}") for bi in range(bs)]
        CD_MC_Red = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_MC_Red_r{r}_{bi}") for bi in range(bs)]
        self.CD_MC_Blue += CD_MC_Blue
        self.CD_MC_Red += CD_MC_Red
        MC_SumGary_SupP_Blue = [self.m.addVar(vtype = GRB.INTEGER, name = f"MC_SumGary_SupP_Blue_r{r}_{bi}") for bi in range(bs)]
        MC_SumGary_SupP_Red = [self.m.addVar(vtype = GRB.INTEGER, name = f"MC_SumGary_SupP_Red_r{r}_{bi}") for bi in range(bs)]
        MC_IP_hasNoWhite = [self.m.addVar(vtype = GRB.BINARY, name = f"MC_IP_hasNoWhite_r{r}_{bi}") for bi in range(bs)]
        MC_IP_SupP_Blue_AND_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"MC_IP_SupP_Blue_AND_2_r{r}_{bi}") for bi in range(bs)]
        MC_IP_SupP_Red_AND_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"MC_IP_SupP_Red_AND_1_r{r}_{bi}") for bi in range(bs)]
        for Coli in range(ColN):
            for RoWi in range(RowN):
                MITMPreConstraints.NXor_SupP_Blue_i(
                    [column(IMC_SupP_Blue_1, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    [column(IMC_SupP_Blue_2, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    OMC_SupP_Blue_1[RoWi * ColN + Coli],
                    OMC_SupP_Blue_2[RoWi * ColN + Coli],
                    CD_MC_Blue[RoWi * ColN + Coli],
                    MC_SumGary_SupP_Blue[RoWi * ColN + Coli],
                    MC_IP_hasNoWhite[RoWi * ColN + Coli],
                    MC_IP_SupP_Blue_AND_2[RoWi * ColN + Coli],
                    self.m
                )
                MITMPreConstraints.NXor_SupP_Red_i(
                    [column(IMC_SupP_Red_1, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    [column(IMC_SupP_Red_2, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    OMC_SupP_Red_1[RoWi * ColN + Coli],
                    OMC_SupP_Red_2[RoWi * ColN + Coli],
                    CD_MC_Red[RoWi * ColN + Coli],
                    MC_SumGary_SupP_Red[RoWi * ColN + Coli],
                    MC_IP_hasNoWhite[RoWi * ColN + Coli],
                    MC_IP_SupP_Red_AND_1[RoWi * ColN + Coli],
                    self.m
                )
        # Compute the Real Consumed Degree
        CD_MC_Blue_Real = [self.m.addVar(vtype = GRB.INTEGER, name = f"CD_MC_Blue_Real_r{r}_{Coli}") for Coli in range(ColN)]
        CD_MC_Red_Real = [self.m.addVar(vtype = GRB.INTEGER, name = f"CD_MC_Red_Real_r{r}_{Coli}") for Coli in range(ColN)]
        self.CD_MC_Blue_Real += CD_MC_Blue_Real
        self.CD_MC_Red_Real += CD_MC_Red_Real
        for Coli in range(ColN):
            MITMPreConstraints.compute_real_CD_MC(
                column(IMC_SupP_Blue_2, Coli),
                column(CD_MC_Blue, Coli),
                CD_MC_Blue_Real[Coli],
                self.m
            )
            MITMPreConstraints.compute_real_CD_MC(
                column(IMC_SupP_Red_1, Coli),
                column(CD_MC_Red, Coli),
                CD_MC_Red_Real[Coli],
                self.m
            )
        # ARK
        OAK_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"OAK_SupP_Blue_1_r{r}_{bi}") for bi in range(bs)]
        OAK_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"OAK_SupP_Blue_2_r{r}_{bi}") for bi in range(bs)]
        OAK_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"OAK_SupP_Red_1_r{r}_{bi}") for bi in range(bs)]
        OAK_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"OAK_SupP_Red_2_r{r}_{bi}") for bi in range(bs)]
        CD_ARK_Blue = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_ARK_Blue_r{r}_{bi}") for bi in range(bs)]
        CD_ARK_Red = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_ARK_Red_r{r}_{bi}") for bi in range(bs)]
        self.CD_ARK_Blue += CD_ARK_Blue
        self.CD_ARK_Red += CD_ARK_Red
        ARK_SumGary_SupP_Blue = [self.m.addVar(vtype = GRB.INTEGER, name = f"ARK_SumGary_SupP_Blue_r{r}_{bi}") for bi in range(bs)]
        ARK_SumGary_SupP_Red = [self.m.addVar(vtype = GRB.INTEGER, name = f"ARK_SumGary_SupP_Red_r{r}_{bi}") for bi in range(bs)]
        ARK_IP_hasNoWhite = [self.m.addVar(vtype = GRB.BINARY, name = f"ARK_IP_hasNoWhite_r{r}_{bi}") for bi in range(bs)]
        ARK_IP_SupP_Blue_AND_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"ARK_IP_SupP_Blue_AND_2_r{r}_{bi}") for bi in range(bs)]
        ARK_IP_SupP_Red_AND_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"ARK_IP_SupP_Red_AND_1_r{r}_{bi}") for bi in range(bs)]
        if r % 2 == 0:
            Key_SupP_Blue_1 = self.Key1_SupP_Blue_1
            Key_SupP_Blue_2 = self.Key1_SupP_Blue_2
            Key_SupP_Red_1 = self.Key1_SupP_Red_1
            Key_SupP_Red_2 = self.Key1_SupP_Red_2
        else:
            Key_SupP_Blue_1 = self.Key2_SupP_Blue_1
            Key_SupP_Blue_2 = self.Key2_SupP_Blue_2
            Key_SupP_Red_1 = self.Key2_SupP_Red_1
            Key_SupP_Red_2 = self.Key2_SupP_Red_2
        for bi in range(bs):
            MITMPreConstraints.NXor_SupP_Blue_i(
                [OMC_SupP_Blue_1[bi], Key_SupP_Blue_1[bi]],
                [OMC_SupP_Blue_2[bi], Key_SupP_Blue_2[bi]],
                OAK_SupP_Blue_1[bi],
                OAK_SupP_Blue_2[bi],
                CD_ARK_Blue[bi],
                ARK_SumGary_SupP_Blue[bi],
                ARK_IP_hasNoWhite[bi],
                ARK_IP_SupP_Blue_AND_2[bi],
                self.m
            )
            MITMPreConstraints.NXor_SupP_Red_i(
                [OMC_SupP_Red_1[bi], Key_SupP_Red_1[bi]],
                [OMC_SupP_Red_2[bi], Key_SupP_Red_2[bi]],
                OAK_SupP_Red_1[bi],
                OAK_SupP_Red_2[bi],
                CD_ARK_Red[bi],
                ARK_SumGary_SupP_Red[bi],
                ARK_IP_hasNoWhite[bi],
                ARK_IP_SupP_Red_AND_1[bi],
                self.m
            )

        # Merge
        for bi in range(bs):
            self.m.addGenConstrAnd(self.IP_1[r + 1][bi], [OAK_SupP_Blue_1[bi], OAK_SupP_Red_1[bi]])
            self.m.addGenConstrAnd(self.IP_2[r + 1][bi], [OAK_SupP_Blue_2[bi], OAK_SupP_Red_2[bi]])

    def genConstraints_backward(self, r):
        # Separate
        IP_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"IP_SupP_Blue_1_r{r}_{bi}") for bi in range(bs)]
        IP_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"IP_SupP_Blue_2_r{r}_{bi}") for bi in range(bs)]
        IP_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"IP_SupP_Red_1_r{r}_{bi}") for bi in range(bs)]
        IP_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"IP_SupP_Red_2_r{r}_{bi}") for bi in range(bs)]
        In_isNotWhite = [self.m.addVar(vtype = GRB.BINARY, name = f"In_isNotWhite_r{r}_{bi}") for bi in range(bs)]
        for bi in range(bs):
            MITMPreConstraints.Separate_Without_Guess_i(
                self.IP_1[r + 1][bi],
                self.IP_2[r + 1][bi],
                IP_SupP_Blue_1[bi],
                IP_SupP_Blue_2[bi],
                IP_SupP_Red_1[bi],
                IP_SupP_Red_2[bi],
                In_isNotWhite[bi],
                self.m
            )

        # ARK - MC
        OMC_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"OMC_SupP_Blue_1_r{r}_{bi}") for bi in range(bs)]
        OMC_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"OMC_SupP_Blue_2_r{r}_{bi}") for bi in range(bs)]
        OMC_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"OMC_SupP_Red_1_r{r}_{bi}") for bi in range(bs)]
        OMC_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"OMC_SupP_Red_2_r{r}_{bi}") for bi in range(bs)]
        CD_MC_Blue = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_MC_Blue_r{r}_{bi}") for bi in range(bs)]
        CD_MC_Red = [self.m.addVar(vtype = GRB.BINARY, name = f"CD_MC_Red_r{r}_{bi}") for bi in range(bs)]
        self.CD_MC_Blue += CD_MC_Blue
        self.CD_MC_Red += CD_MC_Red
        MC_SumGary_SupP_Blue = [self.m.addVar(vtype = GRB.INTEGER, name = f"MC_SumGary_SupP_Blue_r{r}_{bi}") for bi in range(bs)]
        MC_SumGary_SupP_Red = [self.m.addVar(vtype = GRB.INTEGER, name = f"MC_SumGary_SupP_Red_r{r}_{bi}") for bi in range(bs)]
        MC_IP_hasNoWhite = [self.m.addVar(vtype = GRB.BINARY, name = f"MC_IP_hasNoWhite_r{r}_{bi}") for bi in range(bs)]
        MC_IP_SupP_Blue_AND_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"MC_IP_SupP_Blue_AND_2_r{r}_{bi}") for bi in range(bs)]
        MC_IP_SupP_Red_AND_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"MC_IP_SupP_Red_AND_1_r{r}_{bi}") for bi in range(bs)]
        # IP - MC
        for Coli in range(ColN):
            for RoWi in range(RowN):
                MITMPreConstraints.NXor_SupP_Blue_i(
                    [column(IP_SupP_Blue_1, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    [column(IP_SupP_Blue_2, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    OMC_SupP_Blue_1[RoWi * ColN + Coli],
                    OMC_SupP_Blue_2[RoWi * ColN + Coli],
                    CD_MC_Blue[RoWi * ColN + Coli],
                    MC_SumGary_SupP_Blue[RoWi * ColN + Coli],
                    MC_IP_hasNoWhite[RoWi * ColN + Coli],
                    MC_IP_SupP_Blue_AND_2[RoWi * ColN + Coli],
                    self.m
                )
                MITMPreConstraints.NXor_SupP_Red_i(
                    [column(IP_SupP_Red_1, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    [column(IP_SupP_Red_2, Coli)[bi] for bi in range(ColN) if MC[RoWi][bi] == 1],
                    OMC_SupP_Red_1[RoWi * ColN + Coli],
                    OMC_SupP_Red_2[RoWi * ColN + Coli],
                    CD_MC_Red[RoWi * ColN + Coli],
                    MC_SumGary_SupP_Red[RoWi * ColN + Coli],
                    MC_IP_hasNoWhite[RoWi * ColN + Coli],
                    MC_IP_SupP_Red_AND_1[RoWi * ColN + Coli],
                    self.m
                )
        # Compute Real Consumed Degree of IP - MC
        CD_MC_Blue_Real = [self.m.addVar(vtype = GRB.INTEGER, name = f"CD_MC_Blue_Real_r{r}_{Coli}") for Coli in range(ColN)]
        CD_MC_Red_Real = [self.m.addVar(vtype = GRB.INTEGER, name = f"CD_MC_Red_Real_r{r}_{Coli}") for Coli in range(ColN)]
        self.CD_MC_Blue_Real += CD_MC_Blue_Real
        self.CD_MC_Red_Real += CD_MC_Red_Real
        for Coli in range(ColN):
            MITMPreConstraints.compute_real_CD_MC(
                column(IP_SupP_Blue_2, Coli),
                column(CD_MC_Blue, Coli),
                CD_MC_Blue_Real[Coli],
                self.m
            )
            MITMPreConstraints.compute_real_CD_MC(
                column(IP_SupP_Red_1, Coli),
                column(CD_MC_Red, Coli),
                CD_MC_Red_Real[Coli],
                self.m
            )

        # ARK
        if r % 2 == 0:
            Key_SupP_Blue_1 = self.Key1_MC_SupP_Blue_1
            Key_SupP_Blue_2 = self.Key1_MC_SupP_Blue_2
            Key_SupP_Red_1 = self.Key1_MC_SupP_Red_1
            Key_SupP_Red_2 = self.Key1_MC_SupP_Red_2
        else:
            Key_SupP_Blue_1 = self.Key2_MC_SupP_Blue_1
            Key_SupP_Blue_2 = self.Key2_MC_SupP_Blue_2
            Key_SupP_Red_1 = self.Key2_MC_SupP_Red_1
            Key_SupP_Red_2 = self.Key2_MC_SupP_Red_2
        IMC_SupP_Blue_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"IMC_SupP_Blue_1_r{r}_{bi}") for bi in range(bs)]
        IMC_SupP_Blue_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"IMC_SupP_Blue_2_r{r}_{bi}") for bi in range(bs)]
        IMC_SupP_Red_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"IMC_SupP_Red_1_r{r}_{bi}") for bi in range(bs)]
        IMC_SupP_Red_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"IMC_SupP_Red_2_r{r}_{bi}") for bi in range(bs)]
        CD_Xor_Blue = [self.m.addVar(vtype = GRB.BINARY, name = f'CD_Xor_Blue_r{r}_{bi}') for bi in range(bs)]
        CD_Xor_Red = [self.m.addVar(vtype = GRB.BINARY, name = f'CD_Xor_Red_r{r}_{bi}') for bi in range(bs)]
        self.CD_Xor_Blue += CD_Xor_Blue
        self.CD_Xor_Red += CD_Xor_Red
        for bi in range(bs):
            MITMPreConstraints.Xor2_SupP_Blue_i(
                OMC_SupP_Blue_1[bi],
                OMC_SupP_Blue_2[bi],
                Key_SupP_Blue_1[bi],
                Key_SupP_Blue_2[bi],
                IMC_SupP_Blue_1[bi],
                IMC_SupP_Blue_2[bi],
                self.CD_Key_MC_Blue[bi + (r % 2) * bs],
                CD_Xor_Blue[bi],
                self.m
            )
            MITMPreConstraints.Xor2_SupP_Red_i(
                OMC_SupP_Red_1[bi],
                OMC_SupP_Red_2[bi],
                Key_SupP_Red_1[bi],
                Key_SupP_Red_2[bi],
                IMC_SupP_Red_1[bi],
                IMC_SupP_Red_2[bi],
                self.CD_Key_MC_Red[bi + (r % 2) * bs],
                CD_Xor_Red[bi],
                self.m
            )
        # Merge
        for bi in range(bs):
            self.m.addGenConstrAnd(self.IP_1[r][bi], [ShuffleCell_Inv(IMC_SupP_Blue_1)[bi], ShuffleCell_Inv(IMC_SupP_Red_1)[bi]])
            self.m.addGenConstrAnd(self.IP_2[r][bi], [ShuffleCell_Inv(IMC_SupP_Blue_2)[bi], ShuffleCell_Inv(IMC_SupP_Red_2)[bi]])

    def genConstraints_Xor_WhitenKey(self):
        PT_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"PT_1_{bi}") for bi in range(bs)]
        PT_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"PT_2_{bi}") for bi in range(bs)]
        CT_1 = [self.m.addVar(vtype = GRB.BINARY, name = f"CT_1_{bi}") for bi in range(bs)]
        CT_2 = [self.m.addVar(vtype = GRB.BINARY, name = f"CT_2_{bi}") for bi in range(bs)]
        # self.m.addConstr(quicksum(self.ExistGray) >= 1)
        if self.ini_r < self.mat_r:
            for bi in range(bs):
                self.m.addConstr(self.IP_1[0][bi] + self.IP_2[0][bi] >= 1)
            for bi in range(bs):
                self.m.addConstr(CT_1[bi] == 0)
                self.m.addConstr(CT_2[bi] == 1)
                self.m.addConstr(PT_2[bi] == 1)
                self.m.addConstr(PT_1[bi] <= PT_2[bi])
                self.m.addGenConstrAnd(self.ExistGray[bi], [PT_1[bi], PT_2[bi]])
            for bi in range(bs):
                MITMPreConstraints.WhiterKey_Xor(
                    self.Key1_1[bi],
                    self.Key1_2[bi],
                    self.Key2_1[bi],
                    self.Key2_2[bi],
                    self.IP_1[0][bi],
                    self.IP_2[0][bi],
                    PT_1[bi],
                    PT_2[bi],
                    self.CD_WhitenKey_Blue[bi],
                    self.CD_WhitenKey_Red[bi],
                    self.CD_WhitenKey_Blue_Key[bi],
                    self.CD_WhitenKey_Red_Key[bi],
                    self.m
                )
                MITMPreConstraints.WhiterKey_Xor(
                    self.Key1_1[bi],
                    self.Key1_2[bi],
                    self.Key2_1[bi],
                    self.Key2_2[bi],
                    CT_1[bi],
                    CT_2[bi],
                    self.IP_1[self.TR][bi],
                    self.IP_2[self.TR][bi],
                    self.CD_WhitenKey_Blue[bs + bi],
                    self.CD_WhitenKey_Red[bs + bi],
                    self.CD_WhitenKey_Blue_Key[bs + bi],
                    self.CD_WhitenKey_Red_Key[bs + bi],
                    self.m
                )
        if self.ini_r > self.mat_r:
            for bi in range(bs):
                self.m.addConstr(self.IP_1[self.TR][bi] + self.IP_2[self.TR][bi] >= 1)
            for bi in range(bs):
                self.m.addConstr(PT_1[bi] == 0)
                self.m.addConstr(PT_2[bi] == 1)
                self.m.addConstr(CT_2[bi] == 1)
                self.m.addConstr(CT_1[bi] <= CT_2[bi])
                self.m.addGenConstrAnd(self.ExistGray[bi], [CT_1[bi], CT_2[bi]])
            for bi in range(bs):
                MITMPreConstraints.WhiterKey_Xor(
                    self.Key1_1[bi],
                    self.Key1_2[bi],
                    self.Key2_1[bi],
                    self.Key2_2[bi],
                    PT_1[bi],
                    PT_2[bi],
                    self.IP_1[0][bi],
                    self.IP_2[0][bi],
                    self.CD_WhitenKey_Blue[bi],
                    self.CD_WhitenKey_Red[bi],
                    self.CD_WhitenKey_Blue_Key[bi],
                    self.CD_WhitenKey_Red_Key[bi],
                    self.m
                )
                MITMPreConstraints.WhiterKey_Xor(
                    self.Key1_1[bi],
                    self.Key1_2[bi],
                    self.Key2_1[bi],
                    self.Key2_2[bi],
                    self.IP_1[self.TR][bi],
                    self.IP_2[self.TR][bi],
                    CT_1[bi],
                    CT_2[bi],
                    self.CD_WhitenKey_Blue[bs + bi],
                    self.CD_WhitenKey_Red[bs + bi],
                    self.CD_WhitenKey_Blue_Key[bs + bi],
                    self.CD_WhitenKey_Red_Key[bs + bi],
                    self.m
                )
        for bi in range(bs):
            self.m.addGenConstrOr(self.CD_WhitenKey_Blue_Key_Real[bi], [self.CD_WhitenKey_Blue_Key[bi], self.CD_WhitenKey_Blue_Key[bs + bi]])
            self.m.addGenConstrOr(self.CD_WhitenKey_Red_Key_Real[bi], [self.CD_WhitenKey_Red_Key[bi], self.CD_WhitenKey_Red_Key[bs + bi]])

    def genConstraints_Match(self):
        for bi in range(bs):
            self.m.addGenConstrOr(self.Match_isNotWhite_forward[bi], [ShuffleCell(self.IP_1[self.mat_r])[bi], ShuffleCell(self.IP_2[self.mat_r])[bi]])
            self.m.addGenConstrOr(self.Match_isNotWhite_backward[bi], [self.IP_1[self.mat_r + 1][bi], self.IP_2[self.mat_r + 1][bi]])
        for Coli in range(ColN):
            MITMPreConstraints.Match(
                column(self.Match_isNotWhite_forward, Coli),
                column(self.Match_isNotWhite_backward, Coli),
                self.Match_counter[Coli],
                self.m
            )
        self.m.addConstr(quicksum(self.Match_counter) == self.GMat)
        self.m.addConstr(self.GMat >= 1)

    def genConstraints_additional(self):
        d1_CD = self.m.addVar(vtype = GRB.INTEGER, name = f"d1_CD")
        d2_CD = self.m.addVar(vtype = GRB.INTEGER, name = f"d2_CD")
        self.m.addConstr(quicksum(self.d1) - quicksum(self.CD_MC_Blue_Real + self.CD_ARK_Blue + self.CD_Xor_Blue + self.CD_WhitenKey_Blue) == d1_CD)
        self.m.addConstr(quicksum(self.d2) - quicksum(self.CD_MC_Red_Real + self.CD_ARK_Red + self.CD_Xor_Red + self.CD_WhitenKey_Red) == d2_CD)
        self.m.addConstr(d1_CD + d2_CD == 0)
        self.m.addConstr(quicksum(self.d1_Key1 + self.d1_Key2) - quicksum(self.CD_Key_MC_Blue_Real + self.CD_WhitenKey_Blue_Key_Real) == self.GDeg1)
        self.m.addConstr(quicksum(self.d2_Key1 + self.d2_Key2) - quicksum(self.CD_Key_MC_Red_Real + self.CD_WhitenKey_Red_Key_Real) == self.GDeg2)
        self.m.addConstr(self.Obj <= self.GDeg1)
        self.m.addConstr(self.Obj <= self.GDeg2)
        # IP_1 = ShuffleCell(self.IP_1[self.TR])
        # IP_2 = ShuffleCell(self.IP_1[self.TR])

    def genConstraints_total(self):
        self.genConstraints_initial_degree()
        if self.ini_r < self.mat_r:
            for r in range(self.ini_r, self.mat_r):
                self.genConstraints_forward(r)
            for r in range(0, self.ini_r):
                self.genConstraints_backward(r)
            for r in range(self.mat_r + 1, self.TR):
                self.genConstraints_backward(r)
        if self.ini_r > self.mat_r:
            for r in range(self.ini_r, self.TR):
                self.genConstraints_forward(r)
            for r in range(0, self.mat_r):
                self.genConstraints_forward(r)
            for r in range(self.mat_r + 1, self.ini_r):
                self.genConstraints_backward(r)
        self.genConstraints_Key_MC_Inv()
        self.genConstraints_Match()
        self.genConstraints_Xor_WhitenKey()
        self.genConstraints_additional()

    def gen_Model(self, LPFile, SolFile):
        self.genConstraints_total()
        self.m.addConstr(self.Obj >= 1)
        self.m.setObjective(self.Obj, sense = GRB.MAXIMIZE)
        self.m.write(LPFile)
        # self.m.setParam('TimeLimit', 180 * 60)
        self.m.optimize()
        if self.m.SolCount > 0:
            self.m.write(SolFile)
            Sol = dict()
            with open(SolFile, 'r') as fp:
                for line in fp.readlines():
                    if line[0] != '#':
                        tmp = line
                        tmp = tmp.split()
                        Sol[tmp[0]] = round(float(tmp[1]))
            return True, [Sol['GDeg1'], Sol['GDeg2'], Sol['GMat']]
        else:
            os.remove(LPFile)
            return False, []


def Midori64_attack():
    filename = './Model/'
    if not os.path.exists(filename):
        os.mkdir(filename)
    TR = 10
    with open(filename + f'Result_{TR}.txt', 'w') as fp:
        for ini_r in [8]:
            for mat_r in [3]:
                # for ini_r in range(TR):
                #     for mat_r in range(TR):
                if ini_r != mat_r:
                    print(f'=================== TR{TR}, ini_r {ini_r}, mat_r {mat_r} ===================')
                    cons = constraints_generator(TR, ini_r, mat_r)
                    LPFile = filename + f"TR{TR}_inir{ini_r}_matr{mat_r}.lp"
                    SolFile = filename + f"TR{TR}_inir{ini_r}_matr{mat_r}.sol"
                    flag, res = cons.gen_Model(LPFile, SolFile)
                    if flag:
                        fp.write(str(TR) + ',' + str(ini_r) + ',' + str(mat_r) + ':')
                        fp.write(str(res[0]) + ',' + str(res[1]) + ',' + str(res[2]) + '\n')
                        fp.flush()


if __name__ == '__main__':
    Midori64_attack()
