NB = [float("-inf"),   -1,   -2/3.]
NM = [-1,   -2/3., -1/3.]
NS = [-2/3., -1/3.,  0]
ZO = [-1/3.,  0,    1/3.]
PS = [ 0,    1/3.,  2/3.]
PM = [ 1/3.,  2/3.,  1]
PB = [ 2/3.,  1,    float("inf")]

class Fuzzy():
    def __init__(self, Ke, Kce, Ku):
        self.rule = [None]*19
        self.rule_init()
        self.Ke = Ke
        self.Kce = Kce
        self.Ku = Ku

    def rule_init(self):
        self.rule[0] = (NB, ZO, NB)
        self.rule[1] = (NB, PS, NM)
        self.rule[2] = (NM, ZO, NM)
        self.rule[3] = (NS, ZO, NS)
        self.rule[4] = (NS, PS, ZO)
        self.rule[5] = (NS, PB, PM)
        self.rule[6] = (ZO, NB, NB)
        self.rule[7] = (ZO, NM, NM)
        self.rule[8] = (ZO, NS, NS)
        self.rule[9] = (ZO, ZO, ZO)
        self.rule[10]= (ZO, PS, PS)
        self.rule[11]= (ZO, PM, PM)
        self.rule[12]= (ZO, PB, PB)
        self.rule[13]= (PS, NB, NM)
        self.rule[14]= (PS, NS, ZO)
        self.rule[15]= (PS, ZO, PS)
        self.rule[16]= (PM, ZO, PM)
        self.rule[17]= (PB, NS, PM)
        self.rule[18]= (PB, ZO, PB)

    def strength(self, x1, A1, x2, A2):
        return min(self.membership(x1,A1), self.membership(x2,A2))

    def membership(self, x, A):
        if A[0] == float("-inf") and x<A[1]:
            return 1
        if A[2] == float("inf") and x>=A[1]:
            return 1
        if (x>=A[0] and x<A[1]):
            a = 1/(A[1]-A[0])
            b = -A[0]/(A[1]-A[0])
            return a*x+b
        if (x>=A[1] and x<A[2]):
            a = -1/(A[2]-A[1])
            b = A[2]/(A[2]-A[1])
            return a*x+b
        return 0

    def defuzzy(self, rule_out, rule):
        tmp1 = 0
        tmp2 = 0
        for i in range(len(rule_out)):
            tmp1 += rule_out[i]*rule[i][2][1]
            tmp2 += rule_out[i]
        if tmp2 == 0:
            return 0
        return tmp1/tmp2

    def step(self, error, d_error):
        rule_out = [0]*19
        for i, rule in enumerate(self.rule):
            rule_out[i] = self.strength(error, rule[0], d_error, rule[1])
        return self.Ku*self.defuzzy(rule_out, self.rule)
