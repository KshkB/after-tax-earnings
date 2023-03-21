import matplotlib.pyplot as plt

class ProgressiveTax:

    def __init__(self, tax_brackets, tax_rates):
        "tax_brackets is an array of ordered 2-tuples"
        "tax_rates is an array of floats"
        "the arrays tax_brackets and tax_rates have the same dimension"
        "the i-th tax_rate is the rate of tax applicable on the i-th tax bracket"

        self.brackets = tax_brackets
        self.rates = tax_rates
        self.tax_dict = dict(zip(self.brackets, self.rates))        

    def netIncome(self, income):
        "from a yearly income amount, returns the after after-tax income."

        curr_bracket = self.brackets[0]
        for bracket in self.brackets:
            a = bracket[0]
            if income > a:
                curr_bracket = bracket
        net_income = 0
        if self.brackets.index(curr_bracket) == 0:
            net_income = income * (1 - self.tax_dict[curr_bracket])
            return net_income
        else:
            net_income = (income - curr_bracket[0]) * (1 - self.tax_dict[curr_bracket])
            for i in range(self.brackets.index(curr_bracket)):
                bracket = self.brackets[i]
                a = bracket[0]
                b = bracket[-1]
                net_income += (b - a) * (1 - self.tax_dict[bracket])

        return net_income

    def taxPaid(self, income):
        "return the tax paid on a given income"
        net_income = ProgressiveTax.netIncome(self, income)
        return income - net_income
        
    def gross(self, net_income):
        "from net (after tax) income, return the income earned before tax"

        def solver(bracket_index, net_income):
            "helper function to recursively get gross income from net income"
            
            threshhold = self.brackets[bracket_index][0]
            threshhold_upper = self.brackets[bracket_index][-1]
            threshhold_net_income = ProgressiveTax.netIncome(self, threshhold)

            tx_rt = 1 - self.tax_dict[self.brackets[bracket_index]]
            gross_income_summand = (net_income - threshhold_net_income) / tx_rt
            gross_income = threshhold + gross_income_summand

            if gross_income > threshhold_upper:
                bracket_index += 1
                return solver(bracket_index, net_income)
            else:
                return gross_income
            
        brackets = self.brackets
        curr_bracket = brackets[0]
        for bracket in brackets:
            a = bracket[0]
            if net_income > a:
                curr_bracket = bracket 
            
        index = self.brackets.index(curr_bracket)
        return solver(index, net_income)

class Earnings(ProgressiveTax):

    def __init__(self, tax_brackets, tax_rates, wage, wage_growth, savings_rate, savings_returns):
        super().__init__(tax_brackets, tax_rates)

        self.wage = wage
        self.wage_growth = wage_growth/100
        self.savings_rate = savings_rate/100
        self.savings_returns = savings_returns/100

    def returnsAfter(self, investment, years):
        int_yrs = int(years)
        returns = investment
        for _ in range(int_yrs+1):
            returns = returns + self.netIncome(self.savings_returns * returns)
        
        remainder = years - int_yrs
        returns = returns + self.netIncome(self.savings_returns * remainder * returns)
        return returns

    def earningsAfter(self, years):

        int_yrs = int(years)
        curr_earnings = 0
        for yr in range(int_yrs):
            wage = self.wage * ((1 + self.wage_growth)**yr)
            after_tax_wage = self.netIncome(wage)
            after_savings = after_tax_wage*self.savings_rate
            returns_on_savings = self.returnsAfter(after_savings, years-yr)
            curr_earnings += returns_on_savings
            
        remainder = years - int_yrs
        wage = self.wage * ((1 + self.wage_growth)**int_yrs)
        remaining_wage = remainder * wage
        remaining_after_tax = self.netIncome(remaining_wage)
        remaining_after_savings = remaining_after_tax*self.savings_rate
        curr_earnings += remaining_after_savings

        return curr_earnings

    def yearsUntil(self, tgt_earnings):

        yrs = 0
        curr_earnings = self.earningsAfter(yrs)
        while curr_earnings < tgt_earnings:
            yrs += 1
            curr_earnings = self.earningsAfter(yrs)
        yrs += -1

        remainder = tgt_earnings - self.earningsAfter(yrs)
        remainder_before_savings = remainder / self.savings_rate
        remainder_before_tax = self.gross(remainder_before_savings)
        remainder_yrs = remainder_before_tax / self.wage 
        yrs += remainder_yrs

        return yrs 

    def plt(self, years):
        """
        2D plot, Years vs Earnings after Years
        """
        x_data = [i for i in range(years+1)]
        y_data = [
            self.earningsAfter(yrs) for yrs in x_data
        ]

        plt.plot(x_data, y_data)

        plt.title("Earnings Curve")
        plt.xlabel("Time (years)")
        plt.ylabel("Net After-Tax Earnings")
        plt.show()
        return 
    